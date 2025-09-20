from google.adk.agents import Agent
# from .tools.hospital_lookup import hospital_lookup
# from .tools.contact_hospital import contact_hospital

hospital_agent = Agent(
    name="hospital_agent",
    model="gemini-live-2.5-flash-preview",
    description="Finds receiving hospitals, checks bed/specialist availability, sends pre-notification.",
    instruction=(
        "Given patient condition and ETA, find suitable hospitals, query bed/OR availability, and send structured pre-notification "
        "to the receiving facility with minimal PHI required for triage. Escalate if no suitable hospital accepts the patient."
    ),
    # tools=[hospital_lookup, contact_hospital],
)