Section: Cover and core mental model
Claim: Desktop computer use is a routed control problem: choose the richest available interface and fall back to pixels only when semantics disappear.
Source: User request and prior conversation; Microsoft UI Automation tree documentation; W3C platform accessibility mappings.

Section: The control-surface tier list
Claim: Native APIs and structured interfaces are most reliable, while raw coordinates are the last resort; deterministic keyboard macros belong above vision when they are observable and verified.
Source: User request and prior conversation.

Section: The computer-use equivalent of the DOM
Claim: The desktop analogue of the DOM is the operating system accessibility tree; pixels are observations, and coordinates are actuator targets.
Source: Microsoft UI Automation tree documentation; W3C Core Accessibility API Mappings; freedesktop.org AT-SPI2.

Section: Perfect the CLI-first lane
Claim: The practical path from partial coverage toward complete coverage is to perfect a bounded set of eligible workflows using lifecycle adapters, app-native CLIs, generated harnesses, and typed contracts.
Source: User request; CLI-Anything official repository.

Section: Vim and keyboard pipelines are reusable nodes
Claim: Vim-style key sequences are strong automation primitives when packaged as stateful, observable, idempotent nodes rather than used as blind navigation.
Source: User request and prior conversation.

Section: Small local models should route, not improvise
Claim: A sub-1GB local model is best used for classification, slot filling, and tool selection over a validated catalog; deterministic code executes and verifies the action.
Source: User request and current design proposal.

Section: The discrete computer-use pipeline
Claim: A complete owner-controlled system needs observe, normalize, route, plan, validate, act, verify, recover, and log stages, with explicit lane escalation.
Source: User request and prior conversation.

Section: Build roadmap and scorecard
Claim: Coverage should be measured per workflow and lane, replacing the unverified 40% estimate with a benchmark that shows how much of the user's real workload is handled locally and deterministically.
Source: User request; analytical recommendation.

Section: Quick reference and sources
Claim: A compact decision ladder, vocabulary, and authoritative references make the architecture easier to remember and implement.
Source: Microsoft Learn, W3C, freedesktop.org, CLI-Anything GitHub.
