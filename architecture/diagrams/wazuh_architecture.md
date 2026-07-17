flowchart TB

    subgraph SOURCES["Monitored Systems and Telemetry"]
        direction LR
        WIN11["win11<br/>Windows 11<br/>Wazuh Agent"]
        DC["dc01<br/>Windows Server 2025<br/>Wazuh Agent"]
        LOCAL["wazuh01 Local Telemetry<br/>Ubuntu, SSH, Auditd and FIM"]
    end

    MANAGER["Wazuh Manager<br/>Analysis Engine<br/>Rules and Decoders"]

    WIN11 -->|"Sysmon<br/>Security and PowerShell Logs<br/>FIM"| MANAGER
    DC -->|"Windows Security Logs<br/>PowerShell and FIM"| MANAGER
    LOCAL --> MANAGER

    subgraph SIEM["SIEM Processing and Investigation"]
        direction LR
        INDEXER["Wazuh Indexer<br/>Alert Storage"]
        DASHBOARD["Wazuh Dashboard<br/>Threat Hunting<br/>MITRE ATT&CK Context<br/>FIM and Vulnerabilities"]
    end

    MANAGER --> INDEXER
    INDEXER --> DASHBOARD

    subgraph ACTIVE_RESPONSE["Wazuh Active Response"]
        direction LR
        ACTIVE["Rule-Triggered Execution"]
        PROOF["Server-Side Response<br/>Execution Validation"]
    end

    MANAGER --> ACTIVE
    ACTIVE --> PROOF

    CASE["Python SOC Automation<br/>Incident Enrichment and Case Creation"]

    SHUFFLE["Shuffle SOAR<br/>Webhook Ingestion"]

    MANAGER --> CASE
    CASE -->|"Structured Incident JSON"| SHUFFLE

    subgraph SOAR_OUTPUTS["SOAR Enrichment and Notifications"]
        direction TB

        subgraph INTEL["Threat Intelligence"]
            direction LR
            VT["VirusTotal"]
            ABUSE["AbuseIPDB"]
        end

        subgraph NOTIFICATIONS["Notifications and Approval"]
            direction LR
            SLACK["Slack P1 Alert"]
            APPROVAL["Human Approval<br/>Email Approval Request"]
        end
    end

    SHUFFLE --> VT
    SHUFFLE --> ABUSE
    SHUFFLE --> SLACK
    SHUFFLE --> APPROVAL

    AZURE["Azure Automation"]

    APPROVAL --> AZURE

    subgraph CONTAINMENT["Automated Containment"]
        direction TB

        subgraph ENDPOINT_RESPONSE["Endpoint Response"]
            direction LR
            WINRUN["Remote Runbook Execution<br/>win11"]
            FIREWALL["Block Malicious IP<br/>Windows Firewall"]
        end

        subgraph AD_RESPONSE["Active Directory Response"]
            direction LR
            HYBRID["Hybrid Runbook Worker<br/>dc01"]
            AD["Disable Compromised<br/>Active Directory User"]
        end
    end

    AZURE --> WINRUN
    WINRUN --> FIREWALL

    AZURE --> HYBRID
    HYBRID --> AD