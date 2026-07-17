flowchart TB

    INTERNET((Internet))

    subgraph AZURE["Microsoft Azure"]
        subgraph RG["Resource Group<br/>enterprise-soc-rg"]

            subgraph VNET["Virtual Network<br/>enterprise-soc-vnet<br/>10.0.0.0/16"]

                NSG["Network Security Group<br/>enterprise-soc-nsg<br/><br/>Allows:<br/>• RDP<br/>• SSH<br/>• HTTPS"]

                subgraph SUBNET["Subnet<br/>10.0.0.0/24"]

                    DC["dc01<br/>Windows Server 2025<br/>AD DS + DNS<br/>10.0.0.4"]

                    WIN11["win11<br/>Windows 11 Pro<br/>Domain Endpoint<br/>10.0.0.5"]

                    WAZUH["wazuh01<br/>Ubuntu Server<br/>Wazuh Manager<br/>Indexer & Dashboard<br/>10.0.0.6"]

                end
            end
        end
    end

    INTERNET -->|"RDP"| DC
    INTERNET -->|"RDP"| WIN11
    INTERNET -->|"SSH / HTTPS"| WAZUH

    WIN11 -->|"DNS & Authentication"| DC

    DC -->|"Windows Security Logs"| WAZUH

    WIN11 -->|"Sysmon<br/>Security<br/>PowerShell<br/>FIM"| WAZUH