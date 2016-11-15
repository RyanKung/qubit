default: worker
worker:
	celery -A qubit.wsgiapp.queue worker -l info --workdir ./ -E -c 5
beat:
	celery -A qubit.wsgiapp.queue beat -l info --workdir ./
upload:
	python3 setup.py sdist --formats=gztar register upload

