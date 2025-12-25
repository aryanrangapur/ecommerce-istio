# Istio E-Commerce Demo

A microservices e-commerce app on GKE with Istio for security, traffic, and observability.

## Setup
- GCP Project: istio-ecommerce-demo
- Cluster: istio-ecommerce-cluster

## Services
- frontend: React/Next.js
- product: FastAPI
- review: FastAPI (v1/v2 for canary)
- inventory: FastAPI
- order: FastAPI
- payment: FastAPI (mock)

## Phases
1. Microservices only
2. Add Istio
3. Security (mTLS + Auth)
... (add more as we go)
