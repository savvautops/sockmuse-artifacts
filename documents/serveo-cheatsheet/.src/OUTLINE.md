Section: Serveo in one minute
Claim: Serveo temporarily publishes a local web service by carrying public requests through an outbound SSH reverse tunnel.
Source: Serveo official site and documentation; requesting conversation.

Section: What this approval allows
Claim: Approval covers one temporary outbound SSH connection and public forwarding to the Snake dashboard, not general access to the VM.
Source: Requesting conversation and SSH reverse-forwarding behavior documented by Serveo.

Section: The traffic path
Claim: Browser traffic reaches Serveo over HTTPS, then crosses the SSH tunnel to the selected localhost port; the application makes its own downstream model calls.
Source: Serveo official documentation; requesting conversation.

Section: Risks and safeguards
Claim: Encryption in transit does not make a public URL private; anyone with the URL can reach an unauthenticated dashboard, and the relay sits in the request path.
Source: Serveo official docs on public URLs, interstitials, SSH/TLS; protocol implications.

Section: Operator cheatsheet
Claim: The tunnel exists only while the SSH process runs and can be stopped immediately; local service and tunnel status can be checked independently.
Source: OpenSSH behavior and Serveo official documentation.

Section: Approval boundary
Claim: A narrow approval should permit only the named dashboard, avoid secrets, and end with the session.
Source: Requesting conversation and security analysis.
