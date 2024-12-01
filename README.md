# Customer Feedback Analysis Microservice

## Setting Up and Running the App

**Prerequisites**

- **Docker**: Install Docker and Docker Compose on your system.

- **Python**: Install Python 3.x locally if running outside Docker. Version 3.10.12 is recommended.

### Running Locally

- Clone the Repository:
```
git clone https://github.com/iammunir/customer_feedback_analysis_microservice.git
```

- Set Up Python Virtual Environment:
```
python3 -m venv .venv
```

- Activate Virtual Environment
```
source .venv/bin/activate   # unix

venv\Scripts\activate.bat   # windows 
```

- Install Dependencies:
```
cd feedback_service
pip install -r requirements.txt
```

- Start **PostgreSQL** and **Redis** Services: Ensure PostgreSQL and Redis are running locally. Use Docker or local installations if required. Update settings.py or .env file with correct connection strings.

- Migrate and Run Django Development Server:
```
python3 manage.py migrate
python3 manage.py runserver
```

- Run Celery Worker: In a new terminal:
```
cd feedback_service
celery -A celery_task worker --loglevel=INFO
```

- Access Services on http://localhost:8000

### Running in Docker

- Clone the Repository:
```
git clone https://github.com/iammunir/customer_feedback_analysis_microservice.git
```

- Build and Start Containers, **note**: make sure port 80 is not being used by another process otherwise update the config on docker-compose.yaml file
```
docker compose up --build
```

- Run Django Migration
```
docker compose exec django python manage.py migrate
``` 

- Access Services:
    Django API direct access: http://localhost:8000
    Nginx Proxy: https://localhost

- Stopping Services:
```
docker-compose down
```

## API Documentation

**Base URL**
- Local: http://localhost:8000
- Docker: https://localhost

**Process Feedbacks**

Endpoint: POST {{base_url}}/api/v1/feedback/process/

Request Header:
- Content-Type: application/json

Request Body:
```json
[
    {
        "customer_id": 1,
        "feedback_text": "I was extremely impressed with the service I received from The Company. The technician was knowledgeable, efficient, and courteous. They explained everything clearly and answered all my questions. The issue with my [product/service] was resolved quickly and professionally. I would highly recommend this company to anyone.",
        "timestamp": "2024-11-30T12:00:00Z"
    },
    {
        "customer_id": 2,
        "feedback_text": "Unfortunately, my experience with The Company was not positive. I had to wait a long time for the technician to arrive, and when they did, they seemed rushed and uninterested in helping me. The issue with my [product/service] was not resolved, and I was left feeling frustrated and disappointed. I will not be using this company again.",
        "timestamp": "2024-11-30T12:01:00Z"
    }
]
```

Response Body
```json
{
    "message": "Feedback queued for processing. Task Id: fe0d168f-cd5d-4145-a995-3acd115782b8"
}
```

**Get Result Feedbacks**

Endpoint: GET {{base_url}}/api/v1/feedback/results/{{task_id}}

Response Body
```json
{
    "data": [
        {
            "status": "completed",
            "result": {
                "customer_id": 1,
                "feedback_text": "I was extremely impressed with the service I received from The Company. The technician was knowledgeable, efficient, and courteous. They explained everything clearly and answered all my questions. The issue with my [product/service] was resolved quickly and professionally. I would highly recommend this company to anyone.",
                "timestamp": "2024-11-30T12:00:00Z",
                "sentiment": "Positive",
                "keywords": [
                    "would highly recommend",
                    "explained everything clearly",
                    "resolved quickly",
                    "extremely impressed",
                    "technician"
                ]
            }
        },
        {
            "status": "completed",
            "result": {
                "customer_id": 2,
                "feedback_text": "Unfortunately, my experience with The Company was not positive. I had to wait a long time for the technician to arrive, and when they did, they seemed rushed and uninterested in helping me. The issue with my [product/service] was not resolved, and I was left feeling frustrated and disappointed. I will not be using this company again.",
                "timestamp": "2024-11-30T12:01:00Z",
                "sentiment": "Negative",
                "keywords": [
                    "left feeling frustrated",
                    "seemed rushed",
                    "long time",
                    "wait",
                    "using"
                ]
            }
        }
    ]
}
```

## CI/CD Pipeline

### Workflow Triggers

The CI/CD pipeline is triggered on:
- Push events to the main branch.
- Pull request events targeting the main branch.

### Stages

- **Test**

    Purpose: Ensures code quality and functionality by running tests.

    Steps:

    - Checkout code: Fetches the latest code from the repository.
    - Set up Python: Configures Python 3.10.12.
    - Install dependencies: Installs all required Python packages from requirements.txt.
    - Run tests: Executes Django unit tests located in feedback_service/tests/.

- **Build and Push Docker Image**

    Purpose: Builds and pushes the Docker image for the Django service.

    Steps:

    - Checkout code: Fetches the repository code.
    - Log in to DockerHub: Authenticates using DockerHub credentials stored in GitHub Secrets (DOCKER_USERNAME and DOCKER_PASSWORD).
    - Build and tag Docker images: Builds the Docker image for the Django service and tags it with latest.
    - Push Docker images: Pushes the tagged Docker image to DockerHub.

- **Deploy**

    Purpose: Deploys the services to the local environment for verification.

    Steps:
    - Checkout code: Fetches the repository code.
    - Pull latest Docker images: Ensures the local Docker Compose setup uses the latest images.
    - Start services: Uses Docker Compose to bring up all services.

### Extending the CI/CD Pipeline for Production

To adapt this workflow for production, we need to:

- Add a Staging Environment: Use a staging server for deployment verification. Incorporate steps to deploy to the staging environment before production.
    
- Automate Production Deployment: Add an environment-specific configuration (e.g., secrets, resource scaling). Integrate with cloud services like AWS, GCP, or Azure.
    
- Enhance Testing: Include integration and end-to-end tests.
    
- Monitoring and Alerts: Integrate with tools like Prometheus, Grafana, or ELK for real-time monitoring. Set up alerts for failures in any stage.

## Assumptions and Limitations

## Assumptions

- The application assumes that the feedback is in English.
- Request Validation is minimal. The application assumes that the body request is valid and adheres to the schema.

## Limitations

- The application does not include rate-limiting for API endpoints.
- Error messages may not be fully descriptive in case of unexpected failures.
- The CI/CD pipeline is designed for a verification and does not currently support production-level deployments.
- Logging and monitoring are minimal and not integrated with external tools like ELK or Prometheus.
