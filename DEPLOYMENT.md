## NOTE: These deployment notes from the original cookie cutter project

## Deployment

You can deploy the stack to a Docker Swarm mode cluster with a main Traefik proxy, set up using the ideas from <a href="https://dockerswarm.rocks" target="_blank">DockerSwarm.rocks</a>, to get automatic HTTPS certificates, etc.

And you can use CI (continuous integration) systems to do it automatically.

But you have to configure a couple things first.

### Traefik network

This stack expects the public Traefik network to be named `traefik-public`, just as in the tutorials in <a href="https://dockerswarm.rocks" class="external-link" target="_blank">DockerSwarm.rocks</a>.

If you need to use a different Traefik public network name, update it in the `docker-compose.yml` files, in the section:

```YAML
networks:
  traefik-public:
    external: true
```

Change `traefik-public` to the name of the used Traefik network. And then update it in the file `.env`:

```bash
TRAEFIK_PUBLIC_NETWORK=traefik-public
```

### Persisting Docker named volumes

You need to make sure that each service (Docker container) that uses a volume is always deployed to the same Docker "node" in the cluster, that way it will preserve the data. Otherwise, it could be deployed to a different node each time, and each time the volume would be created in that new node before starting the service. As a result, it would look like your service was starting from scratch every time, losing all the previous data.

That's specially important for a service running a database. But the same problem would apply if you were saving files in your main backend service (for example, if those files were uploaded by your users, or if they were created by your system).

To solve that, you can put constraints in the services that use one or more data volumes (like databases) to make them be deployed to a Docker node with a specific label. And of course, you need to have that label assigned to one (only one) of your nodes.

#### Adding services with volumes

For each service that uses a volume (databases, services with uploaded files, etc) you should have a label constraint in your `docker-compose.yml` file.

To make sure that your labels are unique per volume per stack (for example, that they are not the same for `prod` and `stag`) you should prefix them with the name of your stack and then use the same name of the volume.

Then you need to have those constraints in your `docker-compose.yml` file for the services that need to be fixed with each volume.

To be able to use different environments, like `prod` and `stag`, you should pass the name of the stack as an environment variable. Like:

```bash
STACK_NAME=stag-nocookieanalytics sh ./scripts/deploy.sh
```

To use and expand that environment variable inside the `docker-compose.yml` files you can add the constraints to the services like:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.${STACK_NAME}.app-db-data == true
```

note the `${STACK_NAME}`. In the script `./scripts/deploy.sh`, the `docker-compose.yml` would be converted, and saved to a file `docker-stack.yml` containing:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.nocookieanalytics.app-db-data == true
```

If you add more volumes to your stack, you need to make sure you add the corresponding constraints to the services that use that named volume.

Then you have to create those labels in some nodes in your Docker Swarm mode cluster. You can use `docker-auto-labels` to do it automatically.

#### `docker-auto-labels`

You can use [`docker-auto-labels`](https://github.com/tiangolo/docker-auto-labels) to automatically read the placement constraint labels in your Docker stack (Docker Compose file) and assign them to a random Docker node in your Swarm mode cluster if those labels don't exist yet.

To do that, you can install `docker-auto-labels`:

```bash
pip install docker-auto-labels
```

And then run it passing your `docker-stack.yml` file as a parameter:

```bash
docker-auto-labels docker-stack.yml
```

You can run that command every time you deploy, right before deploying, as it doesn't modify anything if the required labels already exist.

#### (Optionally) adding labels manually

If you don't want to use `docker-auto-labels` or for any reason you want to manually assign the constraint labels to specific nodes in your Docker Swarm mode cluster, you can do the following:

* First, connect via SSH to your Docker Swarm mode cluster.

* Then check the available nodes with:

```console
$ docker node ls


// you would see an output like:

ID                            HOSTNAME               STATUS              AVAILABILITY        MANAGER STATUS
nfa3d4df2df34as2fd34230rm *   dog.example.com        Ready               Active              Reachable
2c2sd2342asdfasd42342304e     cat.example.com        Ready               Active              Leader
c4sdf2342asdfasd4234234ii     snake.example.com      Ready               Active              Reachable
```

then chose a node from the list. For example, `dog.example.com`.

* Add the label to that node. Use as label the name of the stack you are deploying followed by a dot (`.`) followed by the named volume, and as value, just `true`, e.g.:

```bash
docker node update --label-add nocookieanalytics.app-db-data=true dog.example.com
```

* Then you need to do the same for each stack version you have. For example, for staging you could do:

```bash
docker node update --label-add stag-nocookieanalytics.app-db-data=true cat.example.com
```

### Deploy to a Docker Swarm mode cluster

There are 3 steps:

1. **Build** your app images
2. Optionally, **push** your custom images to a Docker Registry
3. **Deploy** your stack

---

Here are the steps in detail:

1. **Build your app images**

* Set these environment variables, right before the next command:
  * `TAG=prod`
  * `FRONTEND_ENV=production`
* Use the provided `scripts/build.sh` file with those environment variables:

```bash
TAG=prod FRONTEND_ENV=production bash ./scripts/build.sh
```

2. **Optionally, push your images to a Docker Registry**

**Note**: if the deployment Docker Swarm mode "cluster" has more than one server, you will have to push the images to a registry or build the images in each server, so that when each of the servers in your cluster tries to start the containers it can get the Docker images for them, pulling them from a Docker Registry or because it has them already built locally.

If you are using a registry and pushing your images, you can omit running the previous script and instead using this one, in a single shot.

* Set these environment variables:
  * `TAG=prod`
  * `FRONTEND_ENV=production`
* Use the provided `scripts/build-push.sh` file with those environment variables:

```bash
TAG=prod FRONTEND_ENV=production bash ./scripts/build-push.sh
```

3. **Deploy your stack**

* Set these environment variables:
  * `DOMAIN=nocookieanalytics.com`
  * `TRAEFIK_TAG=nocookieanalytics.com`
  * `STACK_NAME=nocookieanalytics`
  * `TAG=prod`
* Use the provided `scripts/deploy.sh` file with those environment variables:

```bash
DOMAIN=nocookieanalytics.com \
TRAEFIK_TAG=nocookieanalytics.com \
STACK_NAME=nocookieanalytics \
TAG=prod \
bash ./scripts/deploy.sh
```

---

If you change your mind and, for example, want to deploy everything to a different domain, you only have to change the `DOMAIN` environment variable in the previous commands. If you wanted to add a different version / environment of your stack, like "`preproduction`", you would only have to set `TAG=preproduction` in your command and update these other environment variables accordingly. And it would all work, that way you could have different environments and deployments of the same app in the same cluster.

#### Deployment Technical Details

Building and pushing is done with the `docker-compose.yml` file, using the `docker-compose` command. The file `docker-compose.yml` uses the file `.env` with default environment variables. And the scripts set some additional environment variables as well.

The deployment requires using `docker stack` instead of `docker-swarm`, and it can't read environment variables or `.env` files. Because of that, the `deploy.sh` script generates a file `docker-stack.yml` with the configurations from `docker-compose.yml` and injecting the environment variables in it. And then uses it to deploy the stack.

You can do the process by hand based on those same scripts if you wanted. The general structure is like this:

```bash
# Use the environment variables passed to this script, as TAG and FRONTEND_ENV
# And re-create those variables as environment variables for the next command
TAG=${TAG} \
# Set the environment variable FRONTEND_ENV to the same value passed to this script with
# a default value of "production" if nothing else was passed
FRONTEND_ENV=${FRONTEND_ENV-production} \
# The actual comand that does the work: docker-compose
docker-compose \
# Pass the file that should be used, setting explicitly docker-compose.yml avoids the
# default of also using docker-compose.override.yml
-f docker-compose.yml \
# Use the docker-compose sub command named "config", it just uses the docker-compose.yml
# file passed to it and prints their combined contents
# Put those contents in a file "docker-stack.yml", with ">"
config > docker-stack.yml

# The previous only generated a docker-stack.yml file,
# but didn't do anything with it yet

# docker-auto-labels makes sure the labels used for constraints exist in the cluster
docker-auto-labels docker-stack.yml

# Now this command uses that same file to deploy it
docker stack deploy -c docker-stack.yml --with-registry-auth "${STACK_NAME}"
```

## Docker Compose files and env vars

There is a main `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker-compose`.

And there's also a `docker-compose.override.yml` with overrides for development, for example to mount the source code as a volume. It is used automatically by `docker-compose` to apply overrides on top of `docker-compose.yml`.

These Docker Compose files use the `.env` file containing configurations to be injected as environment variables in the containers.

They also use some additional configurations taken from environment variables set in the scripts before calling the `docker-compose` command.

It is all designed to support several "stages", like development, building, testing, and deployment. Also, allowing the deployment to different environments like staging and production (and you can add more environments very easily).

They are designed to have the minimum repetition of code and configurations, so that if you need to change something, you have to change it in the minimum amount of places. That's why files use environment variables that get auto-expanded. That way, if for example, you want to use a different domain, you can call the `docker-compose` command with a different `DOMAIN` environment variable instead of having to change the domain in several places inside the Docker Compose files.

Also, if you want to have another deployment environment, say `preprod`, you just have to change environment variables, but you can keep using the same Docker Compose files.

### The .env file

The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.

Depending on your workflow, you could want to exclude it from Git, for example if your project is public. In that case, you would have to make sure to set up a way for your CI tools to obtain it while building or deploying your project.

One way to do it could be to add each environment variable to your CI/CD system, and updating the `docker-compose.yml` file to read that specific env var instead of reading the `.env` file.
