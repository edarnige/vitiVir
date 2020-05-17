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


## Start MongoDB
First time setup
In a new terminal, execute:
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ mkdir data
+ cd data
+ mkdir db
+ chmod 777 /data/db
```

Start mongod
In a new terminal, execute:
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ mongod
```

Mongo shell 
In a new terminal, execute:
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ mongo
```

## Running the servers
### Django
First time setup - migrate db
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ cd /vagrant/src/vitiVir_project
+ python manage.py makemigrations
+ python manage.py migrate
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

