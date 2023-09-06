Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04"
  config.vm.box_check_update = false
  config.vm.box_download_insecure = false
  config.ssh.insert_key = true

  config.vm.define "Production" do |woo|
    woo.vm.hostname = "Production"
    woo.vm.network "private_network", ip: "192.168.10.10"

    woo.vm.provider "virtualbox" do |vb|
      vb.memory = 4096
      vb.cpus = 2
      vb.name = "Production"
    end

    woo.vm.provision "shell", inline: <<-SHELL
      #!/bin/bash
      sudo apt update && sudo apt upgrade -y
      sudo apt-get install ufw -y
      sudo ufw default deny incoming
      sudo ufw default allow outgoing
      sudo ufw allow 8080
      sudo ufw allow 80
      sudo ufw allow 9090
      sudo ufw allow 443
      sudo ufw allow 22
      sudo ufw allow 3306
      sudo ufw allow 8888
      sudo ufw enable
      sudo -E apt install apt-transport-https ca-certificates curl software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo -E apt-key add -
      CODENAME=$(lsb_release -cs)
      sudo -E add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $CODENAME stable"
      sudo -E apt update
      sudo -E apt install docker-ce=5:20.10.24~3-0~ubuntu-$CODENAME docker-ce-cli=5:20.10.24~3-0~ubuntu-$CODENAME containerd.io docker-compose -y
      sudo usermod -a -G docker vagrant
      docker network create -d bridge vagrant_wordpress_network
      sudo useradd -m -d /home/jenkins -G docker jenkins
      sudo systemctl enable docker
      sudo systemctl start docker
      sudo apt install haproxy -y
      sudo systemctl enable haproxy
      sudo systemctl start haproxy
      cp /home/vagrant/haproxy_micro.cfg /etc/haproxy/haproxy.cfg
      sudo systemctl restart haproxy
      sudo apt install openjdk-17-jdk -y
      sudo apt install python3-pip -y
      pip install -U mock
      pip install nose
      sudo timedatectl set-timezone Europe/Paris
    SHELL

    woo.vm.provision "file", source: "docker-compose.yml", destination: "/home/vagrant/docker-compose.yml"

    woo.vm.provision "shell", inline: <<-SHELL
      #!/bin/bash
      cd /home/vagrant
      sudo docker-compose up -d
    SHELL
  end


# Deploy Jenkins Master

  config.vm.define "JenkinsMaster" do |master|
    master.vm.hostname = "JenkinsMaster"
    master.vm.network "private_network", ip: "192.168.10.20"
  
    master.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 2
      vb.name = "JenkinsMaster"
    end
  
    master.vm.provision "shell", inline: <<-SHELL
      #!/bin/bash
      sudo apt-get update
      sudo -E apt install apt-transport-https ca-certificates curl software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo -E apt-key add -
      CODENAME=$(lsb_release -cs)
      sudo -E add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $CODENAME stable"
      sudo -E apt update
      sudo -E apt install docker-ce=5:20.10.24~3-0~ubuntu-$CODENAME docker-ce-cli=5:20.10.24~3-0~ubuntu-$CODENAME containerd.io docker-compose -y
      sudo usermod -a -G docker vagrant
      sudo systemctl enable docker
      sudo systemctl start docker
      docker swarm init --advertise-addr 10.0.2.15
      docker network create --driver overlay jenkins-network
      
      docker container run -d -p 5555:8080 --restart always -v jenkinsvol1:/var/jenkins_home --name Jenkins_Container jenkins/jenkins:lts
      sudo timedatectl set-timezone Europe/Paris
    SHELL
  end

# Deploy Observability Machine

config.vm.define "Observability" do |master|
  master.vm.hostname = "Observability"
  master.vm.network "private_network", ip: "192.168.10.30"

  master.vm.provider "virtualbox" do |vb|
    vb.memory = 2048
    vb.cpus = 2
    vb.name = "Observability"
  end

  master.vm.provision "shell", inline: <<-SHELL
    #!/bin/bash
    sudo apt-get update
    sudo -E apt install apt-transport-https ca-certificates curl software-properties-common -y
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo -E apt-key add -
    CODENAME=$(lsb_release -cs)
    sudo -E add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $CODENAME stable"
    sudo -E apt update
    sudo apt install openjdk-17-jdk -y
    sudo -E apt install docker-ce=5:20.10.24~3-0~ubuntu-$CODENAME docker-ce-cli=5:20.10.24~3-0~ubuntu-$CODENAME containerd.io docker-compose -y
    sudo usermod -a -G docker vagrant
    sudo systemctl enable docker
    sudo systemctl start docker
    docker swarm init --advertise-addr 10.0.2.15
    docker network create --driver overlay monitoring
  SHELL
end

end