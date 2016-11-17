default: worker
worker:
	celery -A qubit.wsgiapp.queue worker -l info --workdir ./ -E -c 1
beat:
	celery -A qubit.wsgiapp.queue beat -l error --workdir ./
upload:
	python3 setup.py sdist --formats=gztar register upload

