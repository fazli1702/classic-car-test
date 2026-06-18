# Classic Car Singapore

A prototype web app for a classic car dealership in Singapore. This is a design showcase — no backend logic, authentication, or database. The goal is to demonstrate a classic, luxury, and professional aesthetic.

## Tech Stack

- **Backend:** Flask (Python 3.10), run with `python app.py` (debug mode on port 5000)
- **Frontend:** Jinja2 templates + Tailwind CSS v4 (CDN browser build via `@tailwindcss/browser@4`)
- **Data:** Static JSON files (`data.json` for scraped vehicle listings, `cars.json` for placeholder data)
- **Scraper:** `scraper/scraper.py` — BeautifulSoup + lxml, scrapes from classiccarsingapore.com into `data.json`
- **Virtual env:** `.venv` (activate with `source .venv/bin/activate`)

## Project Structure

```
app.py              # Flask app — routes for /, /buy, /contact, /about
data.json           # Scraped vehicle data (used by the app)
cars.json           # Placeholder vehicle data (not currently used by app)
templates/
  base.html         # Shared layout: navbar + footer
  index.html        # Homepage: hero, value props, featured vehicles, enquiry form
  buy.html          # Collection page with client-side filters (make/model/year)
  details.html      # Single vehicle detail page (image gallery, specs, description)
  about.html        # About page
  contact.html      # Contact page with enquiry form
  old_index.html    # Deprecated homepage
scraper/
  scraper.py        # Vehicle data scraper
```

## Design System

- **Theme:** Classic, luxury, professional
- **Primary gold:** `#D4AF37` (accent, buttons, borders, highlights), hover: `#B8942F`
- **Dark background:** `#1A1A1A` (hero sections, footer, dark panels)
- **Text:** `#2D2D2D` (body text), gray-400/gray-500 (secondary text)
- **Light background:** `#F9F9F9` (alternating sections), white
- **Typography:** Serif font (headings, display text) + sans-serif (body, labels)
- **Pattern:** Uppercase tracking-wide labels, gold accent dividers (`w-12 h-px bg-[#D4AF37]`), gold-bordered cards with rounded-xl corners
- **Cards:** Gold border, rounded-xl, hover shadow + lift (`hover:shadow-xl hover:-translate-y-1.5`)

## Running the App

```bash
source .venv/bin/activate
python app.py
```

Visit http://localhost:5000

## Notes

- This is a prototype — forms don't submit, some nav links point to `#`, contact details are commented out
- Vehicle images use Unsplash URLs (external) — no local image assets
- The `/static` directory exists but is currently empty
- No tests, no CI, no requirements.txt — install deps with `pip install flask requests beautifulsoup4 lxml`
