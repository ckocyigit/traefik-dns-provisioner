# Traefik DNS Provisioner

<p align="center">
  <img src="traefik-dns-provisioner.png" width="350" title="Traefik-DNS-Provisioner">
</p>


TDP Traefik DNS Provisioner is a companion product to [Traefik](https://traefik.io/) that automatically provides DNS records in DNS providers based on the Docker labels that have already been set, due to traefik.

```important
This has been a weekend project for me and is more of a scaffold or an initial commit for this idea.

My provider currently is IONOS, which is why the current code does only supports IONOS.

I would love to tinker on this idea if I get some positive feedback from you on this idea.
```


## Current features

* Utilizing the docker engine for reading and intepreting docker labels
* Interpreting subdomain and subfolder labels
* Having a persistency yaml file
* [Dynamic DNS] Updating the dynamic dns ip
* Creating and deleting dns A records in the provider on a scheduled manner
* Docker labels is the SPoT (Single Point of Truth) for the domains
* Parameter for ignoring domains from the SPoT (meaning those will be ignored from householding)
* Reading the dynamic traefik file and parsing domain records from there
* [Unraid] [Plugin?] Reading the Template XML's and adding Traefik Labels automagically

## Future features?

* Add docker compose template
* Expanding Flask Backend API
* Companion frontend for the api
* Github pipeline and docker registry
* Obviously other providers
    - Cloudfare
    - AWS 53
    - Google Cloud
    - Azure
    - ...
* This could also be a Traefik plugin instead of a standalone thing, maybe rewrite in Go
* ...


## Basic usage

### Configuraton

All configuration is done via environment variables.

Current configuration:

| Var | Example | Default | Explanation |
| --- | --- | --- | --- |
| DOMAIN | mydomain.com | **Mandatory** | The main domain used in the DNS records |
| TOKEN | your_token | **Mandatory** | The token used for authentication with the DNS provider. Currently onyl IONOS |
| PERSISTENT_FILE | /data/traefik-dns-provisioner/state.yaml | **Mandatory** | The path to the file with the state  |
| TRAEFIK_YML | /data/traefik/traefik.yml | **Mandatory** | The path to the dynamic traefik file |
| PORT | 8080 | 5000 | Flask port |
| DIFFTIMER | 300 | 60 | The number of seconds that elapse between checking changes in the Traefik configuration file and DNS provisioning. |
| DNSTIMER | 3600 | 600 | The number of seconds between the dynamic dns updates |
| IGNORE_DOMAINS | subdomain1.mydomain.com,subdomain2.mydomain.com | Empty | Eine kommaseparierte Liste von Subdomains, die ignoriert werden sollen |

### Run

Be sure to have the configuration done beforehand

```bash
python app.py
```

### Docker

```bash
docker run -d \
-e DOMAIN="mydomain.tld" \
-e TOKEN="asdsadsadsadasd" \
-e PERSISTENT_FILE="/data/traefik-dns-provisioner/state.yaml" \
-e TRAEFIK_YML="/traefik/dynamic_conf.yml"
ghcr.io/ckocyigit/tdp:latest
```


## License 

GPL-3.0
For more information see the LICENSE file