# Soundiiz MCP

<img src="assets/soundiiz-512.png" alt="Soundiiz" width="80" height="80">

Official [Soundiiz](https://soundiiz.com) integration for AI assistants using the [Model Context Protocol](https://modelcontextprotocol.io/).

Turn a tracklist or a public playlist URL into a Soundiiz import link, discover supported destinations, and check music transfer compatibility. You review the tracks and complete the transfer in Soundiiz.

## Install in Cursor

This repository includes a native Cursor plugin in `.cursor-plugin/plugin.json`,
with the hosted MCP connection in `mcp.json`, the shared usage rule, and the official logo.

To configure the connection directly in Cursor, add this entry to your user MCP
settings (`~/.cursor/mcp.json`) or project MCP settings (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "soundiiz": {
      "url": "https://soundiiz.com/mcp"
    }
  }
}
```

Merge this entry with existing servers. Do not overwrite other MCP settings.
No Soundiiz API key is required. Use Cursor's MCP controls to enable the connection
and confirm the tools are available. See the [shared usage guide](rules/soundiiz.md).

For local plugin testing, place the repository contents in
`~/.cursor/plugins/local/soundiiz`, reload Cursor, and check Customize.
See [Cursor's plugin documentation](https://cursor.com/docs/plugins).
Availability in the curated Marketplace is announced only after Cursor approves
our submission.

## Install in Antigravity

Install the plugin from this repository using [Antigravity CLI](https://antigravity.google/docs/getting-started?tab=cli):

```sh
agy plugin install https://github.com/soundiiz-official/mcp
```

Check the installed plugin with `agy plugin list`. It bundles the hosted MCP connection, a usage rule, and the official Soundiiz logo. No Soundiiz API key is required. Restart an active Antigravity session to load the plugin.

Installation from GitHub is separate from inclusion in the curated Antigravity Marketplace. Marketplace availability is announced only after Google accepts the submission.

## Install in Gemini CLI

Google moved free and Google AI Pro/Ultra subscription access to Antigravity CLI on June 18, 2026. Gemini CLI remains available with supported API and enterprise access. See [Google's transition announcement](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) for details.

With an up-to-date [Gemini CLI](https://geminicli.com/docs/get-started/installation/) and Git installed, run this command in your terminal:

```sh
gemini extensions install https://github.com/soundiiz-official/mcp
```

Restart Gemini CLI, then check the connection:

```text
/mcp list
```

The extension is named `soundiiz` and connects to `https://soundiiz.com/mcp` using Streamable HTTP. No Soundiiz API key or sign-in is required to connect the MCP server. You connect your destination music service in Soundiiz when completing an import.

Validated with Gemini CLI `0.68.0` and Antigravity CLI `1.5.10`. Both client packages share one concise [usage guide](rules/soundiiz.md). Gemini loads it as context; Antigravity loads it as a rule for Soundiiz requests.

### Try it

- "Create a Soundiiz import link for a 20-track jazz playlist, with Spotify as the destination."
- "Prepare an import to Apple Music from this public playlist: [paste the full playlist URL]."
- "Which music services can receive a Soundiiz playlist import?"
- "Can I transfer playlists from Spotify to YouTube Music, and can I keep them synced?"

For an import, the assistant returns a temporary link. Open it, review the tracks, and finish the transfer in Soundiiz. Compatibility checks return information and guides; they do not start a transfer or create a synchronization.

### Update or uninstall

```sh
gemini extensions update soundiiz
```

```sh
gemini extensions uninstall soundiiz
```

Restart Gemini CLI after updating or uninstalling the extension.

## Available tools

| Tool | What it does |
| --- | --- |
| `createSoundiizImportLink` | Creates a 24-hour import link from a supplied tracklist of 1 to 200 tracks. |
| `createSoundiizImportLinkFromUrl` | Reads a supported public playlist URL with at most 200 source items and creates a 24-hour import link. |
| `listSoundiizImportDestinations` | Lists the currently configured playlist import destinations. |
| `getSoundiizTransferCompatibility` | Returns supported transfer item types, one-way playlist sync support, and guide links for two music services. |

The connected client discovers current tool descriptions and schemas from the hosted server.

## Import details and limits

- Public playlist URL sources: Spotify, Apple Music, Deezer, SoundCloud, YouTube, YouTube Music, Qobuz, TIDAL, and public Soundiiz playlists. Use the full HTTPS playlist URL. Private playlists and shortened links are unsupported.
- A URL import accepts up to 200 source items before filtering. Larger playlists are rejected; they are not silently shortened. The assistant should show any returned warnings and the actual number of tracks included.
- A tracklist import requires a title and 1 to 200 tracks. Each track needs a title and an array of artists; unknown album or ISRC values should be omitted.
- Include a destination only when one has been requested. Use the public platform identifier returned by the destination tool; existing Soundiiz corenames are also accepted.
- Keep returned import and guide URLs intact, including their query parameters. Import links expire after 24 hours.
- The MCP server does not read private libraries or complete transfers into music-service accounts. The assistant supplies a tracklist when needed; the server does not generate music recommendations.
- Destination and compatibility information comes from the Soundiiz catalog. It does not check an individual account's eligibility, subscription, regional availability, or live provider status.

See the [Soundiiz MCP documentation](https://soundiiz.com/api) for current capabilities, limits, and setup examples.

## Other MCP clients

Configure your client's remote MCP connection with:

| Setting | Value |
| --- | --- |
| Server URL | `https://soundiiz.com/mcp` |
| Transport | Streamable HTTP |
| Authentication | None |

Configuration fields vary by client. Follow the examples in the [Soundiiz setup documentation](https://soundiiz.com/api). The `gemini-extension.json` in this repository is for Gemini CLI. Antigravity uses `.antigravity-plugin/plugin.json` and `mcp_config.json`.

## Troubleshooting

- If the tools do not appear, restart Gemini CLI and run `/mcp list`. Check that the server URL is reachable from the environment running the CLI.
- If you already configured a server named `soundiiz` in Gemini's `settings.json`, that configuration takes precedence over the extension. Check its URL if the extension appears to connect to a different server.
- If an import fails, follow the returned error or retry interval. A failed response is not a successful import; do not construct an import URL from the request.

For account or transfer questions, visit [Soundiiz Support](https://support.soundiiz.com/). Use this repository's [issues](https://github.com/soundiiz-official/mcp/issues) for problems with the published client configuration or its documentation.

## Versions

The distributed client package has its own version, shared by the Gemini and Antigravity manifests. This repository distributes connection settings and documentation; the MCP tools run on Soundiiz's hosted service. Pinning an extension release does not pin the server implementation.

See [CHANGELOG.md](CHANGELOG.md) for extension releases and [Gemini's extension guide](https://geminicli.com/docs/extensions/) for installation options.

## Repository maintenance

See [the maintenance guide](https://github.com/soundiiz-official/mcp/blob/main/docs/maintaining.md) for the repository layout, validation commands, release procedure, and how to add another client integration.

## License

The client integration package in this repository is licensed under the
[MIT License](LICENSE). It contains configuration, documentation, and packaging
utilities. It does not contain or license the implementation of Soundiiz's hosted
service.
