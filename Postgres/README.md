# PostgreSQL Container for Persistent Storage  

To distinguish whether an error was due to my lack of skills with Docker or Kubernetes, I used the following approach:  

1. Get the desired container running in Docker.  
2. Deploy the container to the Turing Pi 2 k3s cluster.  

### Step 1: Running PostgreSQL in Docker  ###

Fetching the desired PostgreSQL image from Docker Hub (in this case, the latest version):  

```docker pull postgres:latest```

Running a container with the image:

```docker run --name postgres -p 5432:5432 --env-file ./env-file postgres:latest```

The env-file was used to experiment with different environment variables to determine which ones to include in the k3s deployment.

Before testing again, remove the old Docker container:

```docker container rm postgres```

Then proceed to run the container again.

### Step 2: Deploy standard postgres image to k3s  ###

Based on the environment variables determined in Step 1, the YAML files included in this folder were constructed. These files assume the namespace *economy* has been created. You can either create this manually or deploy the ```economy-namespace.yaml``` file in the parent folder.

For this deployment, the environment variables passed to the container are stored as Kubernetes secrets. Since I used Portainer to manage deployments, I first deployed the ```postgres-secrets.yaml``` file and updated the values through the Portainer GUI.

Once the secrets have been deployed, the PostgreSQL container can be deployed using the YAML configuration files.
