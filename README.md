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

### Core Technical Features

#### 🎵 **Pluggable AI Music Engine**
- Production: MusicGen (Meta) via Replicate API
- Development: Mock generator for rapid testing
- Extensible architecture for Riffusion, Suno, Diff-Singer
- Seamless engine swapping without pipeline disruption

#### 🔒 **Stateless Access Control**
- Anonymous user identification via MD5(IP + User-Agent)
- Daily rate limiting 
- Automated daily reset system
- Priority queuing for paid credits

#### 💳 **Integrated Monetization**
- Stripe Checkout with webhook validation
- Pay-per-use billing model
- Explicit pipeline decisions (ALLOW/BLOCK)
- No traditional login required

#### 🤖 **Automated Distribution**
- Telegram Bot API integration
- Multi-channel ready architecture (Instagram, X)
- Automated media upload and messaging
- Centralized logging and tracking

### Technical Stack

| Layer | Technologies |
|-------|--------------|
| **Backend** | Python, Flask, Agent Architecture |
| **Frontend** | Vanilla JS, HTML5, CSS Grid/Flex |
| **AI/ML** | MusicGen (Replicate API), Pluggable Engine System |
| **Payments** | Stripe Checkout, Webhooks |
| **Storage** | JSON file-based (PostgreSQL/Supabase ready) |
| **Infrastructure** | Scheduled pipeline (cron/Task Scheduler) |

### Production Status
- ✅ End-to-end pipeline validated
- ✅ Modular architecture ready for scaling
- ✅ Stateless persistence system
- ✅ Centralized logging with full traceability
- ✅ Production-ready MVP

### Roadmap
- Multi-platform distribution expansion
- Relational database migration
- Additional AI music engines
- Integrated analytics dashboard
- Public API for third-party integrations

---

**Architecture:** Decoupled Agent-Based System  
**Availability:** 24/7 automated pipeline  
**Extensibility:** Plug-and-play modules without refactoring
  

<p align="center">
  &copy; <a href="https://www.linkedin.com/in/arthur-vesaro-798318239/" target="_blank" rel="noopener noreferrer">
    Arthur Vesaro
  </a>
</p>