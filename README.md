# A Gentle Jenkins Primer

A mild refresher for Jenkins.

## Glossary

* Master Server: Controls the pipelines and schedules Builds
* Agents/Nodes: Execute the builds
* Permanent Agents: Dedicated servers for running jobs
* Cloud Agents: Ephemeral Agents on Docker/Kubernetes/AWS Fleet Manager
* Freestyle Build: Simple scripts that are triggered on an event like GitHub Commit
* Pipelines: More complex (multi-stage) workflows (eg: Clone, Build, Test, Package, Deploy)

## 1. Installing Jenkins (Docker)

Create the Docker network

```bash
docker network create jenkins
```

Build the Jenkins image

```bash
docker build -t my-jenkins:latest .
```

Start the Docker-in-Docker sidecar (allows Jenkins to run Docker commands inside pipelines)

```bash
docker run --name jenkins-docker --detach \
  --privileged --network jenkins --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --volume jenkins-data:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind
```

Start the Jenkins container (Master Server)

```bash
docker run --name jenkins-blueocean --restart=on-failure --detach \
  --network jenkins \
  --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  my-jenkins:latest
```

A few details on the docker run commands we executed just now:

- Port 8080 runs the Jenkins Web UI
- Port 50000 is used by Agents to communicate with the Master (over JNLP/TCP)
- Uses the "jenkins" network we created earlier for inter-container connectivity
- Binds to the DIND container over tcp://docker:2376

## 2. Initial Setup

Get the initial admin password

```bash
docker exec jenkins-blueocean cat /var/jenkins_home/secrets/initialAdminPassword
```

Open http://localhost:8080 in your browser and enter the password to unlock Jenkins server.

You will be presented with two options:
- Install Suggested Plugins -> Choose this
- Select Plugins to install

You will be asked to "Create First Admin User"
- Username
- Password
- Confirm Password
- Full Name
- E-mail Address

Leave "Instance Configuration" at its default "http://localhost:8080/"

That's it! You have set up Jenkins.

## 3. Configure Cloud Agent (Docker)

First, install the "Docker" plugin.

- Go to http://localhost:8080/manage/pluginManager/available
- Filter for "Cloud Providers"
- Select **Docker** from the list and click **Install**
- Restart Jenkins when prompted

Next, create a new Cloud.

- Go to http://localhost:8080/manage/cloud/new
- Provide name `docker` and select type **Docker**, then click **Create**

### 3a. Configure Docker Cloud

Under **Docker Cloud details**:

- **Docker Host URI**: `tcp://docker:2376`
- **Server credentials**: Add TLS credentials (see below)

To add TLS credentials, retrieve the certs from the running Jenkins container:

```bash
docker exec jenkins-blueocean cat /certs/client/ca.pem
docker exec jenkins-blueocean cat /certs/client/cert.pem
docker exec jenkins-blueocean cat /certs/client/key.pem
```

- Click **Add** next to Server credentials → **Jenkins**
- Kind: **Docker Host Certificate Authentication**
- Paste the contents of `ca.pem`, `cert.pem`, and `key.pem` into the respective fields
- Click **Add**, then select the new credential from the dropdown

Click **Test Connection** — you should see the Docker version returned, confirming connectivity.

> **Note**: If Test Connection fails with `UnknownHostException: docker`, ensure the `jenkins-docker` (DIND) container is running and on the `jenkins` network.
> ```bash
> docker network inspect jenkins --format '{{range .Containers}}{{.Name}} {{end}}'
> ```

### 3b. Configure Docker Agent Template

Scroll down to **Docker Agent templates** and click **Add Docker Template**.

- **Labels**: `python-agent` (used to target this agent in pipelines)
- **Enabled**: checked
- **Docker Image**: `pluto92/jenkins-agent-python:3.12`
- **Instance Capacity**: `2` (max concurrent agents)
- **Remote File System Root**: `/home/jenkins/agent`

Click **Save**.


## References
- [Jenkins Tutorial - by DevOps Journey](https://www.youtube.com/watch?v=6YZvp2GwT0A)
- [Jenkins Tutorial - Repo](https://github.com/devopsjourney1/jenkins-101)
- [Docs - Installing Jenkins](https://www.jenkins.io/doc/book/installing/)
- [Docs - Jenkins Environment Variables](http://localhost:8080/env-vars.html/)

