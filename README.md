# Soundiiz MCP

Official [Soundiiz](https://soundiiz.com) integration for AI assistants using the [Model Context Protocol](https://modelcontextprotocol.io/).

Turn a tracklist or a public playlist URL into a Soundiiz import link, discover supported destinations, and check music transfer compatibility. You review the tracks and complete the transfer in Soundiiz.

## Install in Gemini CLI

With an up-to-date [Gemini CLI](https://geminicli.com/docs/get-started/installation/) and Git installed, run this command in your terminal:

```sh
gemini extensions install https://github.com/soundiiz-official/mcp
```

Restart Gemini CLI, then check the connection:

```text
/mcp list
```

The extension is named `soundiiz` and connects to `https://soundiiz.com/mcp` using Streamable HTTP. No Soundiiz API key or sign-in is required to connect the MCP server. You connect your destination music service in Soundiiz when completing an import.

Validated with Gemini CLI `0.68.0`.

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

Configuration fields vary by client. Follow the examples in the [Soundiiz setup documentation](https://soundiiz.com/api). The `gemini-extension.json` in this repository is specifically for Gemini CLI.

## Troubleshooting

- If the tools do not appear, restart Gemini CLI and run `/mcp list`. Check that the server URL is reachable from the environment running the CLI.
- If you already configured a server named `soundiiz` in Gemini's `settings.json`, that configuration takes precedence over the extension. Check its URL if the extension appears to connect to a different server.
- If an import fails, follow the returned error or retry interval. A failed response is not a successful import; do not construct an import URL from the request.

For account or transfer questions, visit [Soundiiz Support](https://support.soundiiz.com/). Use this repository's [issues](https://github.com/soundiiz-official/mcp/issues) for problems with the published client configuration or its documentation.

## Versions

The Gemini extension has its own version, starting at `1.0.0`. This repository distributes connection settings and documentation; the MCP tools run on Soundiiz's hosted service. Pinning an extension release does not pin the server implementation.

See [CHANGELOG.md](CHANGELOG.md) for extension releases and [Gemini's extension guide](https://geminicli.com/docs/extensions/) for installation options.
