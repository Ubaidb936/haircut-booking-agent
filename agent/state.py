from typing_extensions import TypedDict
from typing import List, Optional, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class HairCutAppointmentState(TypedDict): 
    messages: Annotated[list, add_messages]     
    customer_name: Optional[str]
    service_type: Optional[str]
    start_time: Optional[str]
    phone: Optional[str]
    booked: Optional[bool]
    




