Section: Executive decision
Claim: GitHub can serve as the durable agent coordination layer, but it should be split into public and private lanes and should never carry raw secrets.
Source: User request and requesting conversation; GitHub webhook, authentication, and credential-security documentation.

Section: Scope and design principles
Claim: The bus coordinates work and references artifacts; it does not replace source control, a secret manager, or the human control channel.
Source: User's SAO/Telegram/n8n architecture in requesting context.

Section: Architecture
Claim: A two-repository topology with a single webhook ingress and policy-aware router gives separation without unnecessary infrastructure.
Source: Design synthesis.

Section: Message and state model
Claim: A small versioned envelope in issue bodies and comments makes messages both machine-parseable and readable to humans.
Source: GitHub Issues/comments API and webhook event model.

Section: Public lane
Claim: Public issues are suitable for non-sensitive coordination when every message is treated as publishable and secret-scanned.
Source: User request; GitHub secret-scanning documentation.

Section: Private lane
Claim: Private repos protect proprietary coordination through access control, while external secret references or recipient encryption are required for credentials and highest-sensitivity data.
Source: GitHub credential-security guidance; threat-model analysis.

Section: Identity and authorization
Claim: A GitHub App is the production identity; fine-grained PATs are an acceptable pilot mechanism with strict repository and permission scope.
Source: GitHub App and fine-grained token documentation.

Section: Delivery, reliability, and idempotency
Claim: Webhooks should be the primary transport, with signature validation, rapid acknowledgement, durable queuing, delivery-ID deduplication, and low-frequency reconciliation polling.
Source: GitHub webhook documentation and troubleshooting guidance.

Section: CLI/API contract
Claim: A minimal set of gh and REST operations can implement send, receive, acknowledge, complete, and fail semantics.
Source: GitHub REST API documentation and design synthesis.

Section: Threat model and controls
Claim: Repository privacy alone does not solve leakage, prompt injection, replay, compromised agents, or destructive autonomy; controls must be enforced at ingress and execution.
Source: Security design analysis.

Section: Operations and governance
Claim: Human-readable labels, audit conventions, retention rules, metrics, and an emergency stop make the bus governable.
Source: User's SAO governance model and design synthesis.

Section: Rollout plan
Claim: A staged pilot proves protocol and security assumptions before adding more agents or encrypted payloads.
Source: Design synthesis.

Section: Decisions and open questions
Claim: The document makes a clear baseline recommendation while isolating a small set of implementation choices for Nelson.
Source: User request and design synthesis.

Section: References
Claim: The key GitHub platform assumptions are traceable to official GitHub documentation.
Source: Official GitHub documentation URLs verified via web search on 2026-09-25.
