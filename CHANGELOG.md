# Changelog

Versions here describe the distributed client configuration and documentation. The hosted MCP server is versioned separately.

## 1.1.0 — 2026-11-17

- Added a concise tool usage guide through `contextFileName`, covering tool selection, destinations, source limits, complete URLs, warnings, expiry, and the user's final review in Soundiiz.
- Added the official Soundiiz logo to the README.
- Audited the Gemini CLI manifest fields and gallery presentation. Gallery thumbnails use the GitHub owner's avatar; the manifest has no supported logo or icon field.

Validation: Gemini CLI `0.68.0` passed native validation, local installation, activation, and the MCP connection check. The installed context file matches the packaged source, and the linked official logo is a valid 512 × 512 PNG.

This release adds client guidance and presentation only. The hosted MCP tools and connection remain unchanged.

## 1.0.0 — 2026-11-17

- Added the official Soundiiz Gemini CLI extension, connecting to `https://soundiiz.com/mcp` over Streamable HTTP without authentication.
- Documented installation, updates, removal, the four available tools, import limits, and user review before completing a transfer in Soundiiz.
- Added setup information for other remote MCP clients.

Validation: the hosted server reported `soundiiz` version `0.2.3` and all four documented tools during `initialize` and `tools/list`; the session was then closed. No business tool was called and no import or transfer was created. Gemini CLI `0.68.0` passed native extension validation without warnings, local installation, extension listing, and an HTTP MCP connection check. The manifest uses the explicit `type: "http"` and `url` connection format supported by that release. No Google account or model session was used for these checks.

This release changes the distribution package only. It does not change the hosted tools, their schemas, authentication, or limits.
