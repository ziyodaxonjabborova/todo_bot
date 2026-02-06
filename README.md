# 📝 Async Task Manager Bot

An asynchronous Telegram bot for high-efficiency task tracking, built with **Python 3.10+** and **Aiogram 3.x**. Focuses on clean state management and optimized SQLite3 interactions.

---

## ⚡ Tech Stack & Core Logic

- **Framework:** `Aiogram 3.x` (Asynchronous Bot API)
- **Database:** `SQLite3` (Embedded Relational Data)
- **State Mgmt:** `python-dotenv` & `environs` (Secure Config)
- **Logic:** Decoupled Database Layer (CRUD optimized)



---

## 🛠 Key Features

- **Full CRUD:** Create, Read, Update, and Delete tasks.
- **Dynamic Filtering:** Query by `pending`, `done`, or `all`.
- **Input Sanitization:** Case-insensitive search and whitespace stripping.
- **Atomic Commits:** Secure database transactions using Context Managers.

---

## 🚀 Quick Start

1. **Environment:** Create `.env` with `BOT_TOKEN=your_token`.
2. **Install:** `pip install -r requirements.txt`
3. **Run:** `python main.py`

---

## 🏗 Schema Preview

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
<sub>Ziyodaxon Jabborova | 2026 | Python Backend Engineer</sub>
