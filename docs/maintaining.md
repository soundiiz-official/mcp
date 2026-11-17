# Maintaining the Soundiiz MCP client packages

## Layout

- `gemini-extension.json`: Gemini CLI's native manifest. It must stay at the repository root for gallery discovery.
- `.antigravity-plugin/plugin.json`: Antigravity's native manifest in its documented location for repositories supporting multiple tools.
- `mcp_config.json`: Antigravity's native MCP configuration at the plugin root.
- `rules/soundiiz.md`: the single shared usage guide. Antigravity loads its model-decision rule; Gemini references the same file through `contextFileName`.
- `assets/soundiiz-512.png`: the original official logo, shared by the Antigravity manifest and README.
- `docs/`: contributor and maintenance documentation.
- `tools/package.py`: offline consistency checks and release ZIP packaging.
- `README.md` and `CHANGELOG.md`: installation, current scope, and version history.

Keep client manifests in their required discovery locations. Shared assets and instructions belong in one place. This repository distributes client configuration; the hosted server remains the source of truth for tool schemas and capabilities.

## Make a change

1. Check the hosted tool contract and documentation before changing product claims or guidance. Preserve requested destinations, real track counts, warnings, expiry, and complete returned URLs.
2. Update the shared usage guide when client guidance changes. Use only fields documented by the target client; an unsupported metadata field does not add a capability.
3. Keep the Gemini and Antigravity package versions aligned and add a changelog entry. Package releases do not change or pin the hosted MCP server implementation.
4. Run the offline checks and the native client validators. Test installation or update for affected clients, including the referenced context/rule and logo assets.
5. Publish a new immutable tag and release. Keep previous releases. Gallery publication, Marketplace submission, and Marketplace acceptance are separate states.

## Validate

```sh
python3 -m unittest discover -s tests -v
python3 tools/package.py --check
gemini extensions validate .
agy plugin validate --json .
```

Antigravity may report expected warnings for files belonging to other clients or contributor documentation. Review every finding. A standalone Antigravity bundle must pass `agy plugin validate --strict`; in the combined repository, require zero errors and no unresolved warnings about Antigravity's own manifest, MCP configuration, rules, or logo.

Use an isolated client profile and a neutral workspace for installation tests. Do not include credentials, local profiles, generated validation evidence, or application source in the release. Discovery checks may initialize, list tools, and close a session; do not call business tools or create imports as a release check.

## Package and release

```sh
python3 tools/package.py --output /tmp/soundiiz-client-package.zip
```

`.gitattributes` keeps source text in LF form on all platforms. The packager also normalizes CRLF text to LF, so a Windows checkout produces the same ZIP as a Linux checkout. Binary logo bytes remain unchanged.

The ZIP contains only the runtime manifests, MCP configuration, shared rule, logo, README, and changelog. Contributor tools and maintenance docs stay in the repository. Native manifest paths remain intact and `gemini-extension.json` stays at the ZIP root.

Commit the checked files, create an annotated version tag, and publish the ZIP on the matching GitHub Release. Confirm the public download matches the locally validated archive. Verify fresh installation or update from the public repository before announcing availability.

- Gemini gallery: public repository, root manifest, and the `gemini-cli-extension` GitHub topic. Gallery thumbnails use the GitHub owner's avatar.
- Antigravity: publish the native plugin, validate it, then use the [Marketplace partner intake form](https://forms.gle/2EX5RFYPoJe1UgxR9). Its `logo` is a bundled asset. An intake submission does not mean the plugin is already listed.

## Add another client

Read its current official distribution and schema documentation first. Add only the required native adapter files, reference the shared hosted endpoint and usage guide where supported, and extend the consistency checker and archive list. Record which exact client version and installation path were tested. Do not advertise compatibility or catalog availability before verifying it.

Official references: [Gemini extension reference](https://geminicli.com/docs/extensions/reference/), [Gemini releases](https://geminicli.com/docs/extensions/releasing/), [Antigravity plugin format](https://antigravity.google/docs/build-plugins/), and [Antigravity MCP configuration](https://antigravity.google/docs/mcp).
