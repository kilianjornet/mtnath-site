# mtnath.com — static site

The public website for MTNATH: home, instructions, open methods, legal and contact.
Plain HTML and CSS, no build step. The app itself lives at **app.mtnath.com** (repo `mtnath-app`).

```
/                    index.html          Home: principles, tools, links
/instructions/       instructions/       User guide for app.mtnath.com (images in instructions/img/)
/methods/            methods/            Open methods: GAP, gut model, lab tests (CC BY 4.0)
/legal/              legal/              Privacy policy, terms of use, legal notice
/contact/            contact/            Contact addresses
/404.html                                Shown for missing pages (old WordPress links)
assets/site.css                          Styles for Home, Legal, Contact, 404
assets/sitebar.css                       The top bar on every page (standalone)
vercel.json / _redirects                 Redirects from old WordPress URLs + headers
```

## Before going live

1. **Fill the placeholders.** Search for `TODO` (they show highlighted in yellow on the Legal page):
   - Legal: legal name / company and org. number, address, Supabase and Vercel regions,
     sign-in email provider, backup and log retention, minimum age, price model, venue.
   - Contact: confirm the addresses `support@`, `methods@`, `hello@`, `privacy@mtnath.com` exist
     (they can all forward to one inbox).
2. **Have the Legal page checked.** It is a draft written from what the app does today
   (Supabase, Vercel, Anthropic for food and lab-report reading, COROS, Withings, Claude connector,
   coach links). Health data is a special category under GDPR, so a short review by a
   Norwegian privacy lawyer is worth it.
3. **Add old URLs to the redirects.** List the pages people link to on the current WordPress site
   (Search Console → Pages, or the WordPress Pages list) and add them to `vercel.json`
   (and `_redirects` if you use Cloudflare/Netlify).
4. **Optional: self-host fonts and MathJax.** Today the pages load Google Fonts and MathJax from
   jsDelivr; the privacy policy says so. Self-hosting removes those third-party requests — then
   delete that paragraph in the policy.

## Updating pages

- **Instructions:** export the new guide as HTML, then replace `instructions/index.html`.
  If the export has images inside it (`data:image/...`), run `python3 tools/extract_images.py new-guide.html`
  to move them into `instructions/img/` and add the site bar.
- **Methods:** replace `methods/index.html` with the new version and run the same script with `--methods`,
  or copy the `<header class="sitebar">` block and the two `<link>` lines from the current file.
- **Legal:** edit `legal/index.html` and change *Last updated*.

Preview locally: `python3 -m http.server 8000` in this folder, then open http://localhost:8000.

## Deploy on Vercel (same account as the app)

1. Push this folder to a new GitHub repo, e.g. `kilianjornet/mtnath-site`.
2. Vercel → **Add New → Project** → import the repo. Framework preset: **Other**, no build command,
   output directory `.` (the root).
3. Check the preview URL Vercel gives you (`mtnath-site-xxxx.vercel.app`).
4. Project → **Settings → Domains** → add `mtnath.com` and `www.mtnath.com`
   (set `www` to redirect to `mtnath.com`). Vercel shows the DNS records to create.
5. At the domain's DNS (where mtnath.com is registered today):
   - replace the WordPress `A` / `CNAME` records for `@` and `www` with Vercel's;
   - **leave the `MX` and email `TXT` records (SPF, DKIM, DMARC) exactly as they are**, or email on
     @mtnath.com stops working;
   - keep the `app` record pointing at the app.
6. Wait for Vercel to show the domain as valid (HTTPS is automatic), test the pages and redirects,
   and only then cancel the WordPress hosting.

**Alternative, free:** Cloudflare Pages or GitHub Pages work the same way (connect the repo, no build
command, output `/`). Cloudflare and Netlify read `_redirects`; GitHub Pages does not support redirects.
