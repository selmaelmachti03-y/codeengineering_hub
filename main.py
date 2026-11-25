from pathlib import Path
import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "codehub.db"

app = FastAPI(title="CodeEngineering Hub", description="A beginner-friendly computer engineering learning hub")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

LESSONS = [
    {
        "id": 1, "category": "Programming", "level": "Beginner", "duration": "20 min",
        "title": "How Programs Work", "summary": "Understand source code, compilers, interpreters, and the edit-run-debug cycle.",
        "objectives": ["Explain what a program is", "Compare a compiler and an interpreter", "Describe the basic development cycle"],
        "sections": [
            ("What is a program?", "A program is a set of instructions that tells a computer how to perform a task. Instructions are written in a programming language such as Python, Java, or C++."),
            ("Source code and execution", "Source code is the human-readable text written by a developer. A compiler translates source code into another form before execution. An interpreter executes instructions through a runtime environment."),
            ("The development cycle", "A common workflow is: understand the problem, write code, run it, test the result, find bugs, and improve the solution. This cycle is repeated throughout software development.")
        ],
        "code": 'name = "Ada"\nprint(f"Hello, {name}!")',
        "code_note": "This Python program stores a name in a variable and prints a greeting.",
        "question": "What is source code?", "choices": ["The human-readable instructions written by a developer", "A computer monitor", "A database backup"], "answer": 0,
        "explanation": "Source code is the human-readable form of a program before it is executed or translated."
    },
    {
        "id": 2, "category": "Programming", "level": "Beginner", "duration": "25 min",
        "title": "Variables and Data Types", "summary": "Learn how programs store information using variables and common data types.",
        "objectives": ["Define a variable", "Recognize common data types", "Choose an appropriate type for a value"],
        "sections": [
            ("Variables", "A variable is a named reference to a value. Variables make programs easier to read and allow information to change while a program runs."),
            ("Common data types", "Integers represent whole numbers, floats represent decimal numbers, strings represent text, and booleans represent True or False values."),
            ("Choosing a type", "Choose a type based on the meaning of the data. A person's age can be an integer; a username is text; whether a user is active can be a boolean.")
        ],
        "code": 'age = 21              # integer\nprice = 19.99         # float\nusername = "sam"      # string\nis_active = True      # boolean',
        "code_note": "Python determines these types from the values assigned.",
        "question": "Which data type is best for True or False?", "choices": ["String", "Boolean", "Float"], "answer": 1,
        "explanation": "A boolean stores one of two logical values: True or False."
    },
    {
        "id": 3, "category": "Computer Science", "level": "Beginner", "duration": "30 min",
        "title": "Algorithms and Big-O", "summary": "Discover what algorithms are and why efficiency matters as data grows.",
        "objectives": ["Define an algorithm", "Understand input and output", "Recognize O(1), O(n), and O(n²)"],
        "sections": [
            ("What is an algorithm?", "An algorithm is a finite, ordered set of steps used to solve a problem. A recipe is a familiar example: it takes ingredients as input and produces a meal as output."),
            ("Measuring efficiency", "Time complexity describes how an algorithm's work grows as input size grows. Big-O notation focuses on the growth rate rather than exact seconds."),
            ("Three common examples", "O(1) is constant work, such as reading an item by array index. O(n) grows proportionally with the input, such as checking every item. O(n²) often appears with nested loops over the same collection.")
        ],
        "code": 'numbers = [4, 8, 2, 9]\nfor number in numbers:  # O(n)\n    print(number)',
        "code_note": "The loop visits each element once, so its work grows linearly with the list length.",
        "question": "A loop visits every item in a list once. Its time complexity is usually:", "choices": ["O(1)", "O(n)", "O(n²)"], "answer": 1,
        "explanation": "The number of operations grows in proportion to the number of list items: O(n)."
    },
    {
        "id": 4, "category": "Software Engineering", "level": "Beginner", "duration": "25 min",
        "title": "Object-Oriented Programming", "summary": "Explore classes, objects, attributes, methods, and encapsulation.",
        "objectives": ["Distinguish a class from an object", "Identify attributes and methods", "Explain encapsulation"],
        "sections": [
            ("Classes and objects", "A class is a blueprint describing data and behavior. An object is a concrete instance created from that blueprint. A Car class can describe many individual car objects."),
            ("Attributes and methods", "Attributes store an object's state, such as its color. Methods define behavior, such as start() or stop()."),
            ("Encapsulation", "Encapsulation groups data and related behavior and controls how internal state is accessed. It helps keep code organized and reduces accidental changes.")
        ],
        "code": 'class Student:\n    def __init__(self, name):\n        self.name = name\n\n    def introduce(self):\n        return f"My name is {self.name}"\n\nstudent = Student("Mina")\nprint(student.introduce())',
        "code_note": "Student is the class; student is an object created from it.",
        "question": "What is an object?", "choices": ["A blueprint only", "An instance of a class", "A programming language"], "answer": 1,
        "explanation": "An object is an instance created from a class."
    },
    {
        "id": 5, "category": "Databases", "level": "Beginner", "duration": "30 min",
        "title": "Relational Databases and SQL", "summary": "Learn tables, rows, primary keys, and basic SQL queries.",
        "objectives": ["Describe a relational table", "Explain primary keys", "Read a basic SELECT query"],
        "sections": [
            ("Relational database basics", "A relational database stores structured data in tables. Each table contains rows (records) and columns (fields). Tables can be related using key columns."),
            ("Keys", "A primary key uniquely identifies each row. A foreign key references a key in another table and helps represent relationships."),
            ("Reading SQL", "SQL is a language used to define, query, and modify relational data. SELECT retrieves columns, FROM identifies a table, and WHERE filters rows.")
        ],
        "code": 'SELECT name, email\nFROM students\nWHERE active = TRUE\nORDER BY name;',
        "code_note": "This query returns the names and email addresses of active students, sorted by name.",
        "question": "What does a primary key do?", "choices": ["Uniquely identifies a row", "Formats a web page", "Encrypts every file"], "answer": 0,
        "explanation": "A primary key provides a unique identifier for each row in a table."
    },
    {
        "id": 6, "category": "Web Development", "level": "Beginner", "duration": "25 min",
        "title": "How the Web Works", "summary": "Understand browsers, servers, HTTP requests, responses, and URLs.",
        "objectives": ["Explain client and server roles", "Describe an HTTP request", "Recognize common HTTP methods"],
        "sections": [
            ("Client and server", "A browser is a client: it requests resources. A web server receives requests, performs work, and sends responses such as HTML, JSON, images, or files."),
            ("HTTP request and response", "HTTP is a protocol for communication on the web. A request includes a method, path, headers, and sometimes a body. A response includes a status code, headers, and content."),
            ("Common methods", "GET usually reads data, POST submits data or creates a resource, PUT replaces a resource, and DELETE requests removal.")
        ],
        "code": 'GET /api/lessons HTTP/1.1\nHost: example.com\nAccept: application/json',
        "code_note": "This is a simplified HTTP request asking a server for lesson data.",
        "question": "Which HTTP method is commonly used to retrieve data?", "choices": ["DELETE", "GET", "POST"], "answer": 1,
        "explanation": "GET is the standard HTTP method for retrieving a representation of a resource."
    },
    {
        "id": 7, "category": "Computer Networks", "level": "Beginner", "duration": "25 min",
        "title": "IP Addresses and DNS", "summary": "Learn how devices are addressed and how domain names are resolved.",
        "objectives": ["Explain the purpose of an IP address", "Describe DNS", "Distinguish a domain from an IP address"],
        "sections": [
            ("IP addresses", "An IP address identifies a network interface for communication using the Internet Protocol. IPv4 addresses are commonly written as four numbers separated by dots."),
            ("What DNS does", "The Domain Name System (DNS) translates human-friendly domain names into records such as IP addresses. It works like a distributed naming directory."),
            ("Putting it together", "When you visit a website, your device may ask DNS for the server's address, then connect to that server using network protocols.")
        ],
        "code": 'Domain: example.com\nExample IPv4 address: 93.184.216.34\n\nBrowser -> DNS lookup -> IP address -> Web server',
        "code_note": "The address is an illustrative example; DNS records can change and may return multiple addresses.",
        "question": "What is the main role of DNS?", "choices": ["Translate domain names into DNS records such as IP addresses", "Compile Python code", "Store images in a browser"], "answer": 0,
        "explanation": "DNS provides the naming system that helps clients find services using domain names."
    },
    {
        "id": 8, "category": "Operating Systems", "level": "Beginner", "duration": "30 min",
        "title": "Processes, Memory, and the OS", "summary": "Explore what an operating system manages when applications run.",
        "objectives": ["Describe an operating system", "Distinguish a process from a program", "Understand memory management"],
        "sections": [
            ("Operating system responsibilities", "An operating system manages hardware resources and provides services to applications. Examples include process scheduling, filesystems, memory management, and device access."),
            ("Programs and processes", "A program is a stored set of instructions. A process is a running instance of a program, with its own execution state and allocated resources."),
            ("Memory management", "The operating system coordinates memory allocation and isolation. Virtual memory gives processes an organized address space and helps protect them from one another.")
        ],
        "code": 'Program on disk\n      |\n      | run\n      v\nProcess in memory\n      |\n      +-- CPU time\n      +-- memory space\n      +-- open resources',
        "code_note": "A process is the running form of a program, managed by the operating system.",
        "question": "What is a process?", "choices": ["A running instance of a program", "A computer brand", "A database column"], "answer": 0,
        "explanation": "A process is a program in execution, together with its current state and resources."
    }
]

@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS progress (
            lesson_id INTEGER PRIMARY KEY, completed INTEGER NOT NULL DEFAULT 0,
            selected_answer INTEGER, updated_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS favorites (
            lesson_id INTEGER PRIMARY KEY, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")

init_db()

def get_lesson(lesson_id: int):
    return next((lesson for lesson in LESSONS if lesson["id"] == lesson_id), None)

def dashboard_data():
    with db() as conn:
        completed = {r["lesson_id"] for r in conn.execute("SELECT lesson_id FROM progress WHERE completed=1")}
        favorites = {r["lesson_id"] for r in conn.execute("SELECT lesson_id FROM favorites")}
    return completed, favorites

@app.get("/", response_class=HTMLResponse)
def home(request: Request, q: str = "", category: str = "All"):
    completed, favorites = dashboard_data()
    lessons = LESSONS
    if category != "All":
        lessons = [l for l in lessons if l["category"] == category]
    if q.strip():
        term = q.casefold().strip()
        lessons = [l for l in lessons if term in (l["title"] + " " + l["summary"] + " " + l["category"]).casefold()]
    categories = ["All"] + sorted({l["category"] for l in LESSONS})
    return templates.TemplateResponse("index.html", {
        "request": request, "lessons": lessons, "categories": categories,
        "selected_category": category, "q": q, "completed": completed,
        "favorites": favorites, "total": len(LESSONS)
    })

@app.get("/lesson/{lesson_id}", response_class=HTMLResponse)
def lesson_page(request: Request, lesson_id: int):
    lesson = get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    completed, favorites = dashboard_data()
    with db() as conn:
        row = conn.execute("SELECT selected_answer FROM progress WHERE lesson_id=?", (lesson_id,)).fetchone()
    return templates.TemplateResponse("lesson.html", {
        "request": request, "lesson": lesson, "completed": completed,
        "favorites": favorites, "selected_answer": row["selected_answer"] if row else None
    })

@app.post("/lesson/{lesson_id}/quiz")
def submit_quiz(lesson_id: int, answer: int = Form(...)):
    lesson = get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    correct = answer == lesson["answer"]
    with db() as conn:
        conn.execute("""INSERT INTO progress (lesson_id, completed, selected_answer, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(lesson_id) DO UPDATE SET
            completed=excluded.completed, selected_answer=excluded.selected_answer,
            updated_at=CURRENT_TIMESTAMP""", (lesson_id, int(correct), answer))
    return RedirectResponse(f"/lesson/{lesson_id}?result={'correct' if correct else 'tryagain'}", status_code=303)

@app.post("/lesson/{lesson_id}/complete")
def mark_complete(lesson_id: int):
    if not get_lesson(lesson_id):
        raise HTTPException(status_code=404, detail="Lesson not found")
    with db() as conn:
        conn.execute("""INSERT INTO progress (lesson_id, completed) VALUES (?, 1)
            ON CONFLICT(lesson_id) DO UPDATE SET completed=1, updated_at=CURRENT_TIMESTAMP""", (lesson_id,))
    return RedirectResponse(f"/lesson/{lesson_id}", status_code=303)

@app.post("/lesson/{lesson_id}/favorite")
def toggle_favorite(lesson_id: int):
    if not get_lesson(lesson_id):
        raise HTTPException(status_code=404, detail="Lesson not found")
    with db() as conn:
        exists = conn.execute("SELECT 1 FROM favorites WHERE lesson_id=?", (lesson_id,)).fetchone()
        if exists:
            conn.execute("DELETE FROM favorites WHERE lesson_id=?", (lesson_id,))
        else:
            conn.execute("INSERT INTO favorites (lesson_id) VALUES (?)", (lesson_id,))
    return RedirectResponse("/", status_code=303)

@app.get("/favorites", response_class=HTMLResponse)
def favorites_page(request: Request):
    completed, favorites = dashboard_data()
    lessons = [l for l in LESSONS if l["id"] in favorites]
    return templates.TemplateResponse("index.html", {
        "request": request, "lessons": lessons, "categories": ["All"],
        "selected_category": "All", "q": "", "completed": completed,
        "favorites": favorites, "total": len(LESSONS), "favorites_view": True
    })

@app.get("/health")
def health():
    return {"status": "ok", "lessons": len(LESSONS)}
