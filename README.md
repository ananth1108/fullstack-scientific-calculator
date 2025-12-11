📟 Full-Stack Scientific Calculator

A modern, full-stack scientific calculator built using Flask (Python backend) and HTML/CSS/JavaScript (frontend).
This calculator safely evaluates mathematical expressions using Python’s AST, supports advanced scientific functions, and maintains a real-time calculation history.

🚀 Features
✅ Frontend

Clean, responsive UI built with HTML + CSS + JavaScript

Scientific function buttons:
sin, cos, tan, log, sqrt, π, e

Auto-insertion of parentheses for functions (sin( → sin())

Chained calculations (use previous result automatically)

Keyboard support for numbers, operators, and scientific keywords

History panel displayed alongside the calculator

✅ Backend

Built with Flask

Safe math evaluation using Python's AST
(No insecure eval() used)

Supports:

Operators → + - * / // % **

Functions → sin, cos, tan, log, sqrt

Constants → pi, e

Degree-based trigonometry

REST API endpoints:

POST /api/calculate

GET /api/history

POST /api/history/clear

✅ Storage

In-memory history storage
(Fast & perfect for demos; clears on restart)

🧩 Project Structure
📦 project-root
 ┣ 📂 templates
 ┃ ┗ 📄 index.html          # Frontend UI
 ┣ 📄 app.py                # Flask backend + safe evaluation
 ┣ 📄 README.md             # This file

🛠️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

2️⃣ Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

3️⃣ Install dependencies
pip install flask

4️⃣ Run the server
python app.py


The app will be available at:

http://127.0.0.1:5000

🔢 Supported Scientific Functions
Function	Example	Output
sin(x)	sin(30)	0.5
cos(x)	cos(60)	0.5
tan(x)	tan(45)	1.0
log(x)	log(e)	1.0
sqrt(x)	sqrt(25)	5
Constants	pi, e	usable directly
🔐 Safe Evaluation (AST-Based)

The backend uses Python's ast module to:

Parse expressions safely

Allow only approved operators & functions

Block all unsafe execution paths

No arbitrary Python code can be executed — ideal for a secure calculator app.

📜 API Endpoints
POST /api/calculate

Evaluate a math expression.

Body:

{
  "expression": "sin(30)+5"
}


Response:

{
  "result": 5.5
}

GET /api/history

Returns the last 10 calculations.

POST /api/history/clear

Clears stored history.

📸 Screenshots

(Add images from your running app here!)
You can drag & drop screenshots into your GitHub README later.

🧭 Roadmap / Future Enhancements

Persistent history using SQLite

Mode toggle: Degrees ↔ Radians

More scientific functions (log10, factorial, arcsin, arccos, arctan)

Dark mode UI

Export history as CSV

Deploy using Render / Vercel / PythonAnywhere

🤝 Contributing

Contributions are welcome!
Feel free to open issues, submit PRs, or suggest new features.

📄 License

MIT License © 2025
You are free to use, modify, and distribute the project.

⭐ If you like this project…

Please star the repository on GitHub — it helps a lot! 🌟
