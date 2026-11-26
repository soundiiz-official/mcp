# Changelog

Versions here describe the distributed client configuration and documentation. The hosted MCP server is versioned separately.

## 1.5.0 — 2026-11-26

- Puts assistant-created playlists, shared public playlists and supplied song lists first in examples.
- Explains the optional truthful curator credit and existing HTTPS illustration URL exposed by hosted MCP 0.5.0.
- Preserves the same endpoint, four tools, no-auth connection and final review in Soundiiz.

The hosted MCP server is version 0.5.0. The client package keeps the same endpoint, four tools and no-auth connection. Final review and transfer remain on Soundiiz; illustrations do not become destination playlist covers.

## 1.4.0 — 2026-11-25

- Updated the shared guide and README for the five official playlist-sharing hosts supported by the hosted MCP 0.4.0 server.
- Documented the hosted `playlist-import` skill and its client-controlled activation, separately from the bundled client rule.
- Preserved requested destinations, supplied order and duplicates, source limits, warnings, complete returned URLs, and user finalization in Soundiiz.

The package still connects to the same public endpoint with four tools and no sign-in. The hosted MCP server has its own version and deployment; this package does not activate a client's Skills extension.

## 1.3.0 — 2026-11-17

- Added the native Cursor plugin manifest and hosted MCP configuration.
- Licensed this public integration package under MIT; the hosted Soundiiz service is distributed separately.
- Added the license and Cursor configuration to the reproducible release archive.
- Added the catalog-specific 400 × 400 logo from the official GitHub organization avatar.

Validation: nine offline packaging tests pass. Gemini CLI validates the combined package. Antigravity validates it with the expected warning about Cursor-only `mcp.json`; the standalone Antigravity projection passes strict validation. The official Cursor template validator passes with only its optional-hooks warning. No model session or business tool call was used.

## 1.2.0 — 2026-11-17

- Added the native Antigravity plugin manifest, remote MCP configuration, bundled official logo, and three starter prompts.
- Shared one usage guide between Gemini context and an Antigravity rule, keeping client guidance consistent.
- Organized common assets, maintenance documentation, and an offline consistency checker and ZIP packager.
- Documented direct GitHub installation separately from curated Marketplace availability.

Validation: Antigravity CLI `1.5.10` passed strict native validation with no findings and installed the rule, logo, and MCP definition. Gemini CLI `0.68.0` passed validation, installation, and the MCP connection check. Five offline packaging tests pass, including version consistency, reproducible ZIPs, and rejection of external symlinks. No model session or business tool call was used.

The hosted MCP service, authentication, tool schemas, and import limits remain unchanged.

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
