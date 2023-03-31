from flask import Flask
from flask_apscheduler import APScheduler
import requests
from interfaces.logger import appLogger
from version import __version__ 
from interfaces.container import getHostsDocker
from interfaces.persistence import Persistence
from interfaces.traefik import getHostsTraefikYML
from interfaces.ionos import Ionos
from tdp_exceptions import DNSUpdateError, IonosApiRateExceedanceError

title = f"TDP - DNS Provisioner - version: {__version__}"
logger = appLogger()
logger.info(f'{title:_^100}')

import config
app = Flask(__name__)
scheduler = APScheduler()
persistence = Persistence(config.PERSISTENT_FILE)
ionos = Ionos(config.TOKEN)

@app.route('/')
def root() -> str:
   links = []
   ignore_links = ['static', 'root']
   for rule in app.url_map.iter_rules():
      if rule.endpoint not in ignore_links:
         link = f'<a href="{rule}">{rule}</a>'
         links.append(link)

   links_str = '<br>'.join(links)
	
   return f"""
        {title}<br><br>
        APIs:<br>
        {links_str}
    """

@app.route('/api/tdp/spot')
def get_single_point_of_truth() -> list:
   dockerHosts: list = getHostsDocker()
   traefikHosts: list = getHostsTraefikYML(config.TRAEFIK_YML)
   return list(set(dockerHosts + traefikHosts))

@app.route('/api/tdp/docker')
def get_docker_domains() -> list:
   dockerHosts: list = getHostsDocker()
   return dockerHosts

@app.route('/api/tdp/traefik')
def get_traefik_domains() -> list:
   traefikHosts: list = getHostsTraefikYML(config.TRAEFIK_YML)
   return traefikHosts

def compare_spot_domains_to_local_state(spot) -> list:
   """checkForNewHosts

   Check if both Traefik hosts and Docker hosts have changed from last state

   :param hosts: list
   :return: boolean
            True: when difference
            False: when no difference
   """
   if persistence.hasKey('domains'):
      state = persistence.getValue('domains')
      domains_not_in_state = [domain for domain in spot if domain not in state]
      domains_not_in_spoc = [domain for domain in state if domain not in spot]
      return domains_not_in_spoc + domains_not_in_state
   else: # Scenario 1
      logger.info(f"Local state is empty, dumping all domains into it \n {spot}")
      persistence.setValue('domains', spot)
      return spot

@app.route('/api/provider/diff')
def get_diff_local_to_provider() -> bool:
   """diffStateToIonos

   diff local state to ionos

   :param hosts
   :return: boolean
            True: when difference
            False: when no difference
   """
   domain = config.DOMAIN
   zoneID = ionos.getZoneID(domain)
   hosts = ionos.getRecordNames(domain)
   names = []
   for key in hosts:
      names.append(key)

   if persistence.hasKey('domains'):
      state = persistence.getValue('domains')
      diff = [item for item in names if item not in state]
      
      if hasattr(config, 'IGNORE_HOSTS'): 
         diff = [item for item in diff if item not in config.IGNORE_HOSTS]

      if len(diff) != 0:
         logger.info(f"Diff detected to Ionos: {diff} Doing some householding")
         for hostToDelete in diff:
            logger.info(f'Deleting {hostToDelete} from Ionos')
            ionos.deleteRecord(zoneID,hosts[hostToDelete])
   return diff

@app.route('/api/provider')
def get_provider_domains() -> bool:
   domain = config.DOMAIN
   hosts = ionos.getRecordNames(domain)
   names = []
   for key in hosts:
      names.append(key)
   return names   

@app.route('/api/dyndns/update')
@scheduler.task("interval", id="update_dyn_dns_ip", seconds=int(config.DNSTIMER), misfire_grace_time=900, max_instances=1)
def update_dyn_dns_ip():
   try:
      response = requests.request("GET", persistence.getUpdateURL())
      if "API rate limit exceeded" in response.text:
         raise IonosApiRateExceedanceError("API rate limit exceeded")
      logger.info(f"Updating DNS IPv4 {response.text}")
   except DNSUpdateError as e:
      logger.warning(f"Updating DNS failed catched following exception: {e}")
   except IonosApiRateExceedanceError as e:
      logger.warning(f"Exceeded Ionos API Call Limit: {e}")
   return response.text

@app.route('/api/tdp/diff')
@scheduler.task("interval", id="get_diff_spot_and_local_state", seconds=int(config.DIFFTIMER), misfire_grace_time=900, max_instances=1)
def get_diff_spot_and_local_state():
   """app

   Single Point of Truth is always Docker and Traefik hosts
   Main app loop runs every config.DIFFTIMER
   """
   spot = get_single_point_of_truth()
   diff = compare_spot_domains_to_local_state(spot)

   if len(diff) != 0: # Scenario 2,3
      logger.info(f"Change detected: {diff}, updating local state")
      response = ionos.register_domains(spot)
      persistence.saveResponse(bulk_id=response.bulk_id, domains=response.domains, description=response.description, update_url=response.update_url)
      update_dyn_dns_ip()
      get_diff_local_to_provider()
   else:
      logger.debug("No changes continuing")

   return diff


@app.route('/api/tdp/state')
def get_state():
   return persistence.read()

if __name__ == "__main__":
   app.run(port=config.PORT, debug=True, host="0.0.0.0")
   scheduler.api_enabled = True
   scheduler.init_app(app)
   scheduler.start()