# VitiVir local setup

Clone repository

## Vagrant
### Install Vagrant:
[https://www.vagrantup.com/](https://www.vagrantup.com/)

### and VirtualBox:
[https://www.virtualbox.org/](https://www.virtualbox.org/)

### Execute the following commands:
```diff
+ vagrant box add --name vitiBox /path/to/vitiVir
+ vagrant init vitiBox
+ vagrant up
```

### Commands to access project:
```diff
+ vagrant ssh
+ cd /vagrant
```

## Virtual environment
Within the vagrant ssh

### Create and use venv:
```diff
+ mkvirtualenv venv_viti --python=python3
+ workon venv_viti
+ deactivate
```

## Backend dependencies
In vagrant ssh
Activate venv
```diff
+ cd /vagrant/vitiVir
+ pip install requirements.txt
```

## Frontend dependencies
In vagrant ssh
```diff
+ cd /vagrant/vitiVir/src/vitivir_frontend
+ npm install package.json
```
## Start MongoDB
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
In a new terminal, execute:
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ cd /vagrant/src/vitiVir_project
+ python manage.py runserver 0.0.0.0:9000
```
On your local browser, go to [http://0.0.0.0:9000/](http://0.0.0.0:9000/)

### Vue.js
In a new terminal, execute:
```diff
+ cd /path/to/vitiVir
+ vagrant ssh
+ cd /vagrant/src/vitivir_frontend
+ npm run serve
```
On your local browser, go to  [http://0.0.0.0:8080/landing](http://0.0.0.0:8080/landing)
