# Habit Tracker

A desktop habit-tracking app built with [Flet](https://flet.dev/), featuring a custom title bar, a warm beige UI, and per-habit streak and completion-rate analytics. Built as the final project for introduction to python course.

## Description

Habit Tracker is a local-first desktop application for logging daily habits and watching consistency build up over time. Habits and completion logs are stored as plain JSON in a local `data/` folder, so there's no account, server, or sync to deal with — you run the app, tick boxes, and your data stays on your machine.

The app is split into three main views:

- **Dashboard** — your day-to-day check-in surface.
- **Statistics** — completion rates and streak analytics over arbitrary date ranges.
- **History** — a calendar-style view of past activity.

## Visuals

<!-- TODO: Add a screenshot -->

_Screenshots coming soon._

## Requirements

- **Python** 3.10 or newer (the codebase uses `list[dict]` / `bool | None` style type hints)
- **pip**
- Windows, macOS, or Linux desktop (Flet renders a native window)

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/<your-username>/Flet-Habit-Tracker.git
cd Flet-Habit-Tracker
pip install -r requirements.txt
```

Key dependency: **flet 0.84.0** (with `flet-desktop` and `flet-charts`). The full pinned list is in `requirements.txt`.

## Usage

From the project root, run:

```bash
python main.py
```

A 1000×600 window will open with a custom title bar (minimize / maximize / close buttons are wired up manually since the native title bar is hidden). Use the left sidebar to switch between **Dashboard**, **Statistics**, and **History**.

On first launch, the app will create the JSON files it needs inside `data/` automatically.

## Features

- Add and delete habits (each gets a UUID and a creation date)
- Toggle daily completion per habit
- **Current streak** and **longest streak** calculations
- Completion rate over any date range, plus a cumulative-rate series for charting
- Configurable week start (Monday or Sunday) via `data/settings.json`
- Local JSON storage with automatic recovery if a file is missing or corrupted
- Custom Quicksand font and a warm beige / brown theme (`#F5F1EB`, `#7D673F`, …)
- Frameless window with a custom draggable title bar

## Configuration

Settings live in `data/settings.json` and are created with these defaults on first run:

```json
{
    "theme": "light",
    "font_size": "medium",
    "language": "English",
    "week_starts_on": "Monday",
    "reminder_enabled": true,
    "reminder_time": "08:00",
    "weekly_summary": true
}
```

## Project Structure

```
Flet-Habit-Tracker/
├── main.py                  # Flet entry point, window setup, custom title bar
├── requirements.txt
├── assets/
│   └── fonts/
│       └── Quicksand-VariableFont_wght.ttf
├── backend/
│   ├── habit_manager.py     # add / delete / list habits
│   ├── log_manager.py       # create / toggle / query completion logs
│   ├── stats_engine.py      # streaks, date ranges, completion rates
│   └── storage.py           # JSON load/save with fallback on missing/corrupt files
├── frontend/
│   ├── layout.py            # sidebar + content area, navigation
│   ├── dashboard.py
│   ├── statistics.py
│   ├── history.py
│   ├── settings.py
│   ├── calendar.py          # calendar component
│   └── chart.py
└── data/
    ├── habits.json
    ├── logs.json
    └── settings.json
```

## Data Model

**Habit**

```json
{
    "id": "uuid-hex",
    "name": "Drink water",
    "created_at": "2026-05-11"
}
```

**Log entry**

```json
{
    "habit_id": "uuid-hex",
    "date": "2026-05-11",
    "completed": true
}
```

## Roadmap

- [ ] Backup system for `data/` files
- [ ] Working reminders 
- [ ] Weekly summary reports
- [ ] Theme / font-size / language switching at runtime

## Contributing

Thanks for your interest in Habit Tracker! Since this is an active course project, please note:

- **During the grading period:** external pull requests will not be merged. You're still welcome to open issues for bugs or suggestions — they'll be reviewed once grading is complete.
- **After grading:** contributions are welcome via the workflow below.

### Reporting Bugs

Open an issue and include:

- What you were doing when the bug occurred
- What you expected to happen
- What actually happened (error messages, screenshots if relevant)
- Your OS and Python version
- Relevant excerpts from `data/habits.json` or `data/logs.json` if the bug seems data-related (please remove anything personal)

### Suggesting Features

Open an issue with the `enhancement` label and describe:

- The problem you're trying to solve
- How you imagine the feature working
- Any alternatives you've considered

### Development Setup

```bash
git clone https://github.com/<your-username>/Flet-Habit-Tracker.git
cd Flet-Habit-Tracker
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Submitting a Pull Request

1. Fork the repository and create a branch from `main`:
   `git checkout -b feature/short-description` or `fix/short-description`
2. Make your changes. Keep PRs focused — one feature or fix per PR.
3. Test the app manually: add a habit, log it, toggle completion, check Statistics and History views.
4. Commit with a clear message (see below).
5. Push to your fork and open a PR against `main`. Describe what changed and why, and link any related issue.

### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) where it doesn't conflict with the existing style of the file you're editing.
- Match the formatting conventions already used in the codebase (spacing, naming, type hints on function signatures).
- Use type hints for new functions, matching the existing `list[dict]` / `bool | None` style.
- Keep `backend/` free of UI code and `frontend/` free of direct file I/O — go through `backend/storage.py`.

### What to Avoid

- Don't commit anything in `data/` — those files are user data, not source.
- Don't add heavy dependencies without discussing in an issue first; Flet + stdlib is the current footprint.
- Don't reformat unrelated files in the same PR as a feature change.

## Authors and Acknowledgment

- **Authors:** Wei-Li Yu, Yu-Xuan Wu, Yu-Ning Peng 
- **Course:** 1142 Python — Final Project
- **Built with:** [Flet](https://flet.dev/), [Quicksand font](https://fonts.google.com/specimen/Quicksand)

## Support / Contact

For any inquiries, please contact me at masonyu463@gmail.com.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Project Status

In active development as a course final project.