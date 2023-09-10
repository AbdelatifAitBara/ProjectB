Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04"
  config.vm.box_check_update = false
  config.vm.box_download_insecure = false
  config.ssh.insert_key = true

  config.vm.define "Production" do |woo|
    woo.vm.hostname = "Production"
    woo.vm.network "private_network", ip: "192.168.10.10"

    woo.vm.provider "virtualbox" do |vb|
      vb.memory = 5552
      vb.cpus = 2
      vb.name = "Production"
    end

    woo.vm.provision "shell", inline: <<-SHELL
      #!/bin/bash
      sudo apt update
      sudo apt-get install ufw -y
      sudo ufw enable
      sudo ufw default deny incoming
      sudo ufw default allow outgoing
      sudo ufw allow 80
      sudo ufw allow 443
      sudo ufw allow 22
      sudo ufw allow 8888
      sudo ufw allow 3306
      sudo ufw allow 8081
      sudo ufw allow 6379
      sudo ufw allow 9100
      sudo ufw allow 7070
      sudo ufw allow 8080
      sudo ufw allow 9090
      sudo -E apt install apt-transport-https ca-certificates curl software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo -E apt-key add -
      CODENAME=$(lsb_release -cs)
      sudo -E add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $CODENAME stable"
      sudo -E apt update
      sudo -E apt install docker-ce=5:20.10.24~3-0~ubuntu-$CODENAME docker-ce-cli=5:20.10.24~3-0~ubuntu-$CODENAME containerd.io docker-compose -y
      sudo usermod -aG docker vagrant
      docker network create -d bridge production-network
      sudo useradd -m -d /home/jenkins -G docker jenkins
      sudo systemctl enable docker
      sudo systemctl start docker
      sudo chown $USER:docker /var/run/docker.sock
      mkdir /home/vagrant/production-compose
      cp /vagrant/production-compose/docker-compose.yml /home/vagrant/production-compose
      docker network create production-network
      docker-compose -f /home/vagrant/production-compose/docker-compose.yml up -d
      sudo apt install openjdk-17-jdk -y
      sudo apt install python3-pip -y
      pip install -U mock
      pip install nose
      sudo timedatectl set-timezone Europe/Paris
      sudo touch /etc/cloud/cloud-init.disabled
    SHELL
  end

  # Deploy Jenkins Master

  config.vm.define "JenkinsMaster" do |master|
    master.vm.hostname = "JenkinsMaster"
    master.vm.network "private_network", ip: "192.168.10.20"

    master.vm.provider "virtualbox" do |vb|
      vb.memory = 3048
      vb.cpus = 2
      vb.name = "JenkinsMaster"
    end

    master.vm.provision "shell", inline: <<-SHELL
      #!/bin/bash
      sudo apt-get update
      sudo apt-get install ufw -y
      sudo ufw enable
      sudo ufw default deny incoming
      sudo ufw default allow outgoing
      sudo ufw allow 80
      sudo ufw allow 443
      sudo ufw allow 22
      sudo ufw allow 5555
      sudo ufw allow 8081
      sudo ufw allow 9100
      sudo ufw allow 6379
      sudo -E apt install apt-transport-https ca-certificates curl software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo -E apt-key add -
      CODENAME=$(lsb_release -cs)
      sudo -E add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $CODENAME stable"
      sudo -E apt update
      sudo -E apt install docker-ce=5:20.10.24~3-0~ubuntu-$CODENAME docker-ce-cli=5:20.10.24~3-0~ubuntu-$CODENAME containerd.io docker-compose -y
      sudo usermod -a -G docker vagrant
      sudo chown $USER:docker /var/run/docker.sock
      sudo systemctl enable docker
      sudo systemctl start docker
      mkdir /home/vagrant/jenkins-compose
      docker network create jenkins-network
      cp /vagrant/jenkins-compose/docker-compose.yml /home/vagrant/jenkins-compose
      docker-compose -f /home/vagrant/jenkins-compose/docker-compose.yml up -d
      sudo touch /etc/cloud/cloud-init.disabled
    SHELL
  end

  # Deploy Observability Machine

  config.vm.define "Observability" do |observa|
    observa.vm.hostname = "Observability"
    observa.vm.network "private_network", ip: "192.168.10.30"
  
    observa.vm.provider "virtualbox" do |vb|
      vb.memory = 5552
      vb.cpus = 2
      vb.name = "Observability"
    end
  
    observa.vm.provision "shell", inline: <<-SHELL
      #!/bin/bash
      sudo apt-get update
      sudo apt-get install ufw -y
      sudo ufw enable
      sudo ufw default deny incoming
      sudo ufw default allow outgoing
      sudo ufw allow 80
      sudo ufw allow 443
      sudo ufw allow 22
      sudo ufw allow 3000
      sudo ufw allow 9090
      sudo ufw allow 1010
      sudo ufw allow 8081
      sudo ufw allow 9100
      sudo ufw allow 6379
      sudo -E apt install apt-transport-https ca-certificates curl software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo -E apt-key add -
      CODENAME=$(lsb_release -cs)
      sudo -E add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $CODENAME stable"
      sudo -E apt update
      sudo apt install openjdk-17-jdk -y
      sudo -E apt install docker-ce=5:20.10.24~3-0~ubuntu-$CODENAME docker-ce-cli=5:20.10.24~3-0~ubuntu-$CODENAME containerd.io docker-compose -y
      sudo usermod -a -G docker vagrant
      sudo chown $USER:docker /var/run/docker.sock
      sudo systemctl enable docker
      sudo systemctl start docker
      mkdir -p promgrafnode/prometheus && mkdir -p promgrafnode/grafana/provisioning &&  touch promgrafnode/docker-compose.yml &&  touch promgrafnode/prometheus/prometheus.yml
      cp /vagrant/observability-compose/docker-compose.yml /home/vagrant/promgrafnode/docker-compose.yml
      cp /vagrant/observability-compose/prometheus/prometheus.yml /home/vagrant/promgrafnode/prometheus/prometheus.yml
      docker network create observability-network
      docker-compose -f /home/vagrant/promgrafnode/docker-compose.yml up -d
      sudo touch /etc/cloud/cloud-init.disabled
    SHELL
  end


    # HAPROXY

    config.vm.define "HAPROXY" do |haproxy|
      haproxy.vm.hostname = "HAPROXY"
      haproxy.vm.network "private_network", ip: "192.168.10.40"
      

      haproxy.vm.provider "virtualbox" do |vb|
        vb.memory = 2048
        vb.cpus = 2
        vb.name = "HAPROXY"
      end
    
      haproxy.vm.provision "shell", inline: <<-SHELL
        #!/bin/bash
        sudo apt-get update
        sudo apt-get install ufw -y
        sudo ufw enable
        sudo ufw default deny incoming
        sudo ufw default allow outgoing
        sudo ufw allow 80
        sudo ufw allow 443
        sudo ufw allow 22
        sudo -E apt install apt-transport-https ca-certificates curl software-properties-common -y
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo -E apt-key add -
        CODENAME=$(lsb_release -cs)
        sudo -E add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $CODENAME stable"
        sudo -E apt update
        sudo -E apt install docker-ce=5:20.10.24~3-0~ubuntu-$CODENAME docker-ce-cli=5:20.10.24~3-0~ubuntu-$CODENAME containerd.io docker-compose -y
        sudo usermod -a -G docker vagrant
        sudo chown $USER:docker /var/run/docker.sock
        sudo systemctl enable docker
        sudo systemctl start docker
        mkdir -p /home/vagrant/haproxy-compose
        cp /vagrant/haproxy-compose/docker-compose.yml /home/vagrant/haproxy-compose/docker-compose.yml
        docker network create haproxy
        docker-compose -f /home/vagrant/haproxy-compose/docker-compose.yml up -d
        mkdir ssl
        cp /vagrant/ssl_generate.sh /home/vagrant/ssl
        sudo sudo apt-get install dos2unix
        sudo dos2unix /home/vagrant/ssl/ssl_generate.sh
        sudo chmod +x /home/vagrant/ssl/ssl_generate.sh
        sudo bash /home/vagrant/ssl/ssl_generate.sh haproxy
        sudo apt install haproxy -y
        sudo cp /vagrant/haproxy_micro.cfg /etc/haproxy/haproxy.cfg
        cp /vagrant/haproxy /etc/default/haproxy
        sudo systemctl enable haproxy
        sudo systemctl restart haproxy
        sudo touch /etc/cloud/cloud-init.disabled
      SHELL
    end

end