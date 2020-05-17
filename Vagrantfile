# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "bento/ubuntu-18.04"
  config.vm.hostname = "vitiBox"

  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 8080, host: 8080 #Vue frontend
  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 27017, host: 27017 #MongoDB
  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 9000, host: 9000 #Django backend

  # Allow symlinks for npm install to work
  config.vm.provider :virtualbox do |vm| 
    vm.customize["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/vagrant", "1"]
  end
  
  config.vm.provision "shell", inline: <<-SHELL
    
  # Update and upgrade the server packages
    sudo apt-get update
    sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
    # Set Ubuntu Language
    sudo locale-gen en_GB.UTF-8
    # Install Python, SQLite and pip
    sudo apt-get install -y python3-dev sqlite python-pip
    # Upgrade pip to the latest version.
    sudo pip install --upgrade pip
    # Install and configure python virtualenvwrapper.
    sudo pip install virtualenvwrapper
    if ! grep -q VIRTUALENV_ALREADY_ADDED /home/vagrant/.bashrc; then
        echo "# VIRTUALENV_ALREADY_ADDED" >> /home/vagrant/.bashrc
        echo "WORKON_HOME=~/.virtualenvs" >> /home/vagrant/.bashrc
        echo "PROJECT_HOME=/vagrant" >> /home/vagrant/.bashrc
        echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
    fi
    
    # Packages
    MONGO="mongodb-org"
    # MongoDB shell v4.2.5
    MONGO_INSTALLED=$(dpkg-query -W --showformat='${Status}\n' $MONGO | grep "install ok installed")
    echo "Checking for $MONGO: $MONGO_INSTALLED"
    if [ "" == "$MONGO_INSTALLED" ]; then
      sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 4B7C549A058F8B6B
      echo "deb http://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
      sudo apt-get update
      sudo apt-get install -y mongodb-org
    fi

    # Node v10.20.0, npm v6.14.4, Vue CLI v4.3.1
    sudo apt-get install curl
    curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash - #12
    sudo apt-get install -y nodejs
    sudo npm install -g @vue/cli@4.2.2 


  SHELL

end