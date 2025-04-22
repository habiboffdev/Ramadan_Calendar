# Ramadan Calendar Bot

> **My very first Telegram bot (6th grade)**
>
> A simple Python Telegram bot that delivers Ramadan prayer schedules on demand. Built before I fully understood APIs, I manually populated a local SQLite database with 30 days of suhoor and iftar timings, debugging pre-dawn sessions over three days.

---

## 🔍 Overview

- **Purpose:** Send daily Ramadan timings via Telegram commands.  
- **Background:** No reliable internet; data entered manually on my mom’s phone tether.

---

## 🤖 Bot Commands

| Command     | Description                           |
| ----------- | ------------------------------------- |
| `/start`    | Show welcome message and usage tips   |
| `/today`    | Display today’s suhoor & iftar times  |
| `/date YYYY-MM-DD` | Lookup prayer times for a specific date |
| `/help`     | List all available commands           |

---

## ⚙️ Tech Stack

- **Language:** Python 3.x  
- **Libraries:** python-telegram-bot (Telegram API), SQLite3  
- **Data:** Manually entered Ramadan calendar in `ramadan.sqlite`

---

## 🚀 Quickstart

1. **Clone & enter**
   ```bash
   git clone https://github.com/habiboffdev/Ramadan_Calendar.git
   cd Ramadan_Calendar
   ```
2. **Install dependencies**
   ```bash
   pip install python-telegram-bot sqlite3
   ```
3. **Configure**  
   - Copy `.env.example` to `.env` and set your `TELEGRAM_BOT_TOKEN`.
4. **Run the bot**
   ```bash
   python main.py
   ```
5. **Interact**  
   - Message your bot on Telegram to get prayer times.

---

## 📝 Key Takeaways

- **Perseverance:** Overcame limited resources by hand-entering data and iterating on pre-dawn debug sessions.  
- **Learning by Doing:** Gained early exposure to Telegram bot development and database integration.  
- **Problem-Solving:** Solved lookup and date-parsing challenges without prior API knowledge.

---

_Last updated: April 22, 2025_

