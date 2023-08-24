# e-grocery-api

REST API for e-grocery service.

### Capabilities:
 - **Create** valid couriers, items, orders, regions, shifts.
 - **Add** a shift to a courier.
 - **Assign** an order based on courier type, courier workload, delivery region.
 - **Complete** an order idempotently.
 - **Сalculate** courier's rating and earnings.

### Strengths:
 - **Maintainable**, **testable** and **(re)usable**. The project is divided by responsibilities: **crud** (database operation), **logic** (business logic) and **api** (presentation).
 - **Readable**. The project is easy to understand thanks to self-documenting code, type hints, docstrings, and interactive API documentation.
 - **Asynchronous**. Fast, non-blocking work thanks to gunicorn with uvicorn workers.

## How to run
Clone the repository. Rename *.env.example* to *.env* and fill in the environment variables.

To run the project in Docker:
```
$ docker-compose up
```

## How to use
After launching, you can send requests. At http://localhost/docs you can find interactive API docs by SwaggerUI. If you want to play around with the API, you can send a request from interactive docs or use other tools like curl, httpie, Postman, etc.

## Testing
To setup a test environment:
```
$ python3.10 -m venv venv
$ . venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.dev.txt
```
To bring up a test database:
```
$ docker-compose --file docker-compose.dev.yml up
```
To run all tests:
```
$ pytest
```

## Contributing
This project made for educational purposes and not intended for production use, but feel free to use Github Issues if you want to report bug, suggest improvements or anything else.
