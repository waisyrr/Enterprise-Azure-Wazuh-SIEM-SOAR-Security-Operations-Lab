flowchart TB

    ATTACK["Simulated Attack<br/>Failed Logons / Suspicious PowerShell / FIM Change"]

    ENDPOINT["Windows Endpoint<br/>win11 or dc01"]

    TELEMETRY["Security Telemetry<br/>Windows Event Logs<br/>Sysmon<br/>PowerShell<br/>FIM"]

    AGENT["Wazuh Agent"]

    MANAGER["Wazuh Manager<br/>Decoders and Rules"]

    CORRELATION["Detection and Correlation<br/>Rule Matching<br/>Severity Assignment"]

    subgraph DETECTION["Detection Outputs"]
        direction LR
        MITRE["MITRE ATT&CK Mapping"]
        ALERT["Wazuh Alert<br/>Dashboard and alerts.json"]
    end

    CASE["Structured SOC Case<br/>Severity • Priority • Endpoint<br/>Account • Source IP • SLA"]

    SHUFFLE["Shuffle SOAR<br/>Webhook Ingestion"]

    subgraph SOAR["SOAR Processing"]
        direction LR
        ENRICH["Threat Enrichment<br/>VirusTotal and AbuseIPDB"]
        NOTIFY["SOC Notification<br/>Slack and Email"]
    end

    APPROVAL["Human Approval<br/>P1 Incident Review"]

    RESPONSE["Automated Containment<br/>Azure Automation"]

    subgraph CONTAINMENT["Containment Actions"]
        direction LR
        FIREWALL["Block Malicious IP<br/>Windows Firewall"]
        DISABLE["Disable Compromised User<br/>Active Directory"]
    end

    ATTACK --> ENDPOINT
    ENDPOINT --> TELEMETRY
    TELEMETRY --> AGENT
    AGENT --> MANAGER
    MANAGER --> CORRELATION

    CORRELATION --> MITRE
    CORRELATION --> ALERT

    ALERT --> CASE
    CASE --> SHUFFLE

    SHUFFLE --> ENRICH
    SHUFFLE --> NOTIFY

    ENRICH --> APPROVAL
    APPROVAL --> RESPONSE

    RESPONSE --> FIREWALL
    RESPONSE --> DISABLE