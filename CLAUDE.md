# Omni-Route Context Engineering

This `CLAUDE.md` serves as the core rulebook and context layer for the Omni-Route orchestrator, synthesizing best practices from `context-engineering-intro` (context separation), `rulebook-ai` (coding standards enforcement), and `awesome-vibecoding` (agentic skills).

## 1. Project Intelligence

This section defines our source of truth for the project. Do not deviate from these constraints.

### Core Technical Stack
* **Frontend:** Next.js (App Router), React, Tailwind CSS
* **Backend:** FastAPI (Python) orchestrator
* **AI Integration:** Local execution via Ollama using Gemma 4 E4B models
* **Tooling:** Docling (PDF parsing), Whisper.cpp (audio transcription)
* **Database:** PostgreSQL (local Docker container)

### Aesthetic Constraints
* **Design Philosophy:** High-contrast, strictly monochromatic (Black and White).
* **Color Usage:** NO COLORS allowed other than black, white, and grayscale for subtle depth or borders. No gradients.
* **Default Mode:** Primary interface must be Dark Mode default.
* **UI/UX:** Minimalist, functional, accessible.

### Resource & Deployment Constraints
* **Environment:** Offline-first. Avoid external API dependencies or cloud CDN links where local alternatives exist.
* **VRAM Constraint:** Hard constraint of **4GB VRAM** maximum. Models and tooling must be optimized for edge hardware. Memory profiling is mandatory for AI workflows.

## 2. Context Engineering & Separation
Based on `context-engineering-intro`:
* Keep feature-specific context isolated to relevant subdirectories.
* Agents must rely on local context first before hallucinating system dependencies.
* Clear boundaries must be drawn between Frontend execution context, Backend Orchestrator context, and Local Model routing context.
* Use `<context>` XML tags when feeding raw data to LLM interfaces.

## 3. Coding Standards Enforcement
Based on `rulebook-ai`:
* All code must follow strict type-checking (TypeScript for frontend, PyDantic/Type hints for FastAPI).
* Comprehensive docstrings are required for all backend functions and AI routers.
* Standardize on clear structured outputs (JSON). Never rely on unstructured text responses from the local model unless it is purely generative user-facing text.
* Zero tolerance for unhandled exceptions in the orchestrator layer.

## 4. Agentic Skills
Based on `awesome-vibecoding`:
* AI Agents acting within this repository must be proactive in exploring the file tree.
* Agents must verify the outcome of their actions using read-only tools.
* Agents should run local tests and ensure no regressions.
* Practice self-reflection on errors before modifying configurations.

## 5. Vibe Coding Guardrails

Strict XML-structured rules for agentic interactions and code generation.

### Multi-Step Task Verification
<rule>
  <name>Verify-Before-Proceeding</name>
  <description>After any state-modifying action (create, update, delete file), the agent MUST verify the action using `read_file` or `list_files`.</description>
  <enforcement>MANDATORY</enforcement>
</rule>

### Quality Gates
<rule>
  <name>Pre-Commit-Quality-Gate</name>
  <description>Code changes must pass typing checks, formatting checks, and local tests. For AI outputs, ensure JSON schema compliance.</description>
  <enforcement>MANDATORY</enforcement>
</rule>

### Three-Fail Fallback Protocol
<rule>
  <name>Three-Fail-Fallback</name>
  <description>If an agent or automated task fails three consecutive times on the same goal (e.g., test failing, build error, model load error), the system MUST halt automated retries and escalate to the user for input or fallback to a safe state.</description>
  <trigger>3 consecutive failures</trigger>
  <action>Stop execution. Request user input. Revert state if necessary.</action>
</rule>
