# Local Model Routing via Model Context Protocol (MCP)

This skill defines the operational parameters for routing inference requests to local models, specifically Gemma 4 E4B via Ollama, within the Omni-Route architecture.

## Overview
As an AI Architect and orchestrator, you must handle local model routing efficiently, securely, and within the strict hardware constraints of edge devices.

## The 4GB VRAM Constraint
* **Hard Limit:** The system operates with a maximum of 4GB VRAM.
* **Model Selection:** Only load quantized models (e.g., 4-bit or 8-bit depending on parameter size) that fit comfortably within a ~3.5GB memory footprint, leaving overhead for context windows and system operations.
* **Context Size:** Strictly manage the context window to prevent Out of Memory (OOM) crashes. Truncate or summarize older context if necessary before routing to the model.
* **Unloading:** Ensure idle models are unloaded or swapped out of VRAM if multiple tools (e.g., Docling, Whisper.cpp) need memory space concurrently.

## Model Context Protocol (MCP) Guidelines

When integrating and routing via MCP:

1. **Structured Server Definitions:**
   Define the Ollama MCP server clearly, ensuring endpoints, model names, and connection parameters are explicit.

2. **Resource Declaration:**
   Always declare the resources (VRAM budget, CPU threads) required for a specific MCP tool call.

3. **Fallback Mechanisms (Three-Fail Protocol Integration):**
   * If an MCP route times out or fails due to OOM:
     * **Attempt 1:** Retry with a truncated context window.
     * **Attempt 2:** Unload other processes (if possible) and retry.
     * **Attempt 3:** Abort the routing request, log the failure, and trigger the Three-Fail Fallback (escalate to user/safe state).

4. **Structured Output Enforcement:**
   Ensure MCP tools interacting with the LLM enforce JSON schema validation. If the model returns malformed JSON, the MCP router must attempt to parse/repair it or trigger a retry *before* passing it back to the orchestrator.

## Execution Example
When asked to process a local file using a model:
1. Verify VRAM availability.
2. Formulate the prompt using `<context>` tags.
3. Route via MCP to the local Ollama instance.
4. Validate the structured output.
5. Handle failures gracefully per the Guardrails in `CLAUDE.md`.