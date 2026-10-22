# SkillForge 🛠️

**SkillForge** is a dual-engine developer copilot built for Hacktoberfest contributors. It solves the massive friction new developers face when joining open-source projects by instantly generating onboarding guides, authoring project-specific agent skills, and intelligently triaging terminal errors using a hybrid local/cloud architecture.

## 🎯 Features
* **Millisecond Log Triage:** Uses a local System One model (**Laya**) to classify terminal errors instantly without API latency.
* **Auto-Skill Generation:** Automatically authors `agentskills.io` compliant `.agents/skills/SKILL.md` files.
* **Codebase Onboarding:** Generates a structured `NEWBIE_GUIDE.md` outlining project entry points.
* **Atomic File Safety:** Utilizes POSIX-safe atomic writes to ensure agent state updates never corrupt repository files.

## 🚀 How to Run It
1. Clone the repository and navigate into it:
   ```bash
   git clone [https://github.com/vicky-404/skillforge.git](https://github.com/vicky-404/skillforge.git)
   cd skillforge
   ```

1. Install dependencies using uv:
```bash
uv sync
```

2. Set up your environment variables:
```bash
cp .env.example .env
# Add your GROQ_API_KEY inside .env
```

3. Run commands via the CLI:

- - Triage a log file: uv run main.py debug test_error.log
- - Generate onboarding guide: uv run main.py onboard
- - Generate agent skills: uv run main.py skills

## 🧠 Dual-Engine AI Architecture
SkillForge separates fast deterministic decision-making from heavy text generation:

1. System One (Local Guardrails & Triage): Laya

- - Role: Millisecond error classification running 100% locally on your machine.
- - Parameters: 421M (Open-Weight)
- - License: Apache 2.0 License

2. System Two (Generation): Qwen2.5-Coder (via Groq / DigitalOcean Gradient AI)

- - Role: Heavy text generation for authoring Markdown guides and SKILL.md rules.

- - License: Qwen License / Apache 2.0

## 📦 Key Dependencies
- uv - Fast Python package manager

- laya - Local System One inference engine[cite: 6]

- langchain-groq - Cloud LLM integration

## 📄 License
This project is open source and licensed under the MIT License[License].
