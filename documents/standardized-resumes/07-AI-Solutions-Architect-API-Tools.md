# Nelson Tsavnande

Winnipeg, MB, Canada | 204-962-8872 | nelsontsavnande@gmail.com  
Portfolio: https://savvstudio.com | GitHub: https://github.com/savvops | LinkedIn: https://www.linkedin.com/in/nelson-tsavnande-94381a2b4/

## AI Solutions Architect / Automation Engineer

## Summary

I design and build practical AI systems that connect models, APIs, browser tools, messaging, local services, and human operators. As founder of Savv Studio / SavvOps, I have built a Telegram-operated agent command plane, multi-provider AI products, n8n workflows, local/cloud model routing, OAuth-connected tools, and commercial webhook/licensing flows. My support background at IntouchCX keeps the architecture grounded in how people actually report problems, follow instructions, recover from errors, and decide when an automated action needs a human.

## Architecture & Engineering Skills

- **AI solution design:** requirements discovery, workflow mapping, rapid prototyping, model selection, prompt workflows, RAG concepts, provider abstraction, local/cloud fallback, and cost-aware architecture.
- **Models and providers:** OpenAI, Anthropic, Gemini, OpenRouter, Ollama, LM Studio, hosted APIs, local models, streaming responses, and bring-your-own-key patterns.
- **Agent and automation systems:** n8n, Telegram bots, tool registries, task routing, durable job state, scheduled work, retries, health checks, watchdogs, approval gates, evidence checkpoints, and recovery paths.
- **APIs and integrations:** REST APIs, webhooks, OAuth-connected tools, Telegram Bot API, GitHub tooling, Cloudflare services, Composio connectors, Gumroad webhooks, and browser automation.
- **Application engineering:** TypeScript, JavaScript, Python, React, Astro, Node.js, Chrome Manifest V3, Electron, Puppeteer, Playwright, HTML/CSS, and SQL basics.
- **Cloud and operations:** Cloudflare Pages, Workers/KV concepts, Tunnels, Docker basics, Linux/WSL, Git/GitHub, local development environments, logging, redacted audit events, and technical documentation.

## Selected Architecture Work

### SavvOps / SAO - Agent Command Plane

- Built a Telegram-controlled environment that routes goals to AI workers and exposes provider CLIs, n8n workflows, browser tools, local files, processes, scheduled jobs, and health checks through consistent command patterns.
- Designed durable job-state and control patterns around unreliable workers: bounded retries, input requests, capacity checks, execution ledgers, append-only events, independent verification, and explicit goal review.
- Kept credentials and consequential actions behind scoped access and human approval boundaries instead of copying secrets into every worker or allowing silent execution.
- Structured the system so provider, interface, and worker implementations can change without rewriting the whole workflow.

### Nerdbot - Multi-Provider Browser AI Assistant (https://chromewebstore.google.com/detail/nerdbot/oegoeflmcbahliaahlameajidnhlpiog)

- Built and published a Chrome Manifest V3 side-panel assistant with React, TypeScript, Vite, Tailwind, streaming chat, local settings, chat history, pinned messages, and provider configuration.
- Integrated Gemini, OpenAI, OpenRouter, Anthropic, Ollama, and LM Studio behind a provider-selection layer with fast/quality modes and local-provider options.
- Added active-page text, selected content, screenshots, multi-tab context, local knowledge/RAG concepts, and custom skills while keeping context sharing explicit.
- Designed privacy-aware BYOK behavior where provider credentials remain local and page content is included only when the user chooses it.

### SavvOps Automation & API Integration Collection

- Built reusable integrations across Telegram, n8n, AI providers, GitHub tooling, Cloudflare services, local models, browsers, files, and process operations instead of coupling each workflow to one interface.
- Connected LinkedIn through Composio OAuth, verified the connection with a read-only profile action, and kept publishing disabled until explicitly approved.
- Built human-in-the-loop patterns for routing, research, reminders, summaries, operational checks, and supervised actions, including evidence that shows whether a task actually completed.

### AI Stock Content & Metadata Pipeline (https://stock.adobe.com/contributor/211451851/Nelson)

- Built repeatable AI-assisted workflows for generation, quality review, metadata, and upload readiness across 30,000+ generated assets and approximately 10,000 accepted/live assets; created title, description, and keyword tooling while preserving human quality control.

### HtmlToMp4 Pro - Product, Webhook & Licensing Architecture (https://htmltomp4.com)

- Built an Electron and CLI product that converts HTML/CSS/JavaScript animations into MP4/WebM with Puppeteer and FFmpeg; designed Gumroad webhook and Cloudflare Workers/KV concepts for machine activation, validation, administrative controls, recovery, and Windows distribution.

## Experience

### Founder & Lead Developer - Savv Studio / SavvOps
*Remote | January 2023 - Present*

- Translate unclear business and workflow problems into bounded architectures, technical options, working prototypes, verification rules, and operating documentation.
- Build AI automations, browser products, websites, API integrations, desktop tools, and local/cloud agent systems from requirements through testing and support.
- Explain architecture choices, constraints, failure paths, and cost trade-offs in plain language for non-technical users and small-business clients.
- Own implementation across TypeScript/JavaScript interfaces, Python automation, Cloudflare delivery, n8n orchestration, browser tooling, and local AI environments.

### Customer Technical Support & Operations Representative - IntouchCX
*Remote / Winnipeg, MB | March 2025 - May 2026*

- Supported assigned client programs through chat, phone, CRM/ticket workflows, escalation paths, and documented quality requirements.
- Resolved customer issues with clear written communication, structured troubleshooting, careful documentation, and safe escalation when more investigation was needed.
- Brought the support perspective into solution design: clearer intake, better error states, understandable instructions, visible next steps, and recoverable workflows.
- Role ended when the client program shut down; available immediately.

### Contract Web Developer & Seasonal Operations Support - Window Guys Winnipeg
*Winnipeg / Remote | Seasonal contracts, 2024 - Present*

- Supported website delivery, lead-generation workflows, customer and sales data cleanup, and seasonal operations for a local service business.
- Turned practical operating needs into clearer customer-facing information, quote-request paths, and repeatable web updates.

### Customer Service Representative - 24/7 Intouch, Lyft Support
*Winnipeg, MB | November 2017 - April 2019*

- Resolved rider and driver inquiries through email and phone while following CRM/ticketing, escalation, and service-quality procedures.
- Documented issues and next steps clearly in a high-volume support environment.

## Education

**Bachelor of Science in Mathematics and Physics**  
University of Manitoba, Winnipeg, MB | May 2023

Relevant study: data analysis, linear algebra, statistics, computational programming/Python, mathematical modeling, and physics problem-solving.
