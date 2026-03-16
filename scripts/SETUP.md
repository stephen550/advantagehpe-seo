# Setup Guide — Advantage HPE SEO System

## Step 1: Push to GitHub (one time)
```bash
cd ~/advantagehpe-seo
git init
git add .
git commit -m "Initial deploy: Phase 3 SEO pages"
gh repo create advantagehpe-seo --public --source=. --remote=origin --push
```

## Step 2: Connect to Cloudflare Pages (one time, ~5 minutes)
1. Go to dash.cloudflare.com
2. Click Workers & Pages → Create → Pages → Connect to Git
3. Select your GitHub repo: advantagehpe-seo
4. Settings:
   - Framework preset: None
   - Build command: (leave blank)
   - Build output directory: (leave blank)
5. Click Save and Deploy
6. Your site goes live at: advantagehpe-seo.pages.dev

## Step 3: Add Anthropic API Key to GitHub (for daily updater)
1. Go to github.com/YOUR_USERNAME/advantagehpe-seo/settings/secrets/actions
2. Click New repository secret
3. Name: ANTHROPIC_API_KEY
4. Value: your Anthropic API key
5. Click Add secret

## Step 4: Set up GHL Redirects (connects your real URLs to the content)
In GHL → Settings → Domains & URL Redirects:
Add one redirect per page:
- Source: /ev-charger-installation-fort-walton-beach
- Destination: https://advantagehpe-seo.pages.dev/ev-charger-installation-fort-walton-beach
- Type: 301

Once Google indexes, you can switch these back to native GHL pages.

## How It Works After Setup
- Every morning at 6am ET, GitHub Actions runs automatically
- It fetches live weather for each Panhandle city
- Claude API writes a fresh seasonal content block for that day's page type
- The updated HTML commits to GitHub
- Cloudflare Pages deploys the update within 60 seconds
- Google sees fresh content every day — signals relevance and authority

## Page Rotation Schedule
Day 1, 7, 13, 19, 25: EV Charger pages
Day 2, 8, 14, 20, 26: Generator pages
Day 3, 9, 15, 21, 27: Tankless Water Heater pages
Day 4, 10, 16, 22, 28: Mini-Split pages
Day 5, 11, 17, 23, 29: No Hot Water pages
Day 6, 12, 18, 24, 30: Lights Flickering pages
