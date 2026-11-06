# X News delivery

Since 2026-11-07, the primary domain uses the independent Nginx static origin on `qiaomu-hostinger` (`76.13.103.27`), via a DNS-only A record. The Worker remains available at its workers.dev hostname. **Use the newest QA.md entry for verification evidence and known limits.** No Docker, database, RSS writer, or application port is involved.

## Source and build

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
npm test
git add scripts src content tests public
git commit -m "Describe the published change"
git push origin main
```

Commit the tested generated `public/` before publishing. Do not rebuild after committing without including the regenerated feed in the release commit. Keep old fingerprinted `/static/` and `/read/` files: cached older HTML can still refer to them.

## Nginx origin

- Vhost source: `deploy/xnews.nginx.conf`; installed at `/www/server/panel/vhost/nginx/xnews.qiaomu.ai.conf`.
- Immutable releases: `/opt/qiaomu-apps/xnews/releases/<Git SHA>`; `current` is the active symlink and `previous` is the prior release.
- Public HTTPS certificate: `/etc/letsencrypt/live/xnews.qiaomu.ai/`; webroot `/www/wwwroot/xnews.qiaomu.ai` is configured for automatic renewal. Certbot reconfigure passed its simulated renewal, the timer is active, and the existing Nginx deploy hook reloads certificates. Bootstrap DNS credentials were removed. Initial certificate expires 2027-02-04.
- `release.nginx.conf` exposes the deployed Git SHA as `X-XNews-Release`.
- Deploy after one-time vhost/TLS bootstrap: `npm run deploy` (`bash scripts/deploy_vps.sh`). It requires a clean checkout, uploads the committed public tree, validates Nginx, and switches the static release symlink.
- Clean article URLs, genuine 404/noindex, RSS MIME, compression, no-referrer, immutable assets/reader payloads and short HTML freshness must be verified after deployment.

## Worker fallback and routing rollback

Keep Worker `xnews` at `https://xnews.vista8.workers.dev` as a fallback copy:

```bash
env -u CLOUDFLARE_API_TOKEN wrangler deploy
```

The shell token is DNS-scoped and can shadow the working Wrangler OAuth login. An expired OAuth access token can be refreshed by `env -u CLOUDFLARE_API_TOKEN wrangler deployments list`; never print or copy OAuth tokens into this repository.

Before routing changes, save the current DNS record and Worker custom-domain binding outside Git. Current bootstrap snapshots are in ignored `.qa-ui/speed-round2/dns-before.json` and `worker-domain-before.json`. Worker domain `9c0dffc5f63c3b43fc1e350f6f4fbec088aec803` originally attached `xnews.qiaomu.ai` to service `xnews`, environment `production`, zone `f83072793cc916b863e0d883a7e5d189`, account `d060d68463fc12fa91fa2aa216bbab02`.

Only switch after the Nginx candidate passes HTTPS checks using `curl --resolve xnews.qiaomu.ai:443:76.13.103.27 https://xnews.qiaomu.ai/` without disabling certificate verification. The completed migration detached the Worker custom-domain binding (its managed DNS record was read-only), then created a DNS-only A record for the same hostname at `76.13.103.27`. The Worker deployment is retained. Cloudflare DELETE may return HTTP 204 with no JSON body; handle that as success. Resolver caches can briefly retain old or negative answers, so check both authoritative/public DNS and normal clients. If DNS creation or candidate health fails, restore the saved Worker custom-domain binding using the Cloudflare Worker Domains API; do not leave a missing DNS record. To deliberately roll back later, remove only the new X News A record and reattach that saved Worker binding. Never alter unrelated domains.

For a content-only rollback, repoint `current` to the verified `previous` release and update `release.nginx.conf`; run `nginx -t` before reload. Do not delete releases during deployment or remove referenced fingerprinted assets.

Domain, canonical URLs, source/rewrite RSS v1 contract, and Umami property `31e0098c-6852-46b6-899c-11eed5ed16e1` remain unchanged. Performance work does not authorize unrelated reader/plugin changes.
