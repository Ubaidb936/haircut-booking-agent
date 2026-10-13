import json
from langchain_core.tools import tool
from database.db_funcs import grab_availibilities, grab_data  

@tool
def find_availability(time: str) -> str:
    """ 
        This function checks the availibility in the Salon  
        Args:
            time: requested time in 24-hour format "HH:MM" (e.g. "10:00", "14:30") 
        returns:
            tool name
            if there is a availibilty at the time
            list of other available slots.    
    """
    availability = grab_availibilities()

    return json.dumps({
       "tool_name": "find_availability",
       "time_requested": time,
       "is_available": time in availability,
       "available_slots": availability 
    })