import yaml
from interfaces.logger import appLogger
from interfaces.docker import handleTraefikHostsLabel

logger = appLogger()

def getHostsTraefikYML(location):
    with open(location, "r") as stream:
        try:
            content = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error('Traefik Yaml file couldnt be loaded', exc)

    routers = content['http']['routers']
    hosts = []
    for router in routers:
        hosts.append(handleTraefikHostsLabel(routers[router]['rule']))
    return hosts
