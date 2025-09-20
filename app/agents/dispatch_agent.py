from google.adk.agents import LlmAgent
from .tools.fetch_nearby import get_nearby_responders_tool, get_nearby_hospitals_tool

dispatch_agent = LlmAgent(
    name="dispatch_agent",
    model="gemini-2.5-flash",
    description="Allocates ambulances, issues dispatch commands, tracks en-route status and ETA updates.",
    instruction=(
        "Match available responders to incident based on ETA, skills, and load. Reserve unit(s), notify crew via sms_sender, "
        "and provide continuous ETA updates. If no ambulances are available locally, expand radius exponentially and escalate."
    ),
    tools=[get_nearby_responders_tool, get_nearby_hospitals_tool],
)