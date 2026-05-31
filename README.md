# Adam Creative Studios // Bot Network
## Complete 5-Bot Discord Infrastructure

---

## 📁 Project Structure

```
ACS_Network/
├── config.json                   ← MASTER CONFIG — Fill this in first
├── requirements.txt              ← Python dependencies
├── ecosystem.config.js           ← PM2 process manager (run all bots at once)
│
├── shared/                       ← Shared utilities imported by all bots
│   ├── database.py               ← Central SQLite database manager
│   ├── embeds.py                 ← Branded embed factory
│   ├── ticket_views.py           ← Reusable ticket UI components
│   └── config_loader.py          ← Loads config.json
│
├── database/
│   └── master.db                 ← Auto-generated SQLite database
│
├── logs/                         ← PM2 log output files
│
└── bots/
    ├── core_bot/                 ← Bot 1: Adam Creative (Hub)
    │   ├── main.py
    │   └── cogs/
    │       ├── verification.py   ← OAuth2-style email verification
    │       ├── autoresponder.py  ← FAQ auto-replies
    │       └── leveling.py       ← XP rank system
    │
    ├── staff_bot/                ← Bot 2: Adam Creative Staff
    │   ├── main.py
    │   └── cogs/
    │       ├── modmail.py        ← 2-way DM thread system + transcript archiver
    │       ├── logging.py        ← ABSOLUTE audit logger (every event)
    │       ├── moderation.py     ← warn, kick, ban, timeout, purge, userinfo
    │       └── backups.py        ← 24h automatic database backup task
    │
    ├── design_bot/               ← Bot 3: Adam Creative Design
    │   ├── main.py
    │   ├── assets/
    │   │   └── watermark.png     ← Place your AC watermark here
    │   └── cogs/
    │       ├── tickets.py        ← Design commission ticket panel
    │       ├── watermarker.py    ← /watermark + /showcase commands
    │       └── invoice.py        ← /invoice (3-way routing) + /tax
    │
    ├── dev_bot/                  ← Bot 4: Adam Creative Development
    │   ├── main.py
    │   └── cogs/
    │       ├── tickets.py        ← Dev commission ticket panel
    │       ├── instance_tracker.py ← Host bot status tracking
    │       └── invoice.py        ← /invoice + /tax
    │
    └── customs_bot/              ← Bot 5: Adam Creative Customs
        ├── main.py
        └── cogs/
            ├── tickets.py        ← Livery/asset commission panel
            └── invoice.py        ← /invoice + /tax
```

---

## ⚡ Setup Guide

### Step 1 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Configure config.json
Open `config.json` and fill in every field:

1. **`guild_id`** — Right-click your Discord server → Copy Server ID
2. **`tokens`** — Paste each bot token from the Discord Developer Portal
3. **`channels`** — Paste the channel IDs for all log/order channels
4. **`roles`** — Paste the role IDs for verified, staff, admin, etc.
5. **`settings.ticket_category_*`** — Category IDs where tickets will be created

### Step 3 — Create Bot Applications
Go to https://discord.com/developers/applications and create **5 separate bot applications**:
- Adam Creative
- Adam Creative Staff
- Adam Creative Design
- Adam Creative Development
- Adam Creative Customs

For each bot:
- Enable **ALL Privileged Gateway Intents** (Presence, Server Members, Message Content)
- Copy the token into `config.json`
- Invite to your server with permissions: `Administrator` (recommended for logging)

### Step 4 — Add Your Watermark
Place your transparent AC monogram PNG at:
```
bots/design_bot/assets/watermark.png
```

### Step 5 — Run the Bots

**Option A — Individual (for testing):**
```bash
cd ACS_Network
python bots/core_bot/main.py
python bots/staff_bot/main.py
# etc.
```

**Option B — All at once via PM2 (for production):**
```bash
npm install -g pm2
pm2 start ecosystem.config.js
pm2 save
pm2 startup       # Auto-start on server reboot
```

---

## 🎯 Slash Commands Reference

### Core Bot
| Command | Description |
|---|---|
| `/setup_verify` | Post the verification panel (Admin) |
| `/faq` | Show FAQ embed |
| `/rank [member]` | View XP rank card |
| `/leaderboard` | View server XP leaderboard |

### Staff Bot
| Command | Description |
|---|---|
| `/warn @member reason` | Issue a warning |
| `/warnings @member` | View a member's warnings |
| `/kick @member reason` | Kick a member |
| `/ban @member reason` | Ban a member |
| `/timeout @member minutes` | Timeout a member |
| `/purge amount` | Delete messages |
| `/userinfo [@member]` | View detailed user info |
| `/modmail_close` | Close and archive a modmail thread |
| `/backup_now` | Trigger immediate database backup (Admin) |

### Design Bot
| Command | Description |
|---|---|
| `/setup_order_panel` | Post the design commission panel (Admin) |
| `/watermark image` | Apply AC watermark to an image |
| `/showcase image title` | Post to portfolio channel (Staff) |
| `/invoice @client amount memo` | Send 3-way invoice |
| `/tax amount` | Calculate Roblox marketplace tax |

### Dev Bot
| Command | Description |
|---|---|
| `/setup_order_panel` | Post the dev commission panel (Admin) |
| `/register_instance client_name bot_name process_name` | Register a hosted bot |
| `/update_status process_name status` | Update an instance's status |
| `/instance_list` | View all registered instances |
| `/invoice @client amount memo` | Send 3-way invoice |
| `/tax amount` | Calculate Roblox marketplace tax |

### Customs Bot
| Command | Description |
|---|---|
| `/setup_order_panel` | Post the customs commission panel (Admin) |
| `/drop_templates` | Post template resource links in ticket |
| `/invoice @client amount memo` | Send 3-way invoice |
| `/tax amount` | Calculate Roblox marketplace tax |

---

## 📋 Discord Server Channel Setup

Create these channels and paste their IDs into config.json:

**Logs (hidden from members):**
- `#absolute-logs` → absolute_logs
- `#message-logs` → message_logs
- `#member-logs` → member_logs
- `#server-logs` → server_logs
- `#voice-logs` → voice_logs
- `#role-logs` → role_logs
- `#system-backups` → system_backups (admin-only)
- `#invoice-logs` → invoice_logs
- `#modmail-threads` → modmail_threads

**Public/Semi-Public:**
- `#verify` → verify_gate
- `#order-design` → order_design
- `#order-dev` → order_dev
- `#order-customs` → order_customs
- `#portfolio` → portfolio
- `#dev-status` → dev_status

---

## 🛡️ Security Notes
- Keep `config.json` in your `.gitignore` — **NEVER push tokens to GitHub**
- Only your top admin role should see `#absolute-logs`, `#system-backups`
- The modmail system only logs messages sent directly TO the Staff bot's DMs — no private DM spying
- Voice logging tracks joins/leaves only, not mute/deafen toggles
