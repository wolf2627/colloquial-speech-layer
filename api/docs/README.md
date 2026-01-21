# API Documentation

Welcome to the Colloquial Speech Layer API documentation.

## Overview

This API provides a modular, extensible interface for connecting to various AI models. The architecture uses dynamic endpoint routing - simply add a new handler file to `/src` and the endpoint is auto-created.

## Contents

1. [Architecture Overview](./architecture.md)
2. [API Reference](./api_reference.md)
3. [Data Flow Guide](./data_flow.md)
4. [Adding New Models](./adding_models.md)
5. [Configuration](./configuration.md)

## Quick Links

- **Base URL**: `http://localhost:8000`
- **API Docs (Swagger)**: `http://localhost:8000/docs`
- **Health Check**: `GET /`
- **List Models**: `GET /api/models`
