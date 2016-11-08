default: worker
worker:
	celery -A qubit.wsgiapp.queue worker -l info --workdir ./
beat:
	celery -A qubit.wsgiapp.queue beat -l info --workdir ./
