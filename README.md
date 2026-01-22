# Cloud-Based IoT Environmental Telemetry Platform

## Overview
This project implements a **cloud-native IoT Environmental Telemetry Platform** that ingests temperature and humidity data from ESP32-based devices, processes the data using asynchronous microservices, and exposes the data through secure REST APIs. The system is deployed on AWS using containerized services, Kubernetes orchestration, Infrastructure as Code, and automated CI/CD pipelines.

The project follows a milestone-driven lifecycle aligned with industry-standard cloud engineering practices, including architecture design, design reviews, observability, security, load testing, and operational readiness.

---

## Architecture Summary
High-level data flow:
ESP32 → API Gateway → Ingestion Service (EKS) → SQS → Worker Service (EKS)
→ DynamoDB → API Service (EKS) → Clients

Key architectural characteristics:
- Cloud-native microservice design
- Asynchronous ingestion using Amazon SQS
- Kubernetes-based deployment with autoscaling
- Centralized logging, metrics, and alerting
- Security-first design with least-privilege access

Detailed architecture diagrams and design decisions are documented in `/docs`.

---

## Core Features
- IoT telemetry ingestion via HTTPS REST API
- Asynchronous processing and buffering
- Scalable, serverless data storage using DynamoDB
- Secure API access with authentication
- Centralized observability (logs, metrics, alarms)
- Kubernetes autoscaling and fault tolerance
- CI/CD automation from commit to deployment

---

## Technology Stack

### Cloud & Infrastructure
- **Cloud Provider:** AWS
- **Container Orchestration:** Amazon EKS (Kubernetes)
- **API Gateway:** Amazon API Gateway (HTTP API)
- **Queue:** Amazon SQS
- **Database:** Amazon DynamoDB
- **Secrets Management:** AWS Secrets Manager
- **Observability:** Amazon CloudWatch
- **IAM:** Least-privilege role-based access

### DevOps & Tooling
- Docker
- Kubernetes (HPA enabled)
- Terraform (Infrastructure as Code)
- GitHub Actions (CI/CD)
- curl / Postman for API testing

### IoT
- ESP32 microcontroller
- DHT temperature/humidity sensor
- HTTPS-based telemetry publishing


---

## API Endpoints

### Telemetry Ingestion
**POST** `/v1/telemetry`  
Ingest telemetry data from ESP32 devices.

### Data Retrieval
**GET** `/v1/devices/{deviceId}/telemetry/latest`  
**GET** `/v1/devices/{deviceId}/telemetry?start=...&end=...`

### Health
**GET** `/health`  
Service health and readiness check.

---

## Security Model
- Device authentication using API keys or JWT (configurable)
- Secrets stored in AWS Secrets Manager
- IAM roles with least-privilege permissions
- Private access to DynamoDB from Kubernetes workloads

---

## Observability & Reliability
- Centralized logging via CloudWatch Logs
- Metrics for request rate, error rate, latency, and queue depth
- CloudWatch Alarms for failure detection
- Horizontal Pod Autoscaling (HPA) for Kubernetes services
- Failure scenarios tested using queue backlog and service interruption

---

## CI/CD
- Automated build and test on pull requests
- Container image build and deployment pipeline
- Versioned deployments with rollback support
- Separate staging and production environments (where applicable)

---

## Project Milestones
This repository supports a milestone-driven academic project lifecycle:
- Project proposal and backlog definition
- Architecture design and review
- Kubernetes deployment and autoscaling
- Asynchronous processing integration
- Load testing, tuning, and cost controls
- Final demo and reporting

---

## Team
- **Seid Cubro**
- **Charles Shoppel**

---

## Status
This project is under active development as part of a cloud practicum course.  
Features and infrastructure evolve incrementally according to milestone requirements.

---

## License
Academic project – for educational use only.
