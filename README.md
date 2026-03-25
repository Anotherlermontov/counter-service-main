# Main Counter Service
The Main Counter Service is a separate Django-based service responsible for handling HTTP requests, reading the current counter value from the blockchain, storing the private key in PostgreSQL, signing transactions, and broadcasting them to the network.

### Responsibilities
- handle `GET /value`
- handle `POST /increment`
- read the current value from the `Counter` smart contract
- request transaction parameters from the Tx Builder Service
- load the wallet private key from PostgreSQL
- sign and send transactions to the blockchain

### Setup project with docker
1. make build
2. make up
3. make migrate

### Setup project local:
1. Create and activate venv python 3.11
2. Install pip-tools `pip install pip-tools`
3. Install requirements `make install-dev`
4. Run migrations `python manage.py migrate`
5. Run project `python manage.py runserver`

### Install pre-commit hook
1. Activate venv
2. Init hook `pre-commit install`
