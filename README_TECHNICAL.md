# CloudMusic Generator

## 🎯 Objective
Autonomous pipeline for AI music generation with IP & User-Agent access control, usage management, and automated social media publishing.

---

## Environment Setup
Developed in **Python 3.8**, compatible with **3.10** (5/5) and **3.11** (5/3)

–> **venv** Virtual environment to isolate project dependencies

---

## Project Structure


CloudWalkMusic/
├─ venv/                      # Ambiente Python isolado
├─ agents/                    # Agentes do sistema
│  ├─ __init__.py
│  ├─ music_agent.py          # Orquestrador de geração musical
│  ├─ music_agent_mock.py     # Gerador mock (teste e validação do pipeline)
│  ├─ music_agent_musicgen.py # Gerador real via MusicGen
│  ├─ billing_agent.py        # Controle de acesso / monetização
│  └─ marketing_agent.py      # Divulgação e teasers
├─ storage/                   # Arquivos gerados (músicas e prompts)
│  ├─ music_001.wav
│  └─ last_prompt.txt
├─ data/                      # Dados do sistema (ex: banco de faturamento)
│  └─ billing_db.json
├─ app/                       # Aplicação web
│  └─ static/                 # Arquivos estáticos
│     ├─ favicon.svg
│     ├─ styles.css
│     └─ script.js
├─ templates/                 # Templates HTML
│  ├─ index.html
│  └─ main.py
├─ docs/                      # Documentação adicional
│  └─ scheduler.md
├─ logger.py                  # Configuração de logs
├─ pipeline.log               # Logs de execução do pipeline
├─ run_pipeline.py            # Orquestração end-to-end do pipeline
├─ requirements.txt           # Dependências do projeto
└─ README.md                  # Documentação principal


**Architecture**

Agent-based pipeline with defined responsibilities:

**MusicAgent → Storage → BillingAgent → MarketingAgent**

---

## ✅ Project Status
*End-to-end autonomous pipeline*  
Agent-oriented and decoupled architecture  
Pluggable music generation engine

---

## 🎵 Music Generation Engine
| State        | Technology                             | Purpose                        |
|--------------|----------------------------------------|--------------------------------|
| **Test**     | Mock generator (.wav)                   | Pipeline validation             |
| **Production**| MusicGen (Meta) via Replicate API     | Real music generation           |
| **Extensible**| Riffusion, Suno, Diff-Singer          | Future flexibility              |

> The AI engine is abstracted and consumed via API (Replicate), allowing model swaps without impacting the pipeline or downstream agents.

---

## Autonomous Execution
- Run via `run_pipeline.py`
- Ready for recurring scheduling (cron / Task Scheduler)

---

## Technical Validation
- Agent-based pipeline (MusicAgent, BillingAgent, MarketingAgent)
- Standardized interface (`run()`) between agents
- End-to-end execution validated
- Real .wav audio generation (16-bit PCM)
- Artifacts persisted in `storage/`

> The mock generator is used for testing and validation without external model dependencies.

---

## Engine Selection
**Dynamic selection via configuration** (`USE_MUSICGEN = True  # True = AI | False = mock`)  
- **Mock:** Fast tests and CI  
- **MusicGen (Replicate):** Real AI generation  

> Engine swap does not change pipeline logic, ensuring flexibility and extensibility.

---

## Scheduling & Logging
- Pipeline ready for automatic execution  
- Centralized logs in `pipeline.log`  
- Traceability for:  
  - Execution  
  - Music generation  
  - Billing  
  - Publishing

---

## Marketing Agent
- Automated publishing via Telegram Bot API  
- Automated media upload and messaging  
- Architecture ready for multiple channels (Instagram, X)

---

## Billing Agent
**Login-free monetization**  
Rate limiting + pay-per-use  

**Rules:**  
- Daily free: 4 generations  
- Automatic daily reset  
- Paid credits prioritized  
- Explicit decision in pipeline (ALLOW | BLOCK)

---

## Access Control
- Stateless identification via MD5 hash(IP + User-Agent)  
- Persisted in JSON (`billing_db.json`)  
- Ready for relational database migration

---

## Tech Stack
**Frontend:** HTML, CSS Grid/Flex, Vanilla JS  
**Backend:** Flask, subprocess, hashlib  
**AI:** MusicGen via Replicate API (pluggable)  
**Payments:** Stripe Checkout + Webhooks  
**Persistence:** JSON file-based (ready for Supabase/PostgreSQL)
