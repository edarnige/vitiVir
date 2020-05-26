# VitiVir local setup

Clone repository

## Vagrant
### Install Vagrant:
[https://www.vagrantup.com/](https://www.vagrantup.com/)

### and VirtualBox:
[https://www.virtualbox.org/](https://www.virtualbox.org/)

### Execute the following command:
```diff
+ vagrant up
```

### Commands to access project:
```diff
+ vagrant ssh
+ cd /vagrant
```

## Virtual environment
Within the vagrant ssh

### Create venv:
```diff
+ mkvirtualenv venv_viti --python=python3
```

### Use venv:
```diff
+ workon venv_viti
+ deactivate
```

## Backend dependencies
In vagrant ssh
Activate venv
```diff
+ cd /vagrant
+ pip install -r requirements.txt
```

## Frontend dependencies
Within the vagrant ssh
In Vagrant, locking isn't supported when syncing files, so npm install fails without symlinking node_modules outside of the synced folder. The name of this directory MUST be node_modules. See [here]( http://perrymitchell.net/article/npm-symlinks-through-vagrant-windows/) for more information. 
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ mkdir ~/node_modules
+ cd /vagrant/src/vitivir_frontend
+ rm -rf node_modules package-lock.json
+ sudo npm cache clean -f
+ ln -s ~/node_modules node_modules
+ npm init
[enter, enter, enter...]
+ npm install
```
If symlinks are not functioning, enable them manually in Vagrany by:\
1. On the host machine: 
Windows ```cd C:\Program Files\Oracle\VirtualBox```
MacOS ```cd /Users/username/VirtualBox\ VMs```

2. Run the following command:
```VBoxManage setextradata VM_NAME VBoxInternal2/SharedFoldersEnableSymlinksCreate/SHARE_NAME 1```
replacing VM_NAME with your Virtual Machine's name (if you don't know this, in VBox go to Machine > Settings > General > Basic > Name --- also replace SHARE_NAME with the name of your shared folder, if you don't remember this, go to Machine > Settings > Shared Folders. 
verify with: 
```VBoxManage getextradata "<vm name>" enumerate```

3. Restart your VM AND VirtualBox, run as administrator


## Start MongoDB
First time setup\
In a new terminal, execute:
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ sudo mkdir /data
+ cd data
+ sudo mkdir /db
+ sudo chmod 777 /data/db
```

Start mongod\
In a new terminal, execute:
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ mongod
```

Mongo shell\
In a new terminal, execute:
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ mongo
```

## Running the servers
### Django
First time setup - migrate db and create superuser
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ cd /vagrant/src/vitiVir_project
+ python manage.py makemigrations
+ python manage.py migrate
+ pyton manage.py createsuperuser
```

Run server
In a new terminal with the venv activated, execute:
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ cd /vagrant/src/vitiVir_project
+ python manage.py runserver 0.0.0.0:9000
```
On your local browser, go to [http://0.0.0.0:9000/](http://0.0.0.0:9000/)

urls:
/admin/
/api/data/entries/
/api/data/entries_csv/
/users/

### Vue.js
In a new terminal with the venv activated, execute:
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ cd /vagrant/src/vitivir_frontend
+ npm run serve
```
On your local browser, go to  [http://0.0.0.0:8080/landing](http://0.0.0.0:8080/landing)

