# SimpleAPI - AWS Lambda CRUD API with DynamoDB

A serverless REST API built with AWS Lambda and DynamoDB using Python 3.13. This project follows **Hexagonal Architecture** principles, providing a well-structured, maintainable, and testable codebase.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Local Development](#local-development)
  - [Using Docker](#using-docker)
  - [Using SAM CLI](#using-sam-cli)
- [Deployment to AWS](#deployment-to-aws)
- [Testing the API](#testing-the-api)

---

## 🎯 Project Overview

SimpleAPI is a serverless CRUD (Create, Read, Update, Delete) API for managing "Items". Each item consists of:

| Field  | Type   | Description       |
| ------ | ------ | ----------------- |
| `id`   | string | Unique identifier |
| `name` | string | Name of the item  |

### Technology Stack

- **Runtime**: Python 3.13
- **Infrastructure**: AWS SAM (Serverless Application Model)
- **Database**: AWS DynamoDB
- **Validation**: Pydantic
- **AWS SDK**: boto3

---

## 🏗️ Architecture

This project implements **Hexagonal Architecture** with four distinct layers:

```
┌─────────────────────────────────────────────────────────────┐
│                      PRESENTATION                           │
│  (Lambda Handlers: get, post, update, delete, get_by_id)   │
├─────────────────────────────────────────────────────────────┤
│                       APPLICATION                           │
│              (Use Cases: Business Logic)                    │
├─────────────────────────────────────────────────────────────┤
│                         DOMAIN                              │
│          (Entities, Ports, Exceptions)                      │
├─────────────────────────────────────────────────────────────┤
│                     INFRASTRUCTURE                          │
│         (DynamoDB Repository, Mappers)                      │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer              | Purpose                                          |
| ------------------ | ------------------------------------------------ |
| **Presentation**   | Lambda handlers - HTTP request/response handling |
| **Application**    | Use cases - Business logic orchestration         |
| **Domain**         | Entities, ports (interfaces), exceptions         |
| **Infrastructure** | Database repositories and mappers                |

---

## 🔌 API Endpoints

| Method | Endpoint      | Description       | Request Body           |
| ------ | ------------- | ----------------- | ---------------------- |
| GET    | `/items`      | Get all items     | -                      |
| GET    | `/items/{id}` | Get item by ID    | -                      |
| POST   | `/items`      | Create a new item | `{ "name": "string" }` |
| PUT    | `/items/{id}` | Update an item    | `{ "name": "string" }` |
| DELETE | `/items/{id}` | Delete an item    | -                      |

---

## 📁 Project Structure

```
SimpleAPI/
├── src/
│   ├── __init__.py
│   ├── requirements.txt          # Lambda dependencies (pydantic)
│   └── features/
│       └── items/
│           ├── presentation/     # Lambda handlers
│           │   ├── get_handler.py
│           │   ├── get_by_id_handler.py
│           │   ├── post_handler.py
│           │   ├── update_handler.py
│           │   └── delete_handler.py
│           ├── application/      # Use cases
│           │   └── use_cases/
│           │       ├── get_all_items_use_case.py
│           │       ├── get_item_by_id_use_case.py
│           │       ├── create_item_use_case.py
│           │       ├── update_item_use_case.py
│           │       └── delete_item_use_case.py
│           ├── domain/           # Core business logic
│           │   ├── entities/
│           │   │   └── item.py
│           │   ├── ports/
│           │   └── exceptions/
│           └── infrastructure/   # External services
│               ├── repositories/
│               │   └── dynamodb_item_repository.py
│               └── mappers/
├── template.yaml                 # SAM template
├── samconfig.toml               # SAM configuration
├── requirements.txt             # Development dependencies
├── Dockerfile                   # Local development container
├── .env.template                # Environment variables template
└── .gitignore
```

---

## 🔧 Environment Variables

| Variable      | Description                   | Required |
| ------------- | ----------------------------- | -------- |
| `ITEMS_TABLE` | DynamoDB table name for items | Yes      |

### Setup

1. Copy the template file:

   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and add your values:
   ```
   ITEMS_TABLE=your-dynamodb-table-name
   ```

> **Note**: When deployed with SAM, the `ITEMS_TABLE` environment variable is automatically set by the CloudFormation template.

---

## 💻 Local Development

### Prerequisites

- [Python 3.13](https://www.python.org/downloads/)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [Docker](https://www.docker.com/products/docker-desktop/) (for local Lambda emulation)
- [AWS CLI](https://aws.amazon.com/cli/) (configured with credentials)

### Install Development Dependencies

```bash
pip install -r requirements.txt
```

### Using Docker

Build the Docker image:

```bash
docker build -t simple-api .
```

Run a specific handler (example: GetItems):

```bash
docker run --rm -p 9000:8080 simple-api
```

Invoke the function locally:

```bash
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"httpMethod": "GET", "path": "/items"}'
```

### Using SAM CLI

Start the local API:

```bash
sam build
sam local start-api
```

This starts a local API Gateway at `http://127.0.0.1:3000`.

Test the endpoints:

```bash
# Get all items
curl http://127.0.0.1:3000/items

# Create an item
curl -X POST http://127.0.0.1:3000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "My Item"}'

# Get item by ID
curl http://127.0.0.1:3000/items/{id}

# Update an item
curl -X PUT http://127.0.0.1:3000/items/{id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item"}'

# Delete an item
curl -X DELETE http://127.0.0.1:3000/items/{id}
```

> **Note**: Local testing requires Docker to emulate the Lambda environment and DynamoDB Local or a connection to a real DynamoDB table.

---

## 🚀 Deployment to AWS

### Prerequisites

1. **AWS CLI configured** with appropriate credentials:

   ```bash
   aws configure
   ```

2. **SAM CLI installed** ([Installation Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html))

### Step 1: Build the Application

```bash
sam build
```

This packages your Lambda functions and resolves dependencies.

### Step 2: Deploy to AWS

**First-time deployment (guided):**

```bash
sam deploy --guided
```

You will be prompted for:

- **Stack Name**: `SimpleApi` (or your preferred name)
- **AWS Region**: `us-east-1` (or your preferred region)
- **Confirm changes before deploy**: Yes
- **Allow SAM CLI IAM role creation**: Yes
- **Save arguments to samconfig.toml**: Yes

**Subsequent deployments:**

```bash
sam deploy
```

This uses the saved configuration in `samconfig.toml`.

### Step 3: Get the API Endpoint

After deployment, SAM outputs the API Gateway URL:

```
Outputs
-----------------------------------------------------------
Key                 ApiEndpoint
Description         API Gateway endpoint URL
Value               https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/Prod/
-----------------------------------------------------------
```

### Deployment Configuration (samconfig.toml)

```toml
[default.deploy.parameters]
stack_name = "SimpleApi"
resolve_s3 = true
s3_prefix = "SimpleApi"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"

[default.global.parameters]
region = "us-east-1"
```

---

## 🧪 Testing the API

Once deployed, test your API with curl or any HTTP client:

```bash
# Replace with your actual API Gateway URL
API_URL="https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/Prod"

# Create an item
curl -X POST "$API_URL/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item"}'

# Get all items
curl "$API_URL/items"

# Get item by ID (replace {id} with actual ID)
curl "$API_URL/items/{id}"

# Update an item
curl -X PUT "$API_URL/items/{id}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'

# Delete an item
curl -X DELETE "$API_URL/items/{id}"
```

---

## 📚 AWS Resources Created

The SAM template creates the following AWS resources:

| Resource    | Type                      | Description                   |
| ----------- | ------------------------- | ----------------------------- |
| Api         | AWS::Serverless::Api      | API Gateway REST API          |
| GetItems    | AWS::Serverless::Function | Lambda for GET /items         |
| GetItemById | AWS::Serverless::Function | Lambda for GET /items/{id}    |
| PostItem    | AWS::Serverless::Function | Lambda for POST /items        |
| UpdateItem  | AWS::Serverless::Function | Lambda for PUT /items/{id}    |
| DeleteItem  | AWS::Serverless::Function | Lambda for DELETE /items/{id} |
| Items       | AWS::DynamoDB::Table      | DynamoDB table for items      |
| \*LogGroups | AWS::Logs::LogGroup       | CloudWatch log groups (5x)    |

### Lambda Configuration

- **Runtime**: Python 3.13
- **Memory**: 3008 MB
- **Timeout**: 30 seconds
- **Tracing**: X-Ray enabled

---

## 🛠️ Useful Commands

| Command                                           | Description                      |
| ------------------------------------------------- | -------------------------------- |
| `sam build`                                       | Build the application            |
| `sam local start-api`                             | Start local API Gateway          |
| `sam local invoke FunctionName`                   | Invoke a single function locally |
| `sam deploy`                                      | Deploy to AWS                    |
| `sam deploy --guided`                             | Deploy with interactive prompts  |
| `sam logs -n FunctionName --stack-name SimpleApi` | View Lambda logs                 |
| `sam delete`                                      | Delete the CloudFormation stack  |

---

## 📄 License

This project is proprietary. All rights reserved.
