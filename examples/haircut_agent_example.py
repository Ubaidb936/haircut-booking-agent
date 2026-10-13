import uuid
import asyncio  
from langchain_anthropic import ChatAnthropic
from agent.hair_cut_agent import HairCutAgent
from core.settings import settings
from tools.find_available_tool import find_availability
from tools.finish_booking import finish_booking


async def main():
    agent = HairCutAgent(
           api_key=settings.anthropic_api_key, 
           tools=[find_availability, finish_booking])
    thread_id = str(uuid.uuid4())
    await agent.start(thread_id)
asyncio.run(main())


