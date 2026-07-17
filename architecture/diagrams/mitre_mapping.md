flowchart LR

    EVENTS["Security Events<br/>Windows Events, Sysmon, PowerShell and FIM"]

    RULES["Wazuh Detection Rules<br/>Rule Matching and Correlation"]

    MITRE["MITRE ATT&CK Context<br/>Applied Where Supported by Rule Metadata"]

    BRUTE["T1110<br/>Brute Force"]

    OTHER["Additional Techniques<br/>Based on Validated Rule Mappings"]

    DASH["Wazuh Dashboard<br/>MITRE ATT&CK View"]

    ANALYST["SOC Analyst<br/>Investigation and Triage"]

    EVENTS --> RULES
    RULES --> BRUTE
    RULES --> OTHER

    BRUTE --> MITRE
    OTHER --> MITRE

    MITRE --> DASH
    DASH --> ANALYST
