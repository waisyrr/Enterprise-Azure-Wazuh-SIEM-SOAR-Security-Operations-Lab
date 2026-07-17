flowchart TB

    ENDPOINTS["Monitored Systems<br/>dc01, win11, wazuh01"]

    TELEMETRY["Security Telemetry<br/>Windows Events, Sysmon, Auditd, FIM"]

    AGENTS["Wazuh Agents<br/>Local Log Collection"]

    MANAGER["Wazuh Manager<br/>Decoders and Rules"]

    CORRELATION["Detection and Correlation<br/>Rules 60122, 60204, 5712"]

    subgraph DETECTION["Detection and Investigation"]
        direction LR
        INDEXER["Wazuh Indexer<br/>Alert Storage"]
        DASHBOARD["Wazuh Dashboard<br/>Threat Hunting and Investigation"]
    end

    CASE["Structured Incident<br/>Case ID, Severity, Priority, SLA"]

    SHUFFLE["Shuffle SOAR<br/>Webhook Ingestion"]

    ENRICH["Threat Enrichment<br/>VirusTotal and AbuseIPDB"]

    subgraph ACTIONS["SOC Actions"]
        direction LR
        NOTIFY["SOC Notifications<br/>Slack and Email"]
        APPROVAL["Human Approval"]
    end

    RESPONSE["Automated Response<br/>Block IP or Disable AD User"]

    VALIDATE["Containment Validation<br/>Firewall Rule and AD Status"]

    ENDPOINTS --> TELEMETRY
    TELEMETRY --> AGENTS
    AGENTS --> MANAGER
    MANAGER --> CORRELATION

    CORRELATION --> INDEXER
    INDEXER --> DASHBOARD

    CORRELATION --> CASE
    CASE --> SHUFFLE
    SHUFFLE --> ENRICH

    ENRICH --> NOTIFY
    ENRICH --> APPROVAL

    APPROVAL --> RESPONSE
    RESPONSE --> VALIDATE