# FastAPI App

A simple FastAPI application with Docker support.

## Features

- FastAPI web framework
- Jinja2 templating
- Docker containerization
- Docker Compose for easy deployment

## Getting Started

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

### Docker

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Access the application at http://localhost:8000

## Project Structure

```
fastapi-app/
├── templates/
│   └── index.html
├── main.py
├── requirements.txt
├── todo.json
├── docker-compose.yml
├── Dockerfile
└── README.md
```

