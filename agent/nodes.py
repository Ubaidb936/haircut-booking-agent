from agent.state import HairCutAppointmentState
from agent.prompt import BOOKING_DETAILS_PROMPT
from langchain_core.messages import HumanMessage
from typing import Callable
import json
from langgraph.types import interrupt

def prepare_input_node(state: HairCutAppointmentState):
    return {
        "messages": HumanMessage(content=BOOKING_DETAILS_PROMPT),
        "booked": False
    }

def make_llm_node(llm_with_tool_calls)-> Callable:
    async def llm_node(state: HairCutAppointmentState):
        response = await llm_with_tool_calls.ainvoke(state["messages"])
        return {"messages": [response]}
    return llm_node    


def parse_tool_output(state:HairCutAppointmentState):
    updates = {}
    for msg in reversed(state["messages"]):
        if hasattr(msg, "name") and msg.name == "finish_booking":
            data = json.loads(msg.content)
            updates["customer_name"] = data.get("customer_name")
            updates["service_type"] = data.get("service_type")
            updates["start_time"] = data.get("start_time")
            updates["phone"] = data.get("phone")
            updates["booked"] = data.get("booked")
            break    
    return updates 

def human_input(state: HairCutAppointmentState):
    user_message = interrupt("Waiting for user input")
    return {"messages": [HumanMessage(content=user_message)]}


def should_continue(state: HairCutAppointmentState):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tool"
    for msg in reversed(state["messages"]):
        if hasattr(msg, "name") and msg.name == "finish_booking":
            return "end"
    return "human_input"




