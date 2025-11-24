import os
import asyncio
import logging
import sys
from dotenv import load_dotenv
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("watson_debug")

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_pass(msg):
    print(f"{GREEN}[PASS] {msg}{RESET}")

def print_fail(msg):
    print(f"{RED}[FAIL] {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}[INFO] {msg}{RESET}")

def print_warn(msg):
    print(f"{YELLOW}[WARN] {msg}{RESET}")

async def check_watsonx_ai(api_key, url, project_id):
    print_info("Testing watsonx.ai connection...")
    
    if not api_key or not project_id:
        print_fail("watsonx.ai credentials missing (API Key or Project ID)")
        return

    # Get IAM Token
    token_url = "https://iam.cloud.ibm.com/identity/token"
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(token_url, data=data, headers=headers)
            if r.status_code != 200:
                print_fail(f"Failed to get IAM token: {r.text}")
                return
            
            token = r.json().get("access_token")
            print_pass("Successfully authenticated with IBM Cloud IAM")
            
            # Test Text Generation (Simple Hello World)
            endpoint = f"{url.rstrip('/')}/ml/v1/text/generation"
            params = {"version": "2024-05-31"}
            payload = {
                "input": "Hello, are you working?",
                "model_id": "ibm/granite-13b-instruct-v2",
                "project_id": project_id,
                "parameters": {
                    "max_new_tokens": 10,
                    "decoding_method": "greedy"
                }
            }
            gen_headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            r_gen = await client.post(endpoint, params=params, json=payload, headers=gen_headers)
            if r_gen.status_code == 200:
                print_pass("Successfully generated text with watsonx.ai")
            else:
                print_fail(f"Failed to generate text: {r_gen.status_code} - {r_gen.text}")

    except Exception as e:
        print_fail(f"Connection error: {str(e)}")

async def check_orchestrate(api_key, url):
    print_info("Testing watsonx Orchestrate connection...")
    
    if not api_key or not url:
        print_warn("watsonx Orchestrate credentials missing. Skipping test.")
        return

    # Basic connectivity check
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Just checking if the URL is reachable, actual auth might require complex flow
            # This is a basic reachability test
            try:
                r = await client.get(url)
                print_pass(f"Successfully reached Orchestrate URL ({r.status_code})")
            except httpx.ConnectError:
                print_fail("Could not connect to Orchestrate URL")
    except Exception as e:
        print_fail(f"Orchestrate check failed: {str(e)}")

async def main():
    print("\n🔍 Starting Watson Configuration Debugger\n" + "="*40)
    
    # 1. Check .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        print_pass(f"Found .env file at {env_path}")
        load_dotenv(env_path)
    else:
        print_fail(f".env file not found at {env_path}")
        print_warn("Please copy .env.example to .env and configure your credentials.")
        return

    # 2. Load Credentials
    wx_api_key = os.getenv("WATSONX_AI_API_KEY")
    wx_url = os.getenv("WATSONX_AI_URL")
    wx_project_id = os.getenv("WATSONX_AI_PROJECT_ID")
    
    wo_api_key = os.getenv("WATSONX_ORCHESTRATE_API_KEY")
    wo_url = os.getenv("WATSONX_ORCHESTRATE_URL")

    # 3. Run Checks
    await check_watsonx_ai(wx_api_key, wx_url, wx_project_id)
    print("-" * 40)
    await check_orchestrate(wo_api_key, wo_url)
    
    print("="*40 + "\nDebug Complete.\n")

if __name__ == "__main__":
    asyncio.run(main())
