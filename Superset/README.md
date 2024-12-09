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

### 1. Creating dockerfile for superset ###
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

### Starting superset for the first time ###

When starting superset and connecting to a new database for the first time, connect to the running container and execute the following to prepare the database.

```flask fab create-admin $@```

```superset db upgrade```

```superset init```

