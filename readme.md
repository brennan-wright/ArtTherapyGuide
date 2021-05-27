
# Art Therapy Guide

[![Deployment](https://github.com/thisisnotmyuserid/art-therapy/actions/workflows/deploy.yml/badge.svg?branch=master)](https://github.com/thisisnotmyuserid/art-therapy/actions/workflows/deploy.yml)

The Art Therapy Guide was created to help provide information on and arount the topic of Art Therapy to patients, clinicians and students.

![Screenshot](images/screenshot.png)

## Prerequisites for Local Development

You will need:

- `docker` ([install](https://docs.docker.com/install/#supported-platforms))
- `docker-compose` ([install](https://docs.docker.com/compose/install/))

## Getting Started

Once docker and docker desktop is installed, you can run the containers by using docker compose:

```sh
foo@bar:~$ docker-compose up
```

Once the containers are up and the migrations have been applied to your local postgres database, you will want to populate the django-cities models with data.

```sh
foo@bar:~$ docker ps -a #find the ID of the container.
CONTAINER ID   IMAGE        COMMAND                  CREATED      STATUS       PORTS                                            NAMES
c56d375c52d4   django-dev   "sh -c 'python manag…"   3 days ago   Up 6 hours   0.0.0.0:3000->3000/tcp, 0.0.0.0:8000->8000/tcp   art-therapy_web_1
9eac4f1ac33f   postgres     "docker-entrypoint.s…"   3 days ago   Up 6 hours   0.0.0.0:5432->5432/tcp                           art-therapy_db_1

foo@bar:~$ docker exec -it c56d375c52d4 sh #replace c56d375c52d4 with the id of the django docker container. This opens a shell in the container.
$ ./manage.py cities_light --progress
```

At this point you will have to make a superuser for wagtail.

```sh
foo@bar:~$ docker ps -a #find the ID of the container.
CONTAINER ID   IMAGE        COMMAND                  CREATED      STATUS       PORTS                                            NAMES
c56d375c52d4   django-dev   "sh -c 'python manag…"   3 days ago   Up 6 hours   0.0.0.0:3000->3000/tcp, 0.0.0.0:8000->8000/tcp   art-therapy_web_1
9eac4f1ac33f   postgres     "docker-entrypoint.s…"   3 days ago   Up 6 hours   0.0.0.0:5432->5432/tcp                           art-therapy_db_1

foo@bar:~$ docker exec -it c56d375c52d4 sh #replace c56d375c52d4 with the id of the django docker container. This opens a shell in the container.
$ ./manage.py createsuperuser
```

You can now visit [http://localhost:8000](http://localhost:8000) and view the blank wagtail site. Now is a good time to populate your local database with some example data. Navigate to [http://localhost:8000/admin](http://localhost:8000/admin) to login with the super user account and start populating the database.

## Deployment

Deployment is done via a GitHub workflow [here](https://github.com/thisisnotmyuserid/art-therapy/actions) A deployment involves SSHing into the target server, updating the code and deploying the Docker Compose config. Testing and Deployments are run automatically on any commit to the master branch, tests are run on any pull request.

When making a change or bugfix, you should:

- Create a feature branch from `master` called `master/my-branch-name` and test it locally.
- Merge the `master/my-branch-name` into `master` trigger a release of your change to prod.

## Infrastructure

There are two containers that run the application. A Django web server and a Nginx server.

The application runs using Docker Compose. The production environment using a Django container and a Nginx container runs on a single AWS EC2 instance. A seperate instance contains the PostgreSQL database.

Database backups are taken automatically using EC2 [EBS Lifecycle Manager](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snapshot-lifecycle.html). Uploaded files are stored in `s3://art-therapy-guide-media`. Other than uploaded files and the contents of the PostgreSQL database, there is no important state on the EC2 instance or Docker images, which can be torn down and rebuilt at any time.

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
