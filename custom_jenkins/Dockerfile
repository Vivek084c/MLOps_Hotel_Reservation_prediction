FROM jenkins/jenkins:lts

USER root

RUN apt-get update -y && \
    apt-get install -y ca-certificates curl gnupg lsb-release && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
    https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

RUN groupadd -f docker && usermod -aG docker jenkins

RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

USER jenkins