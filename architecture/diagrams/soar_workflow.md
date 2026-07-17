flowchart TB

    ALERT["P1 Wazuh Alert"]

    WEBHOOK["Shuffle Webhook"]

    PARSE["Parse Incident JSON"]

    ENRICH["Threat Enrichment"]

    subgraph INTEL["Threat Intelligence"]
        direction LR
        VT["VirusTotal"]
        ABUSE["AbuseIPDB"]
    end

    EMAIL["SOC Email"]

    APPROVAL["Human Approval"]

    AZURE["Azure Automation"]

    subgraph RESPONSE["Containment Actions"]
        direction LR
        FIREWALL["Block Malicious IP"]
        AD["Disable AD User"]
    end

    COMPLETE["Incident Contained"]

    ALERT --> WEBHOOK
    WEBHOOK --> PARSE

    PARSE --> ENRICH
    ENRICH --> VT
    ENRICH --> ABUSE

    PARSE --> EMAIL

    VT --> APPROVAL
    ABUSE --> APPROVAL
    EMAIL --> APPROVAL

    APPROVAL --> AZURE

    AZURE --> FIREWALL
    AZURE --> AD

    FIREWALL --> COMPLETE
    AD --> COMPLETE