default: worker
worker:
	celery -A qubit.wsgiapp.queue worker -l info --workdir ./ -B
beat:
	celery -A qubit.wsgiapp.queue beat -l info --workdir ./
upload:
	python3 setup.py sdist --formats=gztar register upload

