from flask import Flask, render_template, request, redirect
from datetime import datetime
import json
import os

app = Flask(__name__)

# مسار آمن للكتابة على Render
DATA_FILE = os.path.join("/tmp", "questions.json")

# إنشاء الملف إذا لم يكن موجود
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        question_text = request.form.get("question")
        if question_text:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                questions = json.load(f)
            questions.append({
                "text": question_text,
                "date_submitted": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            })
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=4)
        return redirect("/")
    return render_template("index.html")

@app.route("/admin")
def admin():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    questions = list(reversed(questions))
    return render_template("admin.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
