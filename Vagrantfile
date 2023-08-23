Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04"
  config.vm.box_check_update = false
  config.vm.box_download_insecure = false
  config.ssh.insert_key = true

  config.vm.define "WooCommerce" do |master|
    master.vm.hostname = "WooCommerce"
    master.vm.network "private_network", ip: "192.168.10.10"

    master.vm.provider "virtualbox" do |vb|
      vb.memory = 3096
      vb.cpus = 2
      vb.name = "WooCommerce"
    end

    master.vm.provision "shell", inline: <<-SHELL
      sudo apt-get update
      sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
      sudo apt update
      sudo apt install docker-ce=5:20.10.24~3-0~ubuntu-$(lsb_release -cs) docker-ce-cli=5:20.10.24~3-0~ubuntu-$(lsb_release -cs) containerd.io docker-compose -y
      sudo usermod -a -G docker vagrant
      sudo systemctl enable docker
      sudo systemctl start docker
      sudo usermod -aG docker vagrant
      git clone https://github.com/AbdelatifAitBara/ProjectB
      cd ProjectB
      docker-compose up -d
      rm -drf /home/vagrant/ProjectB
    SHELL
  end

  config.vm.define "AddProducts" do |master|
    master.vm.hostname = "AddProducts"
    master.vm.network "private_network", ip: "192.168.10.20"

    master.vm.provider "virtualbox" do |vb|
      vb.memory = 2096
      vb.cpus = 2
      vb.name = "AddProducts"
    end

    master.vm.provision "shell", inline: <<-SHELL
      sudo apt-get update
      sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
      sudo apt update
      sudo apt install docker-ce=5:20.10.24~3-0~ubuntu-$(lsb_release -cs) docker-ce-cli=5:20.10.24~3-0~ubuntu-$(lsb_release -cs) containerd.io docker-compose -y
      sudo usermod -a -G docker vagrant
      sudo systemctl enable docker
      sudo systemctl start docker
      git clone https://github.com/AbdelatifAitBara/ProjectB
      cd ProjectB
      docker build -t addproducts .
      docker run -p 8080:8080 addproducts
      rm -drf /home/vagrant/ProjectB
    SHELL
  end
end