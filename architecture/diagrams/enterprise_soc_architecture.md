flowchart TB

    Internet((Internet))

    subgraph Azure["Microsoft Azure"]
        subgraph VNet["enterprise-soc-vnet — 10.0.0.0/16"]
            direction LR

            DC["dc01<br/>Windows Server 2025<br/>AD DS + DNS<br/>10.0.0.4"]

            WIN11["win11<br/>Windows 11 Pro<br/>Domain Endpoint<br/>10.0.0.5"]

            WAZUH["wazuh01<br/>Ubuntu Server<br/>Wazuh Manager, Indexer & Dashboard"]
        end
    end

    Internet --> DC
    Internet --> WIN11
    Internet --> WAZUH

    WIN11 -->|"Domain authentication / DNS"| DC

    DC -->|"Windows security telemetry"| WAZUH
    WIN11 -->|"Sysmon, Security, PowerShell & FIM logs"| WAZUH
    WAZUH -->|"Local Linux, SSH, Auditd & FIM logs"| WAZUH

    DASH["Wazuh Dashboard<br/>Threat Hunting, FIM, SCA,<br/>Vulnerabilities & MITRE"]

    SHUFFLE["Shuffle SOAR<br/>Structured Incident Ingestion"]

    WAZUH --> DASH
    WAZUH -->|"Structured incident JSON"| SHUFFLE

    subgraph ENRICHMENT["Enrichment and Notifications"]
        direction TB

        subgraph THREAT_INTEL["Threat Intelligence"]
            direction LR
            VT["VirusTotal"]
            ABUSE["AbuseIPDB"]
        end

        subgraph NOTIFICATIONS["SOC Notifications"]
            direction LR
            SLACK["Slack P1 Alert"]
            EMAIL["Email Notification"]
        end
    end

    APPROVAL["Human Approval"]

    SHUFFLE --> VT
    SHUFFLE --> ABUSE
    SHUFFLE --> SLACK
    SHUFFLE --> EMAIL
    SHUFFLE --> APPROVAL

    AZAUTO["Azure Automation<br/>Hybrid Worker"]

    subgraph CONTAINMENT["Automated Containment"]
        direction LR
        FIREWALL["Block Malicious IP<br/>Windows Firewall"]
        ADUSER["Disable Compromised User<br/>Active Directory"]
    end

    APPROVAL --> AZAUTO
    AZAUTO --> FIREWALL
    AZAUTO --> ADUSER