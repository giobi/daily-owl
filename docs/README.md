# Daily Owl - Documentazione Completa 🦉

## Cosa è Daily Owl

Daily Owl è un digest quotidiano completamente dinamico che cambia **tutto** ogni giorno:
- Contenuti aggregati da fonti tech internazionali e locali (Verbania)
- Design e CSS generati da AI con mood casuali
- Layout moderno image-driven con estetica contemporanea
- Scritto in italiano con il sarcasmo caustico di Anacleto

## Architettura

### Stack Tecnico

- **Generator**: Python script (`/home/claude/brain/tools/agents/daily-owl-generator.py`)
- **LLM**: Gemini 2.0 Flash (via Google AI API)
- **Hosting**: GitHub Pages
- **Domain**: dailyowl.it (Cloudflare DNS)
- **Automation**: Cron daily (6:00 AM)

### File Structure

```
daily-owl/
├── index.html              # Today's digest (overwritten daily)
├── style.css               # Daily generated CSS
├── assets/
│   ├── logo.png            # Anacleto logo
│   └── images/
│       └── YYYY-MM-DD/     # Daily images
├── archive/
│   ├── index.html          # Archive list
│   └── YYYY-MM-DD.html     # Past editions
├── docs/                   # This documentation
├── CNAME                   # Custom domain config
└── README.md
```

## Fonti di Contenuto

### Tech Internazionali
- **Hacker News** (top 5 stories con score)
- **Quote of the Day** (ZenQuotes API)
- **Random curiosità** (Wikipedia API con fallback)

### Locali Verbania
- **Eco Risveglio** (notizie VCO)
- **Altri portali locali** (da espandere)

## CSS Moods Disponibili

Ogni giorno viene scelto casualmente uno stile:

1. **brutalism** - Bold, raw, concrete
2. **vaporwave** - Pink/purple, retro-futurism
3. **swiss design** - Ultra minimal, grid-based
4. **cyberpunk** - Neon, dark, futuristic
5. **art deco** - Geometric, 1920s elegance
6. **memphis design** - Colorful, playful 80s
7. **bauhaus** - Functional, primary colors
8. **retro newspaper** - Vintage print aesthetic
9. **neo-minimalism** - Extreme whitespace
10. **dark academia** - Warm browns, scholarly
11. **synthwave** - Neon pink/blue, grid patterns
12. **grunge** - Distressed, rough, 90s alt

## Layout Principles

**Design moderno image-driven**:
- Hero image generata per mood del giorno
- Padding generoso (mai cramped)
- Typography respirante
- Mobile-first responsive
- Accessibilità WCAG AA

**Ispirazione**: PressLess layouts, modern editorial design

## Generation Flow

1. **Random mood selection** (dalle 12 opzioni)
2. **Content fetching**:
   - Hacker News API
   - Wikipedia random
   - Quote API
   - Eco Risveglio scraping
3. **LLM generation**:
   - CSS completo per mood
   - HTML content con sarcasmo Anacleto
   - Tono italiano caustico
4. **File writing**:
   - `index.html` (today)
   - `style.css` (daily)
   - `archive/YYYY-MM-DD.html`
5. **Git commit & push**
6. **GitHub Pages auto-deploy** (3-5 min)
7. **Live su dailyowl.it**

## Automation Setup

### Manual Run

```bash
# Test mode (no git push)
python3 /home/claude/brain/tools/agents/daily-owl-generator.py --test

# Production run
python3 /home/claude/brain/tools/agents/daily-owl-generator.py
```

### Cron (Automated)

Aggiunto a `scheduler.py`:

```python
schedule_task(
    hour=6, minute=0,  # 6:00 AM daily
    task_func='daily_owl_generator',
    script_path='/home/claude/brain/tools/agents/daily-owl-generator.py'
)
```

## Custom Domain Setup

### Cloudflare DNS

**Domain**: dailyowl.it (già su account Cloudflare)

**DNS Records**:
```
Type: CNAME
Name: @ (o www)
Content: giobi.github.io
Proxy: ✅ Proxied (orange cloud)
TTL: Auto
```

### GitHub Pages

File `CNAME` nella root:
```
dailyowl.it
```

GitHub Settings → Pages:
- Source: main branch / (root)
- Custom domain: dailyowl.it
- Enforce HTTPS: ✅

## Anacleto's Personality

**Parametri attivi**:
- Sarcasmo: 10/10 (caustico)
- Volgarità: 7/10 (controllata per pubblico)
- Umanità: 10/10 (super friendly)
- Tecnicismo: 5/10 (bilanciato)
- Loquacità: 6/10 (non telegrafico ma non logorroico)

**Tono**: Amicone, sarcastic, usa espressioni italiane, commenti pungenti sulla tech industry e le notizie locali.

## Monitoring

- **Git history**: Ogni deploy tracciato in git
- **GitHub Actions**: Deploy status visibile
- **Archive**: Storico completo di tutti i giorni

## Roadmap Future

- [ ] RSS feed per subscribers
- [ ] Newsletter email integration
- [ ] Social media auto-post (Telegram/Twitter)
- [ ] More local sources (altri portali VCO)
- [ ] GitHub Trending section
- [ ] Reddit programming highlights
- [ ] Weather Verbania widget
- [ ] Search functionality in archive

## Troubleshooting

### Generation fails

1. Check API tokens in `.env`:
   - `GEMINI_API_KEY`
   - `GITHUB_TOKEN` (optional, solo per auto-push)
2. Check Python deps: `requests`, `python-dotenv`
3. Check logs: script output shows detailed steps

### Site not updating

1. Check git push success
2. GitHub Actions status (repo → Actions tab)
3. Wait 5 minutes for GitHub Pages deploy
4. Check Cloudflare cache (purge se necessario)

### CSS looks broken

- Gemini generated invalid CSS (rare)
- Re-run generator per nuovo CSS
- Check browser console for errors

## Maintainer

**Giobi** (via Anacleto AI agent)
- Repo: https://github.com/giobi/daily-owl
- Site: https://dailyowl.it
- Email: giobi@giobi.com

---

*Daily Owl - Perché la coerenza è noiosa. 🦉*
