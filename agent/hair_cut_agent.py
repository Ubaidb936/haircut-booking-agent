from typing import List
from agent.base_agent import BaseAgent
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage
from core.schema import Output

from agent.state import HairCutAppointmentState
from agent.nodes import make_llm_node, prepare_input_node, human_input, should_continue, parse_tool_output

class HairCutAgent(BaseAgent):
    def __init__(self, api_key: str, tools: List):
        llm = ChatAnthropic(api_key=api_key, model_name="claude-sonnet-4-6", temperature=0.2).bind_tools(tools)

        llm_node = make_llm_node(llm)
        tool_node = ToolNode(tools)  

        builder = StateGraph(HairCutAppointmentState)
        builder.add_node("prepare_input_node", prepare_input_node)
        builder.add_node("llm", llm_node)
        builder.add_node("tool", tool_node)
        builder.add_node("human_input", human_input)
        builder.add_node("parse_tool_output", parse_tool_output)

        builder.set_entry_point("prepare_input_node")
        builder.add_edge("prepare_input_node", "llm")
        builder.add_edge("human_input", "llm")
        builder.add_edge("tool", "parse_tool_output")
        builder.add_edge("parse_tool_output", "llm")
        builder.add_conditional_edges("llm", should_continue, {
            "tool": "tool",
            "human_input": "human_input",
            "end": END
        })
        self.graph = builder.compile(checkpointer=MemorySaver())

    def _extract_response(self, result: dict, thread_id: str) -> Output:
        """Extract AI message and done status from graph result."""
        booked = result.get("booked", False)
        message = ""
        for msg in reversed(result.get("messages", [])):
            if isinstance(msg, AIMessage) and not msg.tool_calls:
                content = msg.content
                if isinstance(content, list):
                    content = next((c["text"] for c in content if c.get("type") == "text"), "")
                if content:
                    message = content
                    break
        
        output = Output(message=message, booked=booked, thread_id=thread_id)
        if booked:
            output.customer_name = result.get("customer_name")
            output.service_type = result.get("service_type")
            output.start_time = result.get("start_time")
        return output  

    async def start(self, thread_id: str) -> Output:
        config = {"configurable": {"thread_id": thread_id}}
        state = {
            "messages": [],
            "customer_name": None,
            "start_time": None,
            "booked": False
        }
        result = await self.graph.ainvoke(state, config=config)
        return self._extract_response(result, thread_id)
    
    async def resume(self, thread_id: str, message: str) -> Output:
        config = {"configurable":{"thread_id": thread_id}}
        result = await self.graph.ainvoke(Command(resume=message), config=config)
        return self._extract_response(result, thread_id)







        

        



        
        

        