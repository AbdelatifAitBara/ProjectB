Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04"
  config.vm.box_check_update = false
  config.vm.box_download_insecure = false
  config.ssh.insert_key = true

  config.vm.define "WooCommerce" do |master|
    master.vm.hostname = "WooCommerce"
    master.vm.network "private_network", ip: "192.168.10.10"

    master.vm.provider "virtualbox" do |vb|
      vb.memory = 2096
      vb.cpus = 2
      vb.name = "WooCommerce"
    end

    master.vm.provision "shell", inline: <<-SHELL
      #!/bin/bash
      sudo -E apt-get update
      sudo -E apt install apt-transport-https ca-certificates curl software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo -E apt-key add -
      CODENAME=$(lsb_release -cs)
      sudo -E add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $CODENAME stable"
      sudo -E apt update
      sudo -E apt install docker-ce=5:20.10.24~3-0~ubuntu-$CODENAME docker-ce-cli=5:20.10.24~3-0~ubuntu-$CODENAME containerd.io -y
      sudo usermod -a -G docker vagrant
      sudo systemctl enable docker
      sudo systemctl start docker
      ssh-keyscan github.com >> ~/.ssh/known_hosts

      docker-compose up -d
    SHELL

    master.vm.provision "file", source: "docker-compose.yml", destination: "/home/vagrant/docker-compose.yml"
  end

  s
  # Deploy Jenkins Master:

  config.vm.define "JenkinsMaster" do |master|
    master.vm.hostname = "JenkinsMaster"
    master.vm.network "private_network", ip: "192.168.10.20"

    master.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 2
      vb.name = "JenkinsMaster"
    end

    master.vm.provision "shell", inline: <<-SHELL
      sudo apt-get update
      sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
      sudo apt update
      sudo apt install docker-ce docker-ce-cli containerd.io docker-compose -y
      sudo usermod -a -G docker vagrant
      sudo systemctl enable docker
      sudo systemctl start docker
      docker container run -d -p 5555:8080 --restart always -v jenkinsvol1:/var/jenkins_home --name Jenkins_Container jenkins/jenkins:lts
    SHELL
  end


  # Deploy The Docker Machine as a Jenkins Agent ( Will Contains The Microservice ):

  config.vm.define "Microservice" do |agent|
    agent.vm.hostname = "Microservice"
    agent.vm.network "private_network", ip: "192.168.10.30"

    agent.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 2
      vb.name = "Microservice"
    end

    agent.vm.provision "shell", inline: <<-SHELL
      sudo apt-get update
      sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
      sudo apt update
      sudo apt install openjdk-17-jdk -y
      sudo apt install docker-ce docker-ce-cli containerd.io docker-compose -y
      sudo usermod -a -G docker vagrant
    SHELL
  end
end