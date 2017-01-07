default: all

all:
	celery -A qubit.wsgiapp.queue worker -l info --workdir ./ -E -c 1 -B -l error
debug:
	celery -A qubit.wsgiapp.queue worker -l info --workdir ./ -E -c 1 -B -l info
worker:
	celery -A qubit.wsgiapp.queue worker -l info --workdir ./ -E -c 10
beat:
	celery -A qubit.wsgiapp.queue beat -l error --workdir ./
purge:
	celery -A qubit.wsgiapp.queue purge -f --workdir ./
upload:
	python3 setup.py sdist --formats=gztar register upload
run:
	pwsgi -a qubit -m qubit -w . -b 127.0.0.1:8060

