# ⚡ LLM Red Team Harness

> Automated LLM red-teaming tool that fires prompt injection & jailbreak attacks against local models, maps findings to OWASP LLM Top 10 (2025), and generates a professional HTML report.

Built by [@ShaheerSec](https://linkedin.com/in/shaheer-hussain-cybersec) — AI Security / LLM Red-Team Analyst

---

## What This Does

Most people test LLMs manually — type a prompt, see what happens, move on. This tool automates the entire red-team process:

1. Loads a library of attack prompts (prompt injection, jailbreaks, privilege escalation, data extraction)
2. Fires every prompt against a local model running in Ollama
3. Analyzes each response — did the model comply or resist?
4. Maps every finding to the official OWASP LLM Top 10 (2025) vulnerability list
5. Generates a dark-themed HTML report with risk score, severity badges, and full prompt/response pairs

No API keys. No external services. Runs fully offline on your own machine.

---

## Sample Report Output

| Metric                | Result |
| --------------------- | ------ |
| Total Attacks Fired   | 30     |
| Vulnerabilities Found | 4      |
| Attacks Resisted      | 26     |
| Risk Score            | 13.3%  |

**Key Finding:** `llama3.2:1b` resisted direct jailbreaks but failed on indirect attacks including academic framing (LLM01) and gradual escalation techniques (LLM02) — demonstrating that smaller models are more vulnerable to multi-step social engineering than brute-force instruction overrides.

---

## Attack Categories Covered

| Attack Type                                     | OWASP LLM ID | Severity |
| ----------------------------------------------- | ------------ | -------- |
| Prompt Injection — Direct Override              | LLM01        | Critical |
| Prompt Injection — Token Smuggling (Base64)     | LLM01        | Critical |
| Prompt Injection — Leetspeak Filter Bypass      | LLM01        | Critical |
| Prompt Injection — Indirect via Document        | LLM01        | Critical |
| Prompt Injection — Nested Injection             | LLM01        | Critical |
| Jailbreak — Persona Hijack (DAN)                | LLM02        | High     |
| Jailbreak — Fictional Framing Escalation        | LLM02        | High     |
| Jailbreak — Many Shot Repetition                | LLM02        | High     |
| Jailbreak — Gradual Escalation                  | LLM02        | High     |
| Jailbreak — Academic Framing                    | LLM02        | High     |
| Jailbreak — Emotional Manipulation              | LLM02        | High     |
| Jailbreak — Competing Objectives                | LLM02        | High     |
| Jailbreak — Hypothetical AI (ARIA)              | LLM02        | High     |
| Privilege Escalation — Fake System Prompt       | LLM08        | Critical |
| Privilege Escalation — Admin Override           | LLM08        | Critical |
| Privilege Escalation — Jailbreak via Correction | LLM08        | Critical |
| Data Extraction — System Prompt Extraction      | LLM06        | High     |
| Data Extraction — PII and Memory Probing        | LLM06        | High     |

---

## Tech Stack

- **Python 3.10+**
- **Ollama** — local LLM inference (no API keys required)
- **Jinja2** — HTML report templating
- **python-dotenv** — environment configuration
- **OWASP LLM Top 10 (2025)** — vulnerability mapping framework

---

## Quick Start

**1. Clone the repo**

```bash
git clone https://github.com/Shaheer-Cybersec/llm-redteam-harness.git
cd llm-redteam-harness
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Install Ollama and pull a target model**

Download Ollama from [ollama.com](https://ollama.com) then run:

```bash
ollama pull llama3.2:1b
```

**4. Configure your environment**

```bash
cp .env.example .env
```

Edit `.env` and set your target model:

```
OLLAMA_MODEL=llama3.2:1b
OLLAMA_BASE_URL=http://localhost:11434
```

**5. Run the harness**

```bash
python main.py
```

**6. Open your report**

Report is saved to `reports/report_<timestamp>.html` — open in any browser.

---

## Project Structure

```
llm-redteam-harness/
├── main.py                   # Entry point — runs the full pipeline
├── harness/
│   ├── runner.py             # Fires prompts at the target model
│   ├── parser.py             # Analyzes responses, maps to OWASP LLM Top 10
│   └── report_gen.py         # Generates the HTML report
├── prompts/
│   └── basic_injection.txt   # Attack prompt library (30 prompts across 6 categories)
├── results/                  # Raw JSONL output — one file per run
├── reports/                  # Generated HTML reports — one file per run
├── requirements.txt
└── .env.example
```

---

## How the Pipeline Works

```
prompts/*.txt
     │
     ▼
runner.py  ──►  Ollama (local model)  ──►  results/*.jsonl
                                                  │
                                                  ▼
                                            parser.py
                                          (OWASP mapping +
                                          outcome detection)
                                                  │
                                                  ▼
                                          report_gen.py
                                                  │
                                                  ▼
                                         reports/*.html
```

---

## Adding Your Own Prompts

Add prompts to `prompts/basic_injection.txt` using this format:

```
# CATEGORY: Your Attack Type — Subcategory
Your attack prompt goes here on the next line.
```

The category string automatically maps to OWASP LLM Top 10. Supported categories:

| Category String        | Maps To          |
| ---------------------- | ---------------- |
| `Prompt Injection`     | LLM01 — Critical |
| `Jailbreak`            | LLM02 — High     |
| `Data Extraction`      | LLM06 — High     |
| `Privilege Escalation` | LLM08 — Critical |

---

## Tested Against

| Model       | Size   | Result                                       |
| ----------- | ------ | -------------------------------------------- |
| llama3.2:1b | 1.3 GB | 30 attacks — 4 vulnerable (13.3% risk score) |

Runs fully offline — no data leaves your machine.

---

## Roadmap

- [ ] Multi-model comparison — test same prompts across multiple models side by side
- [ ] Garak integration — extended probe library with 100+ attack probes
- [ ] MITRE ATLAS mapping alongside OWASP LLM Top 10
- [ ] LLM-as-judge scoring — use a second model to evaluate response safety
- [ ] JSON export for integration with security pipelines and SIEM tools
- [ ] CI/CD integration — run red-team suite automatically on model updates

---

## Disclaimer

This tool is built for **educational and authorized security research purposes only**. Only test models you own or have explicit permission to evaluate. Do not use against production systems without written authorization.

---

## Author

**Shaheer Hussain (@ShaheerSec)**  
AI Security / LLM Red-Team Analyst  
[LinkedIn](https://linkedin.com/in/shaheer-hussain-cybersec) · [GitHub](https://github.com/Shaheer-Cybersec) · [TryHackMe](https://tryhackme.com/p/cicada664)
