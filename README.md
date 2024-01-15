![django-nginx-githubactions.jpg](https://krzysztofbrzozowski.com/media/2024/01/15/django-nginx-githubactions.jpg)

## Current tests and deploy status
[![Tests](https://github.com/krzysztofbrzozowski/krzysztofbrzozowski_website/actions/workflows/tests.yml/badge.svg)](https://github.com/krzysztofbrzozowski/krzysztofbrzozowski_website/actions?query=workflow%3ATests)
[![Deploy](https://github.com/krzysztofbrzozowski/krzysztofbrzozowski_website/actions/workflows/deploy.yml/badge.svg)](https://github.com/krzysztofbrzozowski/krzysztofbrzozowski_website/actions?query=workflow%3ADeploy)

## Project requirements
* After push and sucessfull tests CI shall deploy code to remote server with rebased version of webpage
* Webpage is running in Docker container
* Webpage is using database to store posts, projects and other required backend data

## TODO
* [x] Fix current CI issues (Error: Version 3.1 with arch x64 not found)
* [x] Copy production DB form server
* [x] Distinguish in Django settings running in prod mode and test/debug mode
* [x] Run project locally with production DB
* [x] Configure Nginx using container
* [x] Configure Gunicorn
* [x] Create sketch for CI (GitHub actions) to be able pushing code into the server
* [] Initial setup shall contain initialization od DB
* [x] The way how to create SECRET_KEY_KB

## Useful info
Add secret key to your env variables (macOS)

```
echo "export SECRET_KEY_KB=!secret!" >> ~/.zshenv
source ~/.zshenv
```

List of used env variables (macOS)
```
env
```

Your secret key shall be copied into Docker image if you are developing page locally e.g.:
```yml
environment:
    - SECRET_KEY_KB=${SECRET_KEY_KB}
```

Generate random secret key
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Useful commands
Docker compose (to run project)
```
docker compose -f "docker-compose.yml" up -d --build
```

See logs nginx
```
docker logs <container id>
docker logs 2677eef108c4
```

Run shell in Docker container
```
docker exec -it <container id> sh
docker exec -it 90c39aabcab0 sh
```

See logs per container
```
docker logs --tail 1000 -f <container id>
docker logs --tail 1000 -f 90c39aabcab0
```

Create new DB
```
sudo -u postgres psql
- in container you can use:
psql -U postgres
CREATE DATABASE db;
```

How to copy PostgreSQL DB
```
On server side
$ export PGPASSWORD="passwd" ; pg_dump -U <db_user | default: postgres> your_db > place/to/store/db.pgsql

In Docker Container
$ psql -U <db_user | default: postgres> db < place/to/store/db.pgsql
```