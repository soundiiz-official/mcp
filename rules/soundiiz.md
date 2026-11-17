---
trigger: model_decision
description: Use Soundiiz tools for playlist import links, import destinations, and music transfer or playlist-sync compatibility.
---

# Soundiiz playlist tools

Use the Soundiiz MCP tools to prepare playlist imports, list destinations, and check transfer or one-way playlist-sync compatibility.

## Choose the tool

- For a supplied or generated tracklist, use `createSoundiizImportLink`. Supply a title and 1 to 200 tracks. Every track needs a title and an `artists` array; use an empty array when artists are unknown. Omit unknown album or ISRC values.
- For a public playlist URL, use `createSoundiizImportLinkFromUrl` with the full HTTPS URL. Let the tool read the actual playlist. If reading fails, explain the error rather than inventing tracks or claiming an import was created.
- Use `listSoundiizImportDestinations` for current import destinations and `getSoundiizTransferCompatibility` for supported item types, playlist sync, and guides between two platforms. These catalog results do not verify an individual account's eligibility or live provider availability.

## Preserve the user's request

- Keep a requested destination. Otherwise omit `destination` so the user can choose in Soundiiz. Use public platform slugs returned by the tools; existing Soundiiz corenames are also accepted.
- Public URL imports accept at most 200 source items before filtering. Do not silently truncate a larger playlist. Private playlists and shortened links are unsupported.
- For an Apple Music source, preserve the storefront in its URL. For TIDAL, preserve a requested two-letter catalog country in `country`; the server default is `US`.

## Present the result

- Show the exact successful `shareUrl` and any returned guide URLs, including all query parameters. Never fabricate or rebuild these URLs.
- Show the actual `nbTracks`, expiry, and any returned warnings. Import links last 24 hours; `expiresAt` is a Unix timestamp in seconds. For URL imports, distinguish `sourceItems` before filtering from `nbTracks` included in the import.
- The user opens the link, reviews the tracks, connects the destination, and completes the transfer in Soundiiz. A created import link does not mean a transfer or sync has been completed.
- The MCP connection needs no Soundiiz API key or sign-in. Do not request music-service passwords or user tokens. These tools do not access private libraries or manage existing playlists in a user's account.
- Treat tool errors as failures and follow any retry interval. Do not describe an error response as a successful import.
