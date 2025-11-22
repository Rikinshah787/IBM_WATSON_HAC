
content = """# IBM watsonx Orchestrate Configuration
WATSONX_ORCHESTRATE_API_KEY=your_api_key_here
WATSONX_ORCHESTRATE_URL=https://api.watsonx.orchestrate.cloud.ibm.com
WATSONX_ORCHESTRATE_PROJECT_ID=your_project_id_here

# IBM watsonx.ai Configuration (Optional)
WATSONX_AI_API_KEY=your_watsonx_ai_api_key_here
WATSONX_AI_URL=https://us-south.ml.cloud.ibm.com
WATSONX_AI_PROJECT_ID=your_watsonx_ai_project_id_here

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000
"""

with open(".env", "w") as f:
    f.write(content)
print("Created .env file")
