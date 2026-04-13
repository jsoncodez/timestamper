# 🕒 TimeStamper

A lightweight, portable desktop productivity tool for quickly recording timestamps, tracking time intervals, and attaching notes.

---

TimeStamper is a Python-based desktop application built with Tkinter that allows users to instantly record timestamps with a single keypress or click. It automatically tracks the time elapsed between events and supports inline note editing for context.

The project focuses on usability, responsive event handling, and simple local data persistence without external dependencies.

---

## 🚀 Features

- ⚡ Instant timestamp recording (Spacebar / Enter / Button)
- ⏱️ Automatic time delta tracking between entries
- 📝 Inline note editing (double-click to edit)
- 💾 Local file persistence (no database required)
- 🔄 Debounced auto-save system for efficient file writing
- 🧠 Smart input handling (prevents accidental timestamp creation while editing notes)
- 🧹 Clear history with confirmation prompt
- 🖥️ Live updating clock display
- 📦 Packaged as a single executable (no installation required at runtime)

---

## 🎮 Controls

| Action | Input |
|--------|------|
| Record timestamp | `Space` or `Enter` |
| Edit note | Double-click note column |
| Save note | `Enter` or click outside field |
| Clear all data | Click "CLEAR HISTORY" |

---

## 🧱 Tech Stack

- Python 3
- Tkinter (GUI framework)
- ttk Treeview (table interface)
- datetime module (time tracking)
- File I/O (local persistence)

---

## 📁 Data Storage

All timestamps are stored locally in containing directory.

No external database or internet connection is required.

---

## Design Highlights

### ✔ Event-driven architecture
The application is fully driven by user interactions (keyboard and mouse events), ensuring a responsive and intuitive workflow.

### ✔ Efficient persistence strategy
Uses debounced saving to reduce unnecessary disk writes while ensuring data integrity.

### ✔ Lightweight & portable
The application can be packaged into a single executable for easy distribution without requiring installation.

---

## Potential Future Improvements

- Export to CSV / Excel
- Search and filter timestamps
- Global hotkey implementation
- Tagging system for entries
- Dark mode UI
- Multi-project tracking support
- Cloud sync capability
- Data Encryption

---

## [Download portable Application](https://github.com/jsoncodez/timestamper/releases/tag/v0.1.2)



### Run from source

```bash
git clone https://github.com/jsoncodez/timestamper.git
cd timestamper
python timestamper.py