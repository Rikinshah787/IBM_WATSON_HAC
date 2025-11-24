import os
import json
import requests
from dotenv import load_dotenv
from agents import AGENTS

# Load environment variables
load_dotenv()

API_KEY = os.getenv("WATSONX_AI_API_KEY")
PROJECT_ID = os.getenv("WATSONX_AI_PROJECT_ID")
MODEL_ID = os.getenv("WATSONX_AI_MODEL_ID", "ibm/granite-3-8b-instruct")
URL = os.getenv("WATSONX_AI_URL")

class Orchestrator:
    def __init__(self):
        self.access_token = self._get_access_token()
        print(f"🤖 Orchestrator initialized with model: {MODEL_ID}")

    def _get_access_token(self):
        """Authenticate with IBM Cloud"""
        url = "https://iam.cloud.ibm.com/identity/token"
        try:
            response = requests.post(url, data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": API_KEY
            })
            return response.json().get("access_token")
        except Exception as e:
            print(f"Auth Error: {e}")
            return None

    def _call_granite(self, prompt, max_tokens=200):
        """Send prompt to Granite model"""
        if not self.access_token:
            return "Error: No access token"

        url = f"{URL}/ml/v1/text/generation?version=2023-05-29"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "input": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.1, # Low temp for precise routing
                "min_new_tokens": 1
            },
            "model_id": MODEL_ID,
            "project_id": PROJECT_ID
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()["results"][0]["generated_text"].strip()
            else:
                print(f"Granite Error: {response.text}")
                return None
        except Exception as e:
            print(f"Request Error: {e}")
            return None

    def route_request(self, user_query):
        """
        Step 1: Intent Recognition
        Ask Granite which agent handles this query.
        """
        prompt = f"""
        You are an intelligent orchestrator. Your job is to route user queries to the correct agent.
        
        Available Agents:
        1. HR Agent: Employee data, performance, satisfaction.
        2. Sales Agent: Revenue, deals, regional sales.
        3. Customer Service Agent: Tickets, support issues, resolution times.
        4. Finance Agent: Expenses, budgets, department costs.
        
        User Query: "{user_query}"
        
        Which agent should handle this? Reply ONLY with one of these words: HR, SALES, SERVICE, FINANCE.
        If unsure, reply UNKNOWN.
        
        Agent:
        """
        
        intent = self._call_granite(prompt, max_tokens=10)
        print(f"🧠 Intent Detected: {intent}")
        return intent

    def process_query(self, user_query):
        """
        Main flow: Query -> Intent -> Agent -> Data -> Summary
        """
        # 1. Identify Intent
        intent = self.route_request(user_query)
        
        if not intent:
            return "Sorry, I couldn't understand that request."
            
        intent = intent.upper()
        data = None
        agent_name = ""

        # 2. Route to Agent & Get Data
        if "HR" in intent:
            agent_name = "HR Agent"
            data = AGENTS["hr"].get_employee_details() # Simplified for demo
        elif "SALES" in intent:
            agent_name = "Sales Agent"
            data = AGENTS["sales"].get_sales_by_region()
        elif "SERVICE" in intent:
            agent_name = "Customer Service Agent"
            data = AGENTS["service"].get_ticket_stats()
        elif "FINANCE" in intent:
            agent_name = "Finance Agent"
            data = AGENTS["finance"].get_department_expenses()
        else:
            return "I'm not sure which agent to ask. Please try asking about HR, Sales, Service, or Finance."

        print(f"📊 Data Retrieved from {agent_name}: {json.dumps(data)[:100]}...")

        # 3. Generate Natural Language Response
        summary_prompt = f"""
        You are a helpful assistant. Analyze the following data and answer the user's question.
        
        User Question: "{user_query}"
        Data from {agent_name}: {json.dumps(data)}
        
        Provide a clear, professional summary of the answer.
        """
        
        final_answer = self._call_granite(summary_prompt, max_tokens=300)
        return final_answer

# --- Test the Orchestrator ---
if __name__ == "__main__":
    orchestrator = Orchestrator()
    
    test_queries = [
        "How are our sales doing by region?",
        "Show me the employee performance ratings.",
        "What are the current ticket resolution times?"
    ]
    
    print("\n" + "="*50)
    print("🚀 STARTING ORCHESTRATOR TEST")
    print("="*50)
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        response = orchestrator.process_query(query)
        print(f"🤖 Orchestrator: {response}")
        print("-" * 50)
