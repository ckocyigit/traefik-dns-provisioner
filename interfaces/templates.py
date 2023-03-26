import config
from bs4 import BeautifulSoup

path = config.XML_PATH

class TraefikExists(Exception):
    pass

def translateCont(cont):
    return f'my-{cont}.xml'

def getXMLData(cont):
    try:
        with open(path + translateCont(cont), 'r') as f:
            data = f.read()
            return BeautifulSoup(data, "xml")
    except FileNotFoundError:
        print(f'File was not found for {cont}')

def getNameWrittenInXML(cont):
    data = getXMLData(cont)
    return data.find_all('Name')[0].text

def getTraefikConf(cont):
    data = getXMLData(cont)
    configs = data.find_all('Config')
    response = {}
    for entry in configs:
        if 'traefik' in entry['Name']:
            response[entry['Name']] = entry.text
    return response   

def createConf(conf: dict):
    response = []
    for k in conf:
        response.append(f'<Config Default="" Description="" Display="always" Mask="false" Mode="" Name="{k}" Required="false" Target="{k}" Type="Label">{conf[k]}</Config>')
    return response

def createConfXML(host: str,tls = 'true',entrypoints = 'https',middlewares = ''):
    conf = {}
    routerName = host.split('.')[0]
    conf[f'traefik.http.routers.{routerName}.tls'] = tls
    conf[f'traefik.http.routers.{routerName}.rule'] = f'Host(`{host}`)'
    if len(middlewares) > 0: conf[f'traefik.http.routers.{routerName}.middlewares'] = middlewares
    conf[f'traefik.http.routers.{routerName}.entrypoints'] = entrypoints
    response = []
    for k in conf:
        response.append(f'<Config Default="" Description="" Display="always" Mask="false" Mode="" Name="{k}" Required="false" Target="{k}" Type="Label">{conf[k]}</Config>')
    return response

def appendConfig(cont: str, input: dict):
    if len(getTraefikConf(cont)) == 0 :
        try:
            with open(path + translateCont(cont)) as f:
                tree = BeautifulSoup(f.read(), "xml")
                for entry in input:
                    tree.Container.append(BeautifulSoup(entry, "xml"))
            with open(path + translateCont(cont), "w") as f:            
                f.write(str(tree))
                f.close()
        except FileNotFoundError:
            print(f'File was not found for {cont}')
    else:
        raise TraefikExists("Traefik already exists")
        