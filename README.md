![django-nginx-githubactions.jpg](https://krzysztofbrzozowski.com/media/2024/01/15/django-nginx-githubactions.jpg)

# Current tests and deploy status
[![Tests](https://github.com/krzysztofbrzozowski/krzysztofbrzozowski_website/actions/workflows/tests.yml/badge.svg)](https://github.com/krzysztofbrzozowski/krzysztofbrzozowski_website/actions?query=workflow%3ATests)
[![Deploy](https://github.com/krzysztofbrzozowski/krzysztofbrzozowski_website/actions/workflows/deploy.yml/badge.svg)](https://github.com/krzysztofbrzozowski/krzysztofbrzozowski_website/actions?query=workflow%3ADeploy)

# About the project
Personal blog backend and part of frontend. Live demo can find [krzysztofbrzozowski.com](https://krzysztofbrzozowski.com)

Project is based on Django 5, PostgreSQL, NGINX and Docker. All of the code is available widely except static files.

More description can be found in article [Django based website deployed using github actions](https://krzysztofbrzozowski.com/project/django-based-website-deployed-using-github-actions)

## Recreate DB
```bash
pg_dump -U postgres -a -t projects_projectsmeta srcdb | psql -U <db_user> destdb; 


pg_dump --column-inserts -a -t zones_seq -t interway -t table_3 ... > /tmp/zones_seq.sql  
```

## NGINX
In project docker-gen generates reverse proxy configs ->
[more info](https://github.com/nginx-proxy/nginx-proxy/tree/main)

# First steps to run website locally
Clone a repo. Repository contains submodules. To download those run
(be aware not all of them are public)
```bash
git config --global submodule.recurse true

or

git submodule update --init --recursive
```

Run Docker compose 
```bash
docker compose -f "docker-compose.yml" up -d --build
```

# First steps to run website on VPS
### Install Docker on Ubuntu
```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

apt-cache policy docker-ce

sudo apt install docker-ce

sudo systemctl status docker
```

### Install Docker Compose
```bash
mkdir -p ~/.docker/cli-plugins/

curl -SL https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose

chmod +x ~/.docker/cli-plugins/docker-compose

docker compose version
```

### KNOWN ISSUE: during first-time init
```bash
The authenticity of host '<<IP address>>' port <<port#>>: can't be established.
ECDSA key fingerprint is SHA256:<<some_sha>>.
Are you sure you want to continue connecting (yes/no)?

Just try to initialize any other repo via SSH on VPS and type 'yes'
```

### KNOWN ISSUE: Manage Docker as a non-root user
More info [Post-installation steps for Docker Engine](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
```bash
---
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock:
---
Solution:

sudo groupadd docker

sudo usermod -aG docker ${USER}

su -s ${USER}

or
sudo chmod 777 /var/run/docker.sock
```
### Setup secrets for GitHub Actions and run action
![github-actions-secrets.png](https://krzysztofbrzozowski.com//media/2024/01/22/github-actions-secrets.png)

### Check for open ports and close any exposed ones
```bash
udo ss -tulnp | grep LISTEN
sudo ufw deny 5432
```


# Useful commands
Docker compose (to run project)
```bash
docker compose -f "docker-compose.yml" up -d --build
```

See logs nginx
```bash
docker logs <container id>

docker logs 2677eef108c4
```

Run shell in Docker container
```bash
docker exec -it <container id> sh

docker exec -it 90c39aabcab0 sh
```

See logs per container
```bash
docker logs --tail 1000 -f <container id>

docker logs --tail 1000 -f 90c39aabcab0
```

Create new DB
```bash
sudo -u postgres psql

in container you can use:
psql -U postgres
CREATE DATABASE db;
```

Kill all containers
```bash
docker kill $(docker ps -q)
```

Clean every docker image, container
```bash
docker system prune
```

How to copy PostgreSQL DB
```bash
On server side
$ export PGPASSWORD="passwd" ; pg_dump -U <db_user | default: postgres> your_db > place/to/store/db.pgsql

In Docker Container
$ psql -U <db_user | default: postgres> db < place/to/store/db.pgsql
```

Send some file using SCP
```bash
scp -r src_dir root@dest_ip:/home/user/dsc_dir
```

Add secret key to your env variables (macOS)

```bash
echo "export SECRET_KEY_KB=!secret!" >> ~/.zshenv

source ~/.zshenv
```

List of used env variables (macOS, Ubuntu)
```bash
env
```

Your secret key shall be copied into Docker image if you are developing page locally e.g.
```yml
environment:
    - SECRET_KEY_KB=${SECRET_KEY_KB}
```

Generate random secret key
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

# ACME campaign
in file e.g. /etc/nginx/vhost.d/dev.krzysztofborzowski.com put your stitic or media files such as
```bash
location /media/ {
        alias /usr/src/app/media/;
    }
```


