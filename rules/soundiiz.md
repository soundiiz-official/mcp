---
trigger: model_decision
description: Use Soundiiz tools for playlist import links, import destinations, and music transfer or playlist-sync compatibility.
---

# Soundiiz playlist tools

Use the Soundiiz MCP tools to prepare playlist imports, list destinations, and check transfer or one-way playlist-sync compatibility.

## Choose the tool

- For a supplied or generated tracklist, use `createSoundiizImportLink`. Supply a title and 1 to 200 tracks. Every track needs a title and an `artists` array; use an empty array when artists are unknown. Omit unknown album or ISRC values.
- For a public playlist URL, use `createSoundiizImportLinkFromUrl` with the HTTPS URL as supplied, including its query parameters. Let the tool read the actual playlist. If reading fails, explain the error rather than inventing tracks or claiming an import was created.
- Use `listSoundiizImportDestinations` for current import destinations and `getSoundiizTransferCompatibility` for supported item types, playlist sync, and guides between two platforms. These catalog results do not verify an individual account's eligibility or live provider availability.

## Preserve the user's request

- Keep the supplied order and duplicates. Do not silently split a playlist above the limit into multiple import links; guide the user to the full Soundiiz flow.
- Keep a requested destination. Otherwise omit `destination` so the user can choose in Soundiiz. Use public platform slugs returned by the tools; existing Soundiiz corenames are also accepted.
- Public URL imports accept at most 200 source items before filtering. Do not silently truncate a larger playlist. Official short-link hosts are `link.deezer.com`, `spotify.link`, `spotify.app.link`, `apple.co`, and `on.soundcloud.com`; only public playlist targets on the same service are accepted. Other short links and private playlists are unsupported.
- For an Apple Music source, preserve the storefront in its URL. For TIDAL, preserve a requested two-letter catalog country in `country`; the server default is `US`.

## Credit the selection and illustrate the import

Use these optional fields only when the current tool exposes them.

For tracklist imports, `sourceName` may credit the actual curator or assistant that selected the songs. Use a truthful single-line credit in the user's language, with at most 120 characters. When you selected the songs, a credit such as "Selection curated with ChatGPT" is appropriate only if that identifies the actual assistant. Preserve the provenance of user-supplied lists; formatting or importing them is not selecting their songs. Omit an unknown credit to keep the default Soundiiz source name.

The optional `sourceLogo` is an existing HTTPS illustration URL, at most 2048 characters, for the large image on the Soundiiz import page. It does not change the small platform icon and is not sent as a playlist cover to the destination. Use a URL without credentials, local addresses, or raw CSS delimiters; encode characters such as parentheses in an otherwise valid URL. The server does not download, host, or verify the image.

Use an illustration only when a usable existing URL is available. Do not invent an image URL, upload a file, or send base64, a data URL, a local path, or a chat attachment reference. An image generated or attached in the conversation is not automatically a usable HTTPS URL. Omit the illustration if none is available. The image host must keep it available while the import link is used.

These optional arguments belong to `createSoundiizImportLink`; the public-playlist URL tool retains its source metadata.


## Present the result

- Show the exact successful `shareUrl` and any returned guide URLs, including all query parameters. Never fabricate or rebuild these URLs.
- Show the actual `nbTracks`, expiry, and any returned warnings. Import links last 24 hours; `expiresAt` is a Unix timestamp in seconds. For URL imports, distinguish `sourceItems` before filtering from `nbTracks` included in the import.
- The user opens the link, reviews the tracks, connects the destination, and completes the transfer in Soundiiz. A created import link does not mean a transfer or sync has been completed.
- The MCP connection needs no Soundiiz API key or sign-in. Do not request music-service passwords or user tokens. These tools do not access private libraries or manage existing playlists in a user's account.
- Treat tool errors as failures and follow any retry interval. Do not describe an error response as a successful import.
