MANAGE = docker run --env-file=.env turkey_web python /usr/src/app/turkey/manage.py 

all: install-all collect-static migrate run-server

install-docker:
	wget -qO- https://get.docker.com/ | sh
	apt-get -y install python-pip
	pip install docker-compose
install-site:
	docker-compose build
install-all: install-docker install-site
run-server:
	docker-compose up
install-and-run: install-all run-server
collect-static:
	$(MANAGE) collectstatic --noinput
migrate:
	$(MANAGE) migrate
new-super-user:
	$(MANAGE) createsuperuser
