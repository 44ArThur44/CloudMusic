#  CloudMusic Generator

## 🎯 Objetivo
Pipeline autônomo para geração de música com I.A., com controle de acesso vai endereço IP e User-Agent, gestão de consumo e automação de publicações para redes sociais.

---

## Configuração do Ambiente
Desenvolvido em **Python 3.8**, com compatibilidade em Python **3.10** (5/5) e **3.11.** (5/3)

–> **venv** Ambiente virtual para isolar as dependências do projeto

---

##  Estrutura do Projeto

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

**Arquitetura**

Pipeline baseado em agentes, com responsabilidades definidas:

**MusicAgent → Storage → BillingAgent → MarketingAgent**


## ✅ Status do Projeto
*Pipeline autônomo end-to-end*
Arquitetura orientada a agentes e desacoplada  
Motor de geração de música plugável

---

## 🎵 Motor de Geração de Música
| Estado        | Tecnologia                             | Propósito                     |
|---------------|----------------------------------------|-------------------------------|
| **teste**     | Gerador mock (.wav)                    | Validação do pipeline         |
| **Produção**  | MusicGen (Meta) via Replicate API      | Geração real                  |
| **Extensível**| Riffusion, Suno, Diff-Singer           | Flexibilidade futura          |

> O motor de IA é abstraído e consumido via API (Replicate), permitindo troca de modelos sem impacto no pipeline ou nos agentes downstream.

---
## Execução Autônoma
- Execução via `run_pipeline.py`
- Preparado para agendamento recorrente (cron / Task Scheduler)

---

## Validação Técnica
- Pipeline baseado em agentes (MusicAgent, BillingAgent, MarketingAgent)
- Interface padronizada (`run()`) entre agentes
- Execução end-to-end validada
- Geração real de áudio .wav (PCM 16-bit)
- Artefatos persistidos em `storage/`

> O gerador mock é utilizado para testes e validação sem dependência de modelos externos.

---

## Seleção de Motor
**Seleção dinâmica via configuração** (USE_MUSICGEN = True  # True = IA | False = mock) 
- **Mock:** testes rápidos e CI
- **MusicGen (Replicate):** geração real via IA

> A troca de motor não altera a lógica do pipeline, garantindo flexibilidade e extensibilidade.

---

## Agendamento & Logging
- Pipeline preparado para execução automática
- Logs centralizados em `pipeline.log`
- Rastreabilidade de:
  - Execução
  - Geração de música
  - Billing
  - Publicação

---

## Marketing Agent
- Publicação automática via Telegram Bot API
- Upload de mídia e mensagens automatizadas
- Arquitetura preparada para múltiplos canais (Instagram, X)

---

## Billing Agent
**Monetização sem login**  
Rate limiting + pay-per-use

**Regras:**
- Free diário: 4 gerações
- Reset automático diário
- Créditos pagos priorizados
- Decisão explícita no pipeline (ALLOW | BLOCK)

---

## Controle de Acesso
- Identificação stateless via hash MD5(IP + User-Agent)
- Persistência em JSON (`billing_db.json`)
- Pronto para migração para banco relacional

---

## Stack Técnica
**Frontend:** HTML, CSS Grid/Flex, Vanilla JS  
**Backend:** Flask, subprocess, hashlib  
**IA:** MusicGen via Replicate API (plugável)  
**Pagamentos:** Stripe Checkout + Webhooks  
**Persistência:** JSON file-based (pronto para Supabase/PostgreSQL)