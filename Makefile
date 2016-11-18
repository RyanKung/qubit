default: all
all:
	celery -A qubit.wsgiapp.queue worker -l info --workdir ./ -E -c 100 -B
worker:
	celery -A qubit.wsgiapp.queue worker -l info --workdir ./ -E -c 100
beat:
	celery -A qubit.wsgiapp.queue beat -l error --workdir ./
purge:
	celery -A qubit.wsgiapp.queue purge -f --workdir ./
upload:
	python3 setup.py sdist --formats=gztar register upload

