# Advantage HPE SEO Pages
Automated SEO content cluster for Advantage HPE — HVAC, Plumbing, Electrical.
Florida Panhandle: Fort Walton Beach, Destin, Niceville, Navarre, Crestview.

## Structure
Each page lives at /{slug}/index.html
Deployed via Cloudflare Pages, auto-updated daily by GitHub Actions.

## Pages
- Phase 3: EV Charger, Generator, Tankless WH, Mini-Split, No Hot Water, Lights Flickering
- 30 pages × 5 cities = 150 total planned

## Auto-Update System
GitHub Actions runs daily at 6am ET:
1. Fetches local weather/seasonal data for each city
2. Calls Claude API to refresh content with current conditions
3. Commits updated HTML files
4. Cloudflare Pages auto-deploys within 60 seconds
