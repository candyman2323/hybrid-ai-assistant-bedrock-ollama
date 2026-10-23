# Hybrid AI Assistant

## Overview
A Hybrid AI Assistant that combines local AI models and cloud-based AI services to generate responses. It uses Llama 3.2 through Ollama for local inference and Amazon Bedrock for cloud-based inference.

## Features
- Local AI inference using Llama 3.2 and Ollama
- Cloud AI inference using Amazon Bedrock
- Automatic selection between local and cloud models
- FastAPI backend for handling chat requests
- Web-based chat interface

## Technologies Used
- Python
- FastAPI
- Ollama
- Llama 3.2
- Amazon Bedrock
- AWS Boto3
- HTML, CSS, JavaScript

## Project Structure
```text
hybrid-ai-assistant/
├── main.py
├── index.html
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   cd hybrid-ai-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Ollama and download the model:
   ```bash
   ollama pull llama3.2
   ```

5. Configure AWS credentials securely and ensure your AWS account has access to Amazon Bedrock in the configured region.

6. Start the application:
   ```bash
   uvicorn main:app --reload
   ```

7. Open the chat interface:
   http://127.0.0.1:8000/ui

## API Endpoints
- `/` — Application home
- `/health` — Health check
- `/v1/models` — Available model information
- `/chat` — Chat API
- `/ui` — Web chat interface
- `/docs` — Interactive API documentation

## Learning Outcomes
- Integrated local and cloud-based AI models.
- Built REST APIs using FastAPI.
- Used Amazon Bedrock for cloud model inference.
- Implemented hybrid model selection.

## Security
Never upload AWS access keys, secret keys, or other credentials to GitHub. Use secure credential configuration and keep `.venv` and `.env` files out of version control.

## Future Enhancements
- Deploy the application on AWS.
- Add conversation history.
- Improve model routing and error handling.
- Add authentication and monitoring.

## Author
Sangeetha Dola