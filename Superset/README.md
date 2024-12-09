# Apache superset for data visualisation #

To distinguish whether an error was due to my lack of skills with Docker or Kubernetes, I used the following approach:  

1. Create database in postgres to store superset tables.
2. Create the dockerfile and get the desired container running in Docker.  
3. Deploy the container to the Turing Pi 2 k3s cluster.  


### 1. Creating database for superset ###

Connect to database using the default user previously defined

```psql -d postgres -U postgres <ip of database container>```

Create new database for Superset data

```CREATE DATABASE superset;```

Create user to connect to the Superset database

```CREATE USER supersetuser;```

Grant the new user privileges on the newly created database

```GRANT ALL PRIVILEGES ON DATABASE superset TO supersetuser;```

Change ownership of the new database the to new user

```ALTER DATABASE superset OWNER TO supersetuser;```

### 2. Creating dockerfile for superset ###
The ```env-file```was used to determine which environment variables to handle when deploying in k3s. The ```superset_config.py``` enables the database uri to be defined via a environment variable. The requirement.txt is used to ensure the same versions of packages are en installed every time.

Build the docker image:

```docker build -t superset .```

Run the generated image:

```docker run --name superset -p 8088:8088 --env-file ./env-file superset```

If updates to the env-file are needed remove the container:

```docker container rm superset```

If changes are require to the dockerfile remove the image:

```docker image rm superset:latest```

When a running image has been created update the ```requirements.txt``` by connecting to the container:

```docker exec -it superset bash```

And getting all of the installed packages:

```pip freeze```

### 3. Deploying superset to k3s ###

To deploy my image to k3s, I needed to have the image stored in a registry. Instead of setting up my own, I opted for Docker Hub's personal subscription.  

I also needed to ensure my image was available for a suitable architecture. For this reason, I had to build my image for multiple architectures. To achieve this, I followed **Strategy 1** described in the [Docker documentation](https://docs.docker.com/build/building/multi-platform/#simple-multi-platform-build-using-emulation).  

The base image I initially selected did not have support for the Arm64 architecture. As a result, I had to change the base image. After enabling the necessary Docker components, the images were built using the following command:  

```docker build --platform linux/amd64,linux/arm64/v8 -t benricon/superset:latest .```

Before pushing images to Docker Hub, the local Docker instance must be signed into Docker Hub. This can be achieved by following this [example](https://stackoverflow.com/questions/57108005/how-to-login-to-docker-hub-on-the-command-line)

Once logged in, the images can be pushed to Docker Hub using:

```docker image push benricon/superset:latest```

Based on the environment variables determined in Step 2, the YAML files included in this folder were constructed. These files assume the namespace *economy* has been created. You can either create this manually or deploy the ```economy-namespace.yaml``` file in the parent folder.

For this deployment, the environment variables passed to the container are stored as Kubernetes secrets. Since I used Portainer to manage deployments, I first deployed the ```superset-secrets.yaml``` file and updated the values through the Portainer GUI.

Once the secrets have been deployed, the PostgreSQL container can be deployed using the YAML configuration files.

### Starting superset for the first time ###

When starting superset and connecting to a new database for the first time, connect to the running container and execute the following to prepare the database.

```flask fab create-admin $@```

```superset db upgrade```

```superset init```

