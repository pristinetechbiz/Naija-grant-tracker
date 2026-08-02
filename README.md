# 🇳🇬 NaijaGrant Tracker

A Telegram bot that helps Nigerians discover **grants, scholarships, loans, and empowerment programmes**.

Users can search, browse by category, save opportunities, set preferences, and receive notifications when new grants are added.

---

## Features

| Feature | Description |
|---------|-------------|
| 🔍 Search | Keyword search across titles, descriptions, organisations |
| 📂 Categories | Scholarships, Business, Loans, Youth, Women, Agriculture, Skills… |
| 🆕 Latest | Most recently added / updated open opportunities |
| ⭐ Saved | Personal bookmark list |
| ⚙️ Preferences | Preferred state + notification toggle |
| 🛠️ Admin panel | Add, close, delete grants; broadcast updates; stats |

**Pre-loaded sample data** includes real programmes such as:

- NELFUND Student Loan
- BOI Guaranteed Loans for Women (GLOW)
- NiYA Startup Grants
- 3MTT Technical Talent Programme
- BOI–NYSC Entrepreneurship Programme
- SMEDAN Conditional Grants
- PTDF Scholarships
- and more

---

## Quick Start

### 1. Create the bot on Telegram

1. Open Telegram and talk to **[@BotFather](https://t.me/BotFather)**
2. Send `/newbot` and follow the prompts
3. Copy the **API token** you receive

### 2. Get your Telegram user ID (for admin access)

Talk to **[@userinfobot](https://t.me/userinfobot)** and copy your numeric ID.

### 3. Install & configure

```bash
cd nigeria_grant_tracker
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env:
#   BOT_TOKEN=123456:ABC-your-token
#   ADMIN_IDS=your_numeric_id
```

### 4. Run

```bash
python bot.py
```

You should see: `NaijaGrant Tracker starting…`

Open Telegram, find your bot, and send `/start`.

---

## User Commands

| Command | Action |
|---------|--------|
| `/start` | Welcome + main menu |
| `/search` | Search by keyword |
| `/categories` | Browse by category |
| `/latest` | Newest open grants |
| `/saved` | Your saved grants |
| `/prefs` | State & notification settings |
| `/help` | Help text |

Reply-keyboard buttons mirror these commands.

---

## Admin Commands

(Only users listed in `ADMIN_IDS` can use these)

| Command | Action |
|---------|--------|
| `/admin` | Show admin help |
| `/addgrant` | Interactive wizard to add a new grant |
| `/listgrants` | Show recent grants with IDs |
| `/deletegrant <id>` | Permanently delete a grant |
| `/closgrant <id>` | Mark grant as closed |
| `/stats` | Quick database stats |
| `/broadcast <msg>` | Message all users who enabled notifications |

When you add a grant with `/addgrant`, users who have notifications enabled (and matching category preference) are automatically notified.

---

## Project Structure

```
nigeria_grant_tracker/
├── bot.py                 # Entry point
├── database.py            # SQLite models & queries
├── handlers/
│   ├── user.py            # User-facing commands & callbacks
│   └── admin.py           # Admin commands & add-grant conversation
├── data/
│   └── grants.db          # Created automatically on first run
├── requirements.txt
├── .env.example
└── README.md
```

---

## Customisation Ideas

- Add more sample grants or scrape official portals (respect robots.txt & terms)
- Connect a PostgreSQL database for production
- Add scheduled jobs (APScheduler is already a dependency) for deadline reminders
- Multi-language support (English + Pidgin / Hausa / Yoruba / Igbo)
- Web dashboard for non-Telegram admins
- Integration with Google Forms or official APIs when available

---

## Disclaimer

This bot is an **information aggregator**. Always verify eligibility, deadlines, and application procedures on the **official website** of each programme before applying. The maintainers are not responsible for changes made by the original providers.

---

## License

MIT – feel free to use, modify, and deploy for community benefit.

---

## Deploy 24/7 (Recommended: Railway)

Railway is currently one of the easiest platforms for polling Telegram bots. Free trial credits usually cover the first few months for a small bot.

### Option A – Railway (Recommended)

1. **Push the code to GitHub**
   ```bash
   cd nigeria_grant_tracker
   git init
   git add .
   git commit -m "NaijaGrant Tracker"
   # Create a new empty repo on GitHub, then:
   git remote add origin https://github.com/YOUR_USERNAME/naija-grant-tracker.git
   git branch -M main
   git push -u origin main
   ```

2. **Go to [railway.app](https://railway.app)** → Sign up with GitHub

3. **New Project** → **Deploy from GitHub repo** → select your repo

4. **Add Environment Variables** (Variables tab):
   | Variable     | Value                          |
   |--------------|--------------------------------|
   | `BOT_TOKEN`  | Your token from @BotFather     |
   | `ADMIN_IDS`  | Your Telegram numeric user ID  |

5. Railway will detect Python and start the bot automatically (`python bot.py`).

6. Check the **Deployments → Logs**. You should see:
   ```
   NaijaGrant Tracker starting…
   ```

7. Open Telegram and send `/start` to your bot.

> **Note:** The SQLite database lives on the container filesystem. On free/hobby plans it may reset if the service is rebuilt. For production, later switch to Railway’s PostgreSQL plugin (code change needed).

### Option B – Render (not ideal for free tier)

Render’s free web services **sleep after 15 minutes** of inactivity. A polling bot will stop receiving updates. Use only a paid always-on instance, or switch the bot to webhooks.

### Option C – Cheap VPS (most control)

- Hetzner, Contabo, Oracle Cloud free tier, or any $3–6/month VPS
- Install Python 3.12, clone the repo, create a systemd service or use `pm2` / `screen` / `tmux`

Example systemd unit (`/etc/systemd/system/naija-grant.service`):

```ini
[Unit]
Description=NaijaGrant Tracker Bot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/nigeria_grant_tracker
EnvironmentFile=/home/ubuntu/nigeria_grant_tracker/.env
ExecStart=/home/ubuntu/nigeria_grant_tracker/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable --now naija-grant
```

### Option D – Other platforms

- **Fly.io** – good, but needs a bit more config (`fly.toml`)
- **PythonAnywhere** – possible but less convenient for long-polling
- Specialised bot hosts (TeleBotHost, etc.) – check their current free tiers

---

## Production Tips

1. Keep `BOT_TOKEN` and `ADMIN_IDS` only in environment variables — never commit `.env`.
2. For serious use, migrate from SQLite to PostgreSQL (Railway has a one-click plugin).
3. Add a simple health-check or log monitoring so you know if the bot goes down.
4. Regularly update grant data with `/addgrant` or by extending the seed data.
