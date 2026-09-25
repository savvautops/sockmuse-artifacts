Section: Oracle Cloud in one picture
Claim: OCI becomes manageable once tenancy, region, compartment, network, instance, and volume are understood as a containment chain.
Source: Oracle OCI documentation on free resources, networking, and compute.

Section: The full Always Free inventory
Claim: The tenancy can hold up to four free VMs - two A1 Flex instances sharing 2 OCPUs and 12 GB, plus two E2.1.Micro instances - but the 200 GB storage pool can lower the practical count.
Source: Oracle Always Free Resources documentation; current September 2026 allowance supplied in the edit brief.

Section: Nelson's VM compared with Sock's sandbox
Claim: nelson-vm-01 has more memory, much more disk, and dedicated Arm cores, while Sock's sandbox uses shared x86_64 vCPUs and has broader legacy-binary compatibility.
Source: Machine specifications and provisioning configuration supplied in the edit brief.

Section: A safe first VM recipe
Claim: A single Ubuntu A1 VM in a public subnet, with key-based SSH and narrowly scoped ingress, is the simplest practical starter configuration.
Source: Oracle launch, key-pair, networking, and compute-security documentation.

Section: Connect and bootstrap
Claim: A short, repeatable SSH and package setup sequence gets the server usable without weakening authentication.
Source: Oracle Linux instance access and key management documentation; standard Linux commands.

Section: Networking without mystery
Claim: Internet reachability requires the right public IP, route, OCI firewall rule, and OS firewall rule; all layers must agree.
Source: Oracle security rules and SSH troubleshooting documentation.

Section: Operate it day to day
Claim: A small command set covers health, services, logs, disk, updates, transfers, and basic Docker operations.
Source: Standard Linux/systemd/OpenSSH/Docker interfaces; Oracle compute security guidance.

Section: Cost and failure guardrails
Claim: Free-tier users should verify the Always Free label, create budget alerts, back up valuable data, and design for possible idle-instance reclamation.
Source: Oracle Always Free, budgets, boot-volume backup, and security documentation.

Section: Troubleshooting and glossary
Claim: Most beginner failures can be isolated by checking lifecycle state, address, route, cloud firewall, OS firewall, user, key, architecture, and capacity in order.
Source: Oracle SSH troubleshooting and Always Free documentation.

Section: Sources
Claim: The guide is grounded in current Oracle documentation and keeps direct references for re-checking limits and procedures.
Source: Oracle documentation URLs retrieved 2026-09-24.
