# CodeEngineering Hub

A small full-stack learning platform for computer engineering fundamentals. It ships with a curated set of English lessons, code examples, quizzes, search, category filters, saved lessons, and local progress tracking.

## Features

- 8 built-in lessons across programming, computer science, software engineering, databases, web development, networks, and operating systems.
- Search lessons by title, topic, or description.
- Filter lessons by category.
- Read structured lessons with learning objectives and code examples.
- Answer a short quiz after each lesson and receive feedback.
- Save and unsave favorite lessons.
- Track completed lessons and overall progress.
- SQLite database is created automatically on first launch.
- Responsive interface for desktop and mobile.

## Tech stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, Jinja2 templates
- **Database:** SQLite (Python standard library)
- **Server:** Uvicorn

## Run locally

### 1. Requirements

Install Python 3.10 or newer.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the app

```bash
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

The SQLite database (`codehub.db`) is generated automatically in the project folder.

## Project structure

```text
codeengineering_hub/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   └── lesson.html
└── static/
    └── style.css
```

## Main routes

| Route | Purpose |
|---|---|
| `/` | Lesson library, search, category filter, progress |
| `/lesson/{id}` | Lesson content and quiz |
| `/lesson/{id}/quiz` | Submit a quiz answer |
| `/lesson/{id}/complete` | Mark a lesson complete |
| `/lesson/{id}/favorite` | Toggle a saved lesson |
| `/favorites` | View saved lessons |
| `/health` | Simple health-check endpoint |

## Upload to GitHub

1. Create a new empty repository on GitHub, for example `codeengineering-hub`.
2. Extract this ZIP file.
3. Open a terminal inside the extracted `codeengineering_hub` folder.
4. Run:

```bash
git init
git add .
git commit -m "Build CodeEngineering Hub learning platform"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/codeengineering-hub.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Notes and possible next improvements

- This is a portfolio/demo application. Progress and favorites are shared in the local SQLite database; it does not yet have user accounts or cloud synchronization.
- Lesson material is included directly in `main.py`, so the app works without an external content API.
- Good next steps: move lessons into database tables, add user authentication, add unit tests, and deploy the app.

## Learning content note

The included lessons are original introductory explanations written for this project. They are educational material, not a replacement for a full university course or official technical documentation.
