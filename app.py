from flask import Flask, render_template, request, redirect
from datetime import datetime
import json
import os

app = Flask(__name__)

# ملف حفظ الأسئلة
DATA_FILE = "questions.json"

# إنشاء الملف إذا لم يكن موجود
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# صفحة المستخدم
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        question_text = request.form.get("question")
        if question_text:
            # قراءة الأسئلة الحالية
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                questions = json.load(f)
            # إضافة السؤال الجديد
            questions.append({
                "text": question_text,
                "date_submitted": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            })
            # حفظ الأسئلة مرة أخرى
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=4)
        return redirect("/")
    
    return render_template("index.html")

# صفحة الادمن
@app.route("/admin")
def admin():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    # عرض الأحدث أولاً
    questions = list(reversed(questions))
    return render_template("admin.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
