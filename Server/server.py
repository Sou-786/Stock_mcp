import os
import sys
import time
from fastmcp import FastMCP
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from utils import kill_port_process
from Client.client import AliceBlue
from Client.config import APP_KEY, API_SECRET
from Client.utils import * 

load_dotenv()

mcp = FastMCP(
    name="New AliceBlue Portfolio Agent",
    dependencies=["python-dotenv", "requests"]
)
_alice_client = None

def get_alice_client(force_refresh: bool = False) -> AliceBlue:
    """Return a cached AliceBlue client, authenticate only once unless forced."""
    global _alice_client

    if _alice_client and not force_refresh:
        return _alice_client

    app_key = APP_KEY
    api_secret = API_SECRET

    if not app_key or not api_secret:
        raise Exception("Missing credentials. Please set ALICE_APP_KEY and ALICE_API_SECRET in .env file")

    alice = AliceBlue(app_key=app_key, api_secret=api_secret)
    alice.authenticate() 
    _alice_client = alice
    return _alice_client

try:
    sys.path.insert(0, current_dir)
    from tools import *
    print("Tools imported successfully")
except ImportError as e:
    print(f"Error importing tools: {e}")
  
if __name__ == "__main__":
    app_key = API_SECRET
    api_secret = API_SECRET
    if not app_key or not api_secret:
        raise Exception("Missing credentials. Please set ALICE_APP_KEY and ALICE_API_SECRET in .env file")
    
    if not is_port_available(8080):
        print(f"Port 8080 is busy. Attempting to free it...")
        kill_port_process(8080)
        time.sleep(2)

    mcp.run(transport="sse", host="127.0.0.1", port=8000)