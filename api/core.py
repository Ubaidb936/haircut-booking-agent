from agent.hair_cut_agent import HairCutAgent
from core.settings import settings
from tools.find_available_tool import find_availability
from tools.finish_booking import finish_booking

agent = HairCutAgent(
    api_key=settings.anthropic_api_key,
    tools=[find_availability, finish_booking]
)