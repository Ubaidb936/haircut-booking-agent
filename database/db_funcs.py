import json
from pathlib import Path 
from langchain_core.tools import tool
DB_PATH = Path(__file__).parent.parent / "database" / "bookings.json"  

def grab_availibilities() -> list:
    with open(DB_PATH) as f:
      data = json.load(f)
      availability= data["availability"]
    return availability

def grab_data() -> list:
    with open(DB_PATH) as f:
      data = json.load(f)
    return data

def store_data(data: dict):                                                                                                                                 
      with open(DB_PATH, "w") as f:                                                                                                                             
          json.dump(data, f, indent=2)
   