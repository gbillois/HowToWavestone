# AGENTS.md

Instructions pour les assistants de code (Claude Code, Codex, Copilot...) qui travaillent sur ce dépôt ou qui construisent un agent CYB à partir de ses principes.

## Le dépôt

- Site statique HowToWavestone : pages HTML autonomes à la racine, style commun dans `wavestonedesign.css`, assets dans `assets/`.
- Textes en français par défaut, traductions EN / DE dans l'objet `window.WS_I18N` de chaque page (clés `data-i18n`).
- `howto290626.html` et `dist/index.html` sont générés par `tools/build_inline_html.py` (workflow "Build inline HTML"). Toute modification d'une page doit y être reportée ou régénérée.

## Principes des agents CYB

Référence complète : `agent-principles.html`. Tout agent ou outil construit ici suit le prompt type ci-dessous, identique à celui affiché en bas de cette page. Si l'un change, mettre l'autre à jour.

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

## Règles de rédaction

- Garder le prompt type court : uniquement les règles actionnables, sans répéter ce que la page explique déjà.
- Pas de tiret cadratin dans les textes.
- Pas de paramètre `utm_source` dans les URL.
