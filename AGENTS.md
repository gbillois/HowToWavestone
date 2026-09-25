# AGENTS.md

Guidance for coding assistants (Claude Code, Codex, Copilot...) working on this repository or building a CYB agent from its principles.

## Repository

- HowToWavestone static site: standalone HTML pages at the root, shared styling in `wavestonedesign.css`, assets in `assets/`.
- French is the default text written in the HTML; English and German translations live in each page's `window.WS_I18N` object, keyed by `data-i18n` attributes (see `assets/i18n.js`).
- `howto290626.html` and `dist/index.html` are consolidated builds produced by `tools/build_inline_html.py` (the "Build inline HTML" workflow). Any page change must be carried over to them or rebuilt.
- GitHub Pages deploys automatically from `main`.

## CYB agent principles

Full reference: `agent-principles.html`. Any agent or tool built here follows the prompt below. The page shows the same prompt in FR / EN / DE (`prompt.body` key); keep the three versions and this file in sync.

```text
Build or modify a local-first CYB agent.

Architecture
- One standalone HTML file (or small static folder) that opens in any browser: no server, install, admin rights, database or client infrastructure.
- Deterministic logic first; call an LLM only where it clearly adds value. Core features must work offline.
- Share and collaborate through JSON export / import.

LLM layer (optional)
- One LLMClient (getAvailableModels, testConnection, generate). Provider and model are settings: OpenAI, Anthropic, Mistral, Azure OpenAI / AI Foundry, Ollama, any OpenAI-compatible endpoint.
- Block every AI call until the user checks "AI use is authorized for this content and complies with the client's rules".
- Load models dynamically with a curated fallback; show connection status and clear errors (provider, model, HTTP status, never secrets).

Secrets
- API keys never appear in exports, logs, prompts or generated files.
- sessionStorage by default, localStorage only on explicit opt-in; password fields and a "Clear API keys" button.

Done when: no AI call before approval, exports hold no secrets, the app runs without a server.
```

## Writing rules

- Keep the prompt short: actionable rules only, no repetition of what the page already explains.
- No em dashes in any text.
- No `utm_source` parameter in URLs.
