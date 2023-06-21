[![Build Status](https://app.travis-ci.com/Fhockk/WorkerAPI.svg?token=EEVwf1MVsF8FEmpkxpRC&branch=master)](https://app.travis-ci.com/Fhockk/WorkerAPI)

## About
- It is a test project.

- The purpose of the project is to demonstrate my skills and knowledge of the back-end development processes.

## Technical Requirements
- Use PEP8 for your Python code
- Python 3
- Flask
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis, Celery, RabbitMQ
- Docker

# Installation:

## Clone the repo

```shell
git clone https://github.com/Fhockk/WorkerAPI.git
```

## How to run this project?
- Make sure you have docker installed
- Open the terminal and hit the following command :

Change the directory:
```shell
cd WorkerAPI/
```

## Create the .env file like .env.example with ur value to:

- SECRET_KEY = (your value)
- JWT_SECRET_KEY= (your value)

## Run the docker build (development server)
```shell
docker-compose up --build
```

## Tests:
```shell
docker exec workerapi-web-1 python -m pytest
```

- Online service will be available at the address: http://127.0.0.1:5000/.
- API will be available at the address http://127.0.0.1:5000/api/v1/.
- Detailed specifications you can find below:

| Endpoint                     | CRUD Method | JSON Parameters                                                                                                                                                  | Result                                                                       |
|------------------------------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| `/api/v1/auth/regiser/`      | POST        | `{ "email":"example@test.com", "password":"testpass", "first_name":"Test", "last_name": "Test", "gender_id": (1-3)}`                                             | Creates user account. *Allow Any.                                            |
| `/api/v1/auth/login/`        | POST        | `{ "email": "example@test.com", "password": "testpass" }`                                                                                                        | Get access token. Allow Any. Usage with Bearer.                              |
| `/api/v1/users/`             | GET         | N/A                                                                                                                                                              | Get all users. *Only Manager.                                                |
| `/api/v1/users/<id>/`        | GET         | N/A                                                                                                                                                              | Get user information by id. *Allow Any.                                      |   
| `/api/v1/users/<id>/`        | PATCH       | `{ "email":"example@test.com", "password":"testpass", "first_name":"Test", "last_name": "Test", "gender_id": (1-3)}`                                             | Update user information. *Allow Any.                                         |
| `/api/v1/users/<id>/`        | DELETE      | N/A                                                                                                                                                              | Delete user information. *Only Manager.                                      |
| `/api/v1/workers/`           | GET         | N/A                                                                                                                                                              | Get all workers. *Allow Any.                                                 |
| `/api/v1/workers/<id>/`      | GET         | N/A                                                                                                                                                              | Get worker information by id. *Allow Any.                                    |
| `/api/v1/workers/`           | POST        | `{ "email":"example@test.com", "first_name":"Test", "last_name": "Test", "gender_id": (1-3), "specialty_id": (1-3)}`                                             | Create worker account. *Only Manager.                                        |
| `/api/v1/workers/<id>/`      | PATCH       | `{ "email":"example@test.com", "first_name":"Test", "last_name": "Test", "gender_id": (1-3), "specialty_id": (1-3)}`                                             | Update worker account information. *Only Manager.                            |
| `/api/v1/workers/<id>/`      | DELETE      | N/A                                                                                                                                                              | Delete worker account information. *Only Manager.                            |
| `/api/v1/schedules/`         | GET         | N/A                                                                                                                                                              | Get all worker schedules. *Allow Any.                                        |
| `/api/v1/employees/<id>/`    | GET         | N/A                                                                                                                                                              | Get schedule by id. Allow Any.                                               |
| `/api/v1/employees/`         | POST        | `{"year": "2023", "month": 1, "day": 1, "start_time_h": 10, "start_time_m": 0, "end_time_h": 19, "end_time_m": 0, "worker_id": worker.id, "location_id": (1-3)}` | Create schedule to worker. *Only Manager.                                    |
| `/api/v1/employees/<id>/`    | PATCH       | `{"year": "2023", "month": 1, "day": 1, "start_time_h": 10, "start_time_m": 0, "end_time_h": 19, "end_time_m": 0, "worker_id": worker.id, "location_id": (1-3)}` | Update worker schedule information. *Only Manager.                           |
| `/api/v1/employees/<id>/`    | DELETE      | N/A                                                                                                                                                              | Delete worker schedule information. *Only Manager.                           |
| `/api/v1/appointments/<id>/` | GET         | N/A                                                                                                                                                              | Get appointment information by his ID. *Allow Any.                           |
| `/api/v1/appointments/`      | POST        | `{"year": "2023", "month": 1, "day": 1, "start_time_h": 11, "start_time_m": 0, "end_time_h": 12, "end_time_m": 0, "worker_id": worker.id, "user_id": user.id}`   | Create appointment between user and doctor. If schedule exists. *Only Admin. |
| `/api/v1/appointments/<id>/` | PATCH       | `{"year": "2023", "month": 1, "day": 1, "start_time_h": 10, "start_time_m": 0, "end_time_h": 19, "end_time_m": 0, "worker_id": worker.id, "user_id": user.id}`   | Update appointment between user and doctor. *Only Admin.                     |
| `/api/v1/appointments/<id>/` | DELETE      | N/A                                                                                                                                                              | Make appointment status_id=3 (cancelled). *Only Admin.                       |
