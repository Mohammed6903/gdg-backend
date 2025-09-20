from google.adk.agents import Agent
# from .tools.audit_logger import audit_logger
# from .tools.metrics_pusher import metrics_pusher

telemetry_agent = Agent(
    name="telemetry_agent",
    model="gemini-live-2.5-flash-preview",
    description="Records structured logs, metrics and events for auditing and SLA monitoring.",
    instruction=(
        "Append immutable audit records for every decision and action (who/what/when). Push SLA metrics and emit alerts on threshold breaches."
    ),
    # tools=[audit_logger, metrics_pusher],
)