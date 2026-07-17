flowchart TB

    DOMAIN["enterprise.local<br/>Active Directory Domain"]

    subgraph CORE["Domain Services"]
        direction LR
        DC["dc01<br/>Windows Server 2025<br/>Domain Controller"]
        DNS["DNS Server"]
        GPO["Default Domain Policy<br/>Password & Lockout Policies"]
    end

    DOMAIN --> DC
    DC --> DNS
    DOMAIN --> GPO

    subgraph OUS["Organizational Unit Structure"]
        direction TB

        subgraph DEPT_OUS_1["Department OUs"]
            direction LR
            IT["IT OU<br/>John Carter<br/>Sarah Mitchell"]
            HR["HR OU<br/>Emma Wilson<br/>Olivia Brown"]
            FIN["Finance OU<br/>Daniel Moore<br/>Sophia Davis"]
        end

        subgraph DEPT_OUS_2["Additional Department OUs"]
            direction LR
            SALES["Sales OU<br/>Ethan Taylor<br/>Mia Anderson"]
            OPS["Operations OU<br/>Noah Thomas<br/>Ava Jackson"]
        end

        subgraph RESOURCE_OUS["Resource OUs"]
            direction LR
            SERVERS["Servers OU"]
            WORKSTATIONS["Workstations OU<br/>win11"]
            SERVICE["Service Accounts OU<br/>soar.test"]
        end
    end

    subgraph GROUPS["Security Groups"]
        direction TB

        subgraph GROUP_ROW_1["Department Groups"]
            direction LR
            ITADMINS["IT-Admins"]
            HRUSERS["HR-Users"]
            FINUSERS["Finance-Users"]
        end

        subgraph GROUP_ROW_2["User and Support Groups"]
            direction LR
            SALESUSERS["Sales-Users"]
            OPSUSERS["Operations-Users"]
            HELPDESK["Helpdesk"]
        end

        subgraph GROUP_ROW_3["Privileged Groups"]
            direction LR
            SERVERADMINS["Server-Admins"]
        end
    end

    DOMAIN --> IT
    DOMAIN --> HR
    DOMAIN --> FIN
    DOMAIN --> SALES
    DOMAIN --> OPS
    DOMAIN --> SERVERS
    DOMAIN --> WORKSTATIONS
    DOMAIN --> SERVICE

    DOMAIN --> ITADMINS
    DOMAIN --> HRUSERS
    DOMAIN --> FINUSERS
    DOMAIN --> SALESUSERS
    DOMAIN --> OPSUSERS
    DOMAIN --> HELPDESK
    DOMAIN --> SERVERADMINS

    WIN11["win11<br/>Windows 11 Pro<br/>Domain-Joined Endpoint"]

    WORKSTATIONS --> WIN11
    WIN11 -->|"DNS Queries"| DNS
    WIN11 -->|"Kerberos Authentication"| DC
    GPO -->|"Domain Policy Applied"| WIN11