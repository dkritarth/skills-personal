# dkraft-publish troubleshooting

Match the exact printed error text, then apply the fix. Don't retry blind.

## "Missing required environment variables."

`DK_PUBLISH_KEY` or `DK_PUBLISH_URL` unset. Fix: ask the user for both, or check their shell profile / `.env` for existing values. Never invent a key.

## "Error: The target HTML file is empty."

File exists but has zero content after trim. Fix: verify the file was actually written before publishing - check byte size with `ls -la <file>` or re-read it.

## "Upload failed (401): Unauthorized"

`DK_PUBLISH_KEY` doesn't match the Worker's `SECRET_API_KEY`. Fix: confirm the key with the user; it may have been rotated. Do not brute-force retry with guesses.

## "Upload failed (400): ..."

Payload rejected - usually an empty `html` field slipping past the local empty-check (rare), or the Worker's JSON parsing choked. Fix: confirm the file is valid UTF-8 HTML text, not binary.

## "Upload succeeded but response was missing a URL."

Worker responded 200 but with an unexpected body shape - points at a Worker-side bug or a proxy/CDN stripping the response. Fix: report this to the user as a Worker issue, don't retry.

## "Failed to publish draft." + ENOENT

File path wrong. Fix: resolve the path relative to the actual cwd the CLI runs in, or use an absolute path.

## "Failed to publish draft." + fetch/network error

`DK_PUBLISH_URL` unreachable - wrong hostname, Worker not deployed, or the sandbox/environment has no outbound network access. Fix: `curl -I $DK_PUBLISH_URL` to isolate whether it's DNS, TLS, or a genuinely down Worker.

## `dkraft-publish` command not found

Not installed globally. Fix: run `npx freeflow-dkraft-publisher <file>` (pulls straight from npm, no local checkout needed), or `npm install -g freeflow-dkraft-publisher`, or invoke `node cli/index.js <file>` from inside the FreeFlow repo.

## Raw HTTP fallback (no CLI available)

```bash
curl -X POST "$DK_PUBLISH_URL/upload" \
  -H "Authorization: Bearer $DK_PUBLISH_KEY" \
  -H "Content-Type: application/json" \
  -d "$(node -e 'console.log(JSON.stringify({html: require("fs").readFileSync(process.argv[1], "utf8"), pin: process.argv[2] || null}))' <path-to-file.html> <optional-pin>)"
```

Response: `{"url": "https://<worker-domain>/d/<id>"}`. Draft URLs are path-based (`/d/{id}`), not subdomain-based - there is no `*.pages.<domain>` scheme in the current deployment.
