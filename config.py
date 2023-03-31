from interfaces.logger import appLogger
from pprint import pprint
import os

logger = appLogger()

DIFFTIMER=60
DNSTIMER=600
PORT=5000

CONFIGURATION_KEYS =  ['DOMAIN', 'PORT', 'TOKEN', 'PERSISTENT_FILE', 'TRAEFIK_YML', 'DIFFTIMER', 'DNSTIMER', 'IGNORE_DOMAINS']
IGNORE_DOMAINS = None

for key in CONFIGURATION_KEYS:
    value = os.getenv(key)
    if value is not None:
        globals()[key] = os.getenv(key)
    else:
        if key in globals():
            logger.info(f'{key} was not set by environment, falling back to default: {globals()[key]}')
        else:
            logger.error(f'{key} configuration is missing in environment variables')
            

if IGNORE_DOMAINS is not None:
    IGNORE_HOSTS = IGNORE_DOMAINS.split(",")
    logger.info(F'IGNORE_DOMAINS is set will ignore {IGNORE_HOSTS}')
