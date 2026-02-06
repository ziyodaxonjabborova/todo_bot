# 📝 Async Task Manager Bot

An asynchronous Telegram bot for high-efficiency task tracking, built with **Python 3.10+** and **Aiogram 3.x**. Focuses on clean state management and optimized SQLite3 interactions.

---

## ⚡ Tech Stack & Core Logic

- **Framework:** `Aiogram 3.x` (Asynchronous Bot API)
- **Database:** `SQLite3` (Embedded Relational Data)
- **State Mgmt:** `python-dotenv` & `environs` (Secure Config)
- **Logic:** Decoupled Database Layer (CRUD optimized)



---

## 🗄️ Database Schema

To ensure data integrity and optimized querying, the system utilizes the following relational structure:

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

<div align="center">
  <sub>
    <b>Ziyodaxon Jabborova</b> | 2026 | <b>Python Backend Engineer</b>
  </sub>
</div>

