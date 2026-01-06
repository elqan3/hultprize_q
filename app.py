from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# تعريف نموذج السؤال
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Question {self.id}>'

# صفحة المستخدم
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        question_text = request.form.get("question")
        if question_text:
            new_question = Question(text=question_text)
            db.session.add(new_question)
            db.session.commit()
        return redirect("/")
    return render_template("index.html")

# صفحة الادمن
@app.route("/admin")
def admin():
    questions = Question.query.order_by(Question.date_submitted.desc()).all()
    return render_template("admin.html", questions=questions)

if __name__ == "__main__":
    # إنشاء قاعدة البيانات إذا لم تكن موجودة
    with app.app_context():
        db.create_all()
    app.run(debug=True)
