import docker

def handleTraefikHostsLabel(label, subfolders = False):
    if '&&' in label and subfolders:
        return (label.split('`')[1] + label.split('`')[3])
    elif '+' in label:
        logger.info("Skipping host entries")
    else:
        return (label.split('`')[1])

def getAllConts():
    client = docker.from_env()
    runningConts = client.containers.list()
    allConts = []
    for cont in runningConts:
        tempCont = [cont.name, cont.short_id, cont.labels]
        allConts.append(tempCont)
    return allConts

def getAllContNames():
    data = getAllConts()
    response = []
    for cont in data:
        response.append(cont[0])
    return response

def getAllProxied():
    data = getAllConts()
    response = []
    for cont in data:
        name = cont[0]
        short_id = cont[1]
        labels = cont[2]
        traefikLabels = []
        for key in labels:
            if key.__contains__("traefik") and not key.__contains__("enable"):
                traefikLabels.append([key,labels[key]])
        if len(traefikLabels) > 0:
            response.append([name,short_id,traefikLabels])
    return response

def getHostsDocker():
    data = getAllProxied()
    response = []
    for app in data:
        labels = app[2]
        for label in labels:
            if "rule" in label[0]:
                response.append(handleTraefikHostsLabel(label[1]))
    return list(set(response))