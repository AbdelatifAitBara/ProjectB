Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
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
      sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
      sudo apt-get update
      sudo apt-get install docker-ce docker-ce-cli containerd.io -y
      sudo systemctl enable docker
      sudo systemctl start docker
      sudo usermod -aG docker vagrant
      cp /vagrant/docker-compose.yml /home/vagrant/docker-compose.yml
      docker-compose up -d
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
      sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
      sudo apt-get update
      sudo apt-get install docker-ce docker-ce-cli containerd.io -y
      sudo systemctl enable docker
      sudo systemctl start docker
      sudo usermod -aG docker vagrant
    SHELL
  end
end