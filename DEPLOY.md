# Deploying the TriadBlue site to Railway

A simple static website — two pages, one stylesheet, one script.
No database, no build step.

## What's in here

- `index.html` — the homepage (desktop website + mobile app experience)
- `apps.html` — the Products & Pricing page
- `styles.css` — all styling (desktop site + mobile app shell)
- `script.js` — mobile app navigation (tab bar, screens) + page behavior
- `manifest.json` — lets phones "Add to Home Screen" and launch it like an installed app
- `assets/` — ONLY MealPrepPro + ListIt logos (temporary). All other images
  load directly from the CDN at https://cdn.triadblue.com/brands/... —
  update a logo on the CDN and every page updates automatically, no redeploy.
- `package.json` — tells Railway how to serve the site

## Steps

1. **Upload these files to the GitHub repo** (TRIADBLUE/triadblueinc).
   On the repo page: Add file → Upload files → drag everything in
   (including the `assets` folder) → Commit.

2. **Railway deploys automatically** since the project is connected to the repo.
   First time: New Project → Deploy from GitHub repo → pick the repo.

3. **Test it.**
   Railway service → Settings → Networking → Generate Domain.
   Open the `*.up.railway.app` URL. Check it on your phone too —
   the mobile version behaves like an app (bottom tabs, screens).

4. **Point triadblue.com at it.**
   Railway → Settings → Networking → Custom Domain → add `triadblue.com`,
   then add the DNS record Railway shows you at your domain registrar.

## Notes

- The mobile experience is an app shell: bottom tab bar (Home / The Triad /
  Ecosystem / Products / FAQ), screen-based navigation, segmented Product
  tabs. Desktop is the classic full website.
- MealPrepPro and ListIt logos are placeholder images for now. When the real
  ones are on the CDN (brands/mealpreppro/ and brands/listit/), point the
  two `<img>` tags in apps.html at those URLs and delete the assets folder.
- Only the root-domain DNS record changes. Subdomains (my.hostsblue.com,
  triadblue.systems, console.blue, cdn.triadblue.com) stay as they are.
