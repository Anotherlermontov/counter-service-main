lock:
	pip-compile --generate-hashes --no-emit-index-url --allow-unsafe
	pip-compile --generate-hashes --no-emit-index-url requirements_dev.in

install-dev:
	pip-sync requirements.txt requirements_dev.txt --pip-args '--no-deps'
