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
import config

app = Flask(__name__)
scheduler = APScheduler()
logger = appLogger()
persistence = Persistence(config.PERSISTENT_FILE)
ionos = Ionos(config.TOKEN)

@app.route('/')
def root():
	return(f"TDP Version: {__version__}")

@app.route('/hosts')
def mergeHosts() -> list:
   dockerHosts: list = getHostsDocker()
   traefikHosts: list = getHostsTraefikYML(config.TRAEFIK_YML)
   return dockerHosts + traefikHosts


def checkHostsAreSameAsPersisted(hosts) -> bool:
   """checkForNewHosts

   Check if both Traefik hosts and Docker hosts have changed from last state

   :param hosts: list
   :return: boolean
            True: when difference
            False: when no difference
   """
   if persistence.hasKey('domains'):
      state = persistence.getValue('domains')
      diff = [item for item in hosts if item not in state]
      if len(diff) == 0:
         return False
      else:
         logger.info(f"Change detected: {diff} updating")
         persistence.setValue('domains', hosts)
         return True
   else:
      logger.info(f"Hosts state has never been set, saving current state as initial foundation \n {hosts}")
      persistence.setValue('domains', hosts)
      return True


def diffStateToIonos() -> bool:
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
      
      if hasattr(config, 'IGNORE_HOSTS'): diff = [item for item in diff if item not in config.IGNORE_HOSTS]

      if len(diff) != 0:
         logger.info(f"Diff detected to Ionos: {diff} Doing some householding")
         for hostToDelete in diff:
            logger.info(f'Deleting {hostToDelete} from Ionos')
            ionos.deleteRecord(zoneID,hosts[hostToDelete])
   return names

@scheduler.task("interval", id="dnsUpdater", seconds=int(config.DNSTIMER), misfire_grace_time=900, max_instances=1)
def dnsUpdater():
   try:
      response = requests.request("GET", persistence.getUpdateURL())
      if "API rate limit exceeded" in response.text:
         raise IonosApiRateExceedanceError("API rate limit exceeded")
      logger.info(f"Updating DNS IPv4 {response.text}")
   except DNSUpdateError as e:
      logger.warn(f"Updating DNS failed catched following exception: {e}")
   except IonosApiRateExceedanceError as e:
      logger.warn(f"Exceeded Ionos API Call Limit: {e}")


@app.route('/triggerdiff')
@scheduler.task("interval", id="checkForDiff", seconds=int(config.DIFFTIMER), misfire_grace_time=900, max_instances=1)
def checkForDiff():
   """app

   Single Point of Truth is always Docker and Traefik hosts
   Main app loop runs every config.DIFFTIMER
   """
   payload = mergeHosts()
   
   if checkHostsAreSameAsPersisted(payload):
      response = ionos.registerDomains(payload)
      persistence.saveResponse(bulk_id=response.bulk_id, domains=response.domains, description=response.description, update_url=response.update_url)
      dnsUpdater()

   return diffStateToIonos()

@app.route('/state')
def showState():
   return persistence.read()

if __name__ == "__main__":
   logger.info(f"TDP - DNS Provisioner - version: {__version__}")
   if hasattr(config, 'IGNORE_DOMAINS'): logger.info(F'IGNORE_DOMAINS is set will ignore {config.IGNORE_DOMAINS}')   
   scheduler.api_enabled = True
   scheduler.init_app(app)
   scheduler.start()
   app.run(port=config.PORT, debug=True, host="0.0.0.0")