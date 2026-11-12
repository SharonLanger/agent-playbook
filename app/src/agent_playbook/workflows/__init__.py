"""Stage 01 workflows run locally, without CrewAI usage telemetry or AMP tracing.

Python loads this package before its flow modules import CrewAI. These settings
are deliberately enforced for this deterministic stage, without disabling global
OpenTelemetry (which a later stage will configure independently).
"""

import os

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["CREWAI_TRACING_ENABLED"] = "false"
