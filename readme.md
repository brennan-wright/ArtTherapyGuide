 
# Art Therapy Guide

[![Deployment](https://github.com/thisisnotmyuserid/ArtTherapyGuide/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/thisisnotmyuserid/ArtTherapyGuide/actions/workflows/deploy.yml)

The Art Therapy Guide was created to help provide information on and arount the topic of Art Therapy to patients, clinicians and students.

## Prerequisites for Local Development

You will need:

- `docker` ([install](https://docs.docker.com/install/#supported-platforms))
- `docker-compose` ([install](https://docs.docker.com/compose/install/))

## Getting Started

Once docker and docker desktop is installed, you can run the containers by using docker compose:

```sh
foo@bar:~$ docker-compose up
```

A super user has been created for the development environment if you use the docker compose file.
user: testadmin
password: testadmin

You can now visit [http://localhost:8000](http://localhost:8000) and view the blank wagtail site. Now is a good time to populate your local database with some example data. Navigate to [http://localhost:8000/admin](http://localhost:8000/admin) to login with the super user account and start populating the database.

## Deployment

Deployment is done via a manually ran Dokku command.

```sh
foo@bar:~$ git push dokku main
```

## Infrastructure

Infrastructure is handled by [Dokku](https://dokku.com/) that is running on an EC2 instance. Postgres, backups, Nginx reverse proxy, and ssl certificates are all handled by Dokku.

DNS is handled by [Route 53](https://aws.amazon.com/route53/).

Emails are sent using [SendGrid](https://app.sendgrid.com).

## Testing

### Running Tests

```sh
foo@bar:~$ docker ps -a #find the ID of the container.
CONTAINER ID   IMAGE        COMMAND                  CREATED      STATUS       PORTS                                            NAMES
c56d375c52d4   django-dev   "sh -c 'python manag…"   3 days ago   Up 6 hours   0.0.0.0:3000->3000/tcp, 0.0.0.0:8000->8000/tcp   art-therapy_web_1
9eac4f1ac33f   postgres     "docker-entrypoint.s…"   3 days ago   Up 6 hours   0.0.0.0:5432->5432/tcp                           art-therapy_db_1

foo@bar:~$ docker exec -it c56d375c52d4 sh #replace c56d375c52d4 with the id of the django docker container. This opens a shell in the container.

$ ./manage.py test #Running Tests and Coverage.

$ coverage run manage.py test #Reading the coverage results.

$ coverage report #Reading the coverage results.

$ coverage html #Reading the coverage results via HTML.
```

### Attaching a Debugger to the Django Container

Although this is somewhat of a personal preference, I have included this as it works well for me. This VS config will allow you to debug as though the application is running locally on your computer. This will attach the debugger directly to the django container. This is because of the config in the .vscode file,

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Django",
            "justMyCode": false,
            "type": "python",
            "request": "attach",
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/code"
                }
            ],
            "port": 3000,
            "host": "127.0.0.1",
        }
    ]
}
```

and the code in the manage.py file.

```python
    if settings.DEBUG:
        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
            import ptvsd

            ptvsd.enable_attach(address=('0.0.0.0', 3000))
            print('Attached!')
```
