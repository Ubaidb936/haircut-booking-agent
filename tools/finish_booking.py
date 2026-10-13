import json
from langchain_core.tools import tool
from database.db_funcs import grab_data, store_data

# class HairCutAppointmentState(TypedDict): 
#     messages: Annotated[list, add_messages]     
#     customer_name: Optional[str]
#     service_type: Optional[str]
#     start_time: Optional[str]
#     booked: Optional[bool]

@tool
def finish_booking(start_time:str, service_type:str, customer_name:str, phone: str) -> str:
    """
     Call this tool when the customer is done providing all the details to book the appointment.
    """
    data = grab_data()
    data["availability"] = [t for t in data["availability"] if t != start_time]
    new_booking = {                                                                                                                                     
      "start_time": start_time,                                                                                                                                             
      "service": service_type,
      "customer_name": customer_name,
      "phone": phone,
      "booked": True
    }
    data["bookings"].append(new_booking)
    store_data(data)
    new_booking["tool_name"] = "finish_booking"
    return json.dumps(new_booking)