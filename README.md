# Claim Process Service

This repository contains the Claim Process service that processes claims, handles the data and logic for claim submission. The service is built with **FastAPI** and follows modern development practices using Docker for containerization and **pytest** for unit testing.

## Running the Application

To get started with the project, you'll need Docker and Docker Compose installed. The application runs in containers, and the following commands can help you manage the development environment.

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/)
- Python 3.10 or above (for development and debugging)

### Start the Services

To start the containers, run the following command:

```bash
make up
```

This will start all necessary containers in detached mode (in the background).

### Running Unit Tests

To run the unit tests for the `claim_process` service, use the following command:

```bash
make test
```

To run tests for a specific file, specify the file path as an argument:

```bash
make test file=tests/test_claim.py
```

### Debugging with `ipdb`

To debug the service with `ipdb`, insert breakpoints where you want to inspect the code:

```bash
import ipdb; ipdb.set_trace()
```

And then execute the tests with: `make test`.
