<h1 align="center">CloudMusic</h1>
<h3 align="center">AI-powered loops & assets for DJs/producers</h3>

<p align="center">
  <em>Autonomous music generation platform with usage limits, billing, and automated distribution.</em>
</p>

---

<p align="center">
  <img src="https://github.com/user-attachments/assets/05fde367-f9a2-4a05-a6bd-c401d21d0cd8" width="800" alt="CloudMusic Dashboard Screenshot" />
  <br>
  <em>Screenshot of the main dashboard showing guided & advanced modes, and player interface.</em>
</p>

## Overview
End-to-end pipeline built with a decoupled agent architecture to generate music, enforce access rules, and distribute releases automatically.

Designed as an MVP with production-ready structure and extensibility.

## Architecture
Agent-based pipeline:

MusicAgent → Storage → BillingAgent → MarketingAgent

Each agent is isolated, testable, and replaceable.

## Key Features
- Autonomous music generation (pluggable engine)
- Usage limits with daily reset (IP-based)
- Pay-per-use billing (Stripe Checkout + webhooks)
- No login, no traditional database (file-based persistence)
- Modular pipeline with logging

## Tech Stack
- Backend: Python, Flask
- Frontend: Vanilla JS, HTML, CSS
- AI: MusicGen (pluggable, mock supported)
- Payments: Stripe
- Storage: File-based (JSON, audio files)

## Status
Functional MVP  
End-to-end pipeline validated  
Ready for deployment and scaling

<p align="center">
  &copy; Arthur Vesaro
</p>

