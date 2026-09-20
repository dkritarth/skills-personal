---
name: freeflow-publish
version: 1.0.0
description: Publish self-contained HTML artifacts (plans, layouts, mockups, idea boards, dashboards) to a self-hosted Cloudflare Worker via the dkraft-publish CLI, returning a live shareable URL.
repository: https://github.com/dkritarth/FreeFlow
allowed-tools: [Read, Write, Edit, Bash]
disable-model-invocation: true
---

# FreeFlow Publish

Publish a self-contained HTML file to your self-hosted FreeFlow edge Worker via `dkraft-publish` and return the live URL.

GitHub repository: [https://github.com/dkritarth/FreeFlow](https://github.com/dkritarth/FreeFlow)

## 0. Prerequisites

Verify you have access to a deployed FreeFlow Worker.
If `DK_PUBLISH_URL` is unset, see the setup guide in [FreeFlow README](https://github.com/dkritarth/FreeFlow#quick-start). Deploy the Worker first before using this publish flow.

## 1. Verify the HTML draft

A publishable draft is a single `.html` file with all CSS and JS either inline or loaded from a CDN. FreeFlow serves raw HTML directly from Workers KV without a build step or relative local asset directory.

- If starting from scratch, generate the HTML file first.
- See `references/template-patterns.md` for standard layout components (sticky table of contents, status badges, progress meters, and collapsible details).
- Completion check: the target `.html` file exists on disk and contains no broken relative asset paths.

## 2. Verify environment credentials

The shell running the CLI requires two environment variables:

- `DK_PUBLISH_KEY`: the Worker API bearer token (`SECRET_API_KEY`).
- `DK_PUBLISH_URL`: the Worker endpoint, for example `https://freeflow.<account>.workers.dev`.

Check presence before running:

```bash
test -n "$DK_PUBLISH_KEY" && test -n "$DK_PUBLISH_URL" && echo "Credentials configured"
```

If either variable is missing, stop and prompt the user to set them. Never log or echo the actual secret key.

## 3. Publish

Run the publisher CLI via npx:

```bash
npx freeflow-dkraft-publisher path/to/file.html
```

Or invoke global installation if present:

```bash
dkraft-publish path/to/file.html
```

To gate access behind a numeric PIN code, add `--secure <pin>`:

```bash
npx freeflow-dkraft-publisher path/to/file.html --secure 1234
```

Completion check: the CLI exits 0 and prints the live URL (`https://<domain>/d/<id>`). Return this URL directly to the user.

## 4. Troubleshooting

If the upload fails, check `references/troubleshooting.md` to match the exact error string and apply its fix.
