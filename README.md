AI Network Troubleshooter
A Proof of Concept (PoC) designed to automate network incident response and troubleshooting using Large Language Models (LLMs), telemetry data, and automated network interaction frameworks. This tool integrates a TIG stack (Telegraf, InfluxDB, Grafana) with Cisco pyATS and OpenAI to detect, analyze, and remediate network anomalies.

Architecture Overview
The system operates through a closed-loop automation workflow:

Telemetry Collection: Telegraf utilizes ncpeek (a Netconf client wrapper) to pull real-time telemetry from network devices.

Monitoring & Alerting: Data is stored in InfluxDB. Grafana monitors these metrics and triggers a webhook when a predefined alarm threshold is met.

Intelligent Analysis: A FastAPI-based LLM agent receives the Grafana alert. It uses OpenAI (GPT-4o) to interpret the issue.

Network Interaction: The agent leverages the pyATS framework to execute operational commands on network devices to gather more context or perform troubleshooting.

Communication: Status updates and troubleshooting results are dispatched via a Webex bot or REST API.

Repository Structure
/llm_agent: FastAPI application housing the logic for the LLM agent and chat endpoints.

/telegraf: Configuration for telemetry polling using ncclient.

/grafana: Dashboards and alert policies.

/cml: Cisco Modeling Labs (CML) topology files for simulation.

Makefile: Orchestration commands for building and running the containerized environment.

Prerequisites
Docker & Docker Compose: Ensure you are using Compose V2 (docker compose).

Cisco Modeling Labs (CML): Required to run the XE device topology.

Python 3.10+ (if running components outside of Docker).

OpenAI API Key: For the intelligence engine.

Webex Bot Token: (Optional) For messaging integration.

Installation & Setup
Clone the Repository:

Bash
git clone https://github.com/NachmanM/ai-network-troubleshooter.git
cd ai-network-troubleshooter
Environment Configuration: Create a .env file in the root directory. This file is required by the Makefile and Docker Compose. Include the following variables:

Code snippet
OPENAI_API_KEY=your_key_here
WEBEX_TOKEN=your_token_here
INFLUXDB_TOKEN=your_token_here
# Add other necessary device credentials and API keys
Deploy the Stack: Use the provided Makefile to initialize the TIG stack and the LLM agent:

Bash
make run-tig
Usage
Automated Triage: When Grafana detects a network anomaly (e.g., interface flapping, high CPU), it sends a POST request to the /alert endpoint of the FastAPI agent.

Manual Interaction: You can interact with the agent via Webex to ask specific questions about the network state. The agent will use pyATS to "parse" device outputs into structured JSON for the LLM to analyze.

Technical Considerations
Token Optimization: Netconf outputs can be verbose. The system is designed to filter data before sending it to the LLM to minimize token consumption and latency.

State Management: Repeated alarms are suppressed by Grafana policies. To reset the environment during testing, use make run-tig to recreate the containers.

Extensibility: The notify function in the agent can be modified to support Slack, Microsoft Teams, or other notification platforms.
