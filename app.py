from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# =========================
# PostgreSQL (Supabase)
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql+psycopg://postgres:189919442005elqantri@"
    "db.xclxujpgynytqbxoueyl.supabase.co:5432/postgres"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# Database Model
# =========================
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# =========================
# Create Tables
# =========================
with app.app_context():
    db.create_all()

# =========================
# Routes
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        if content:
            q = Question(content=content)
            db.session.add(q)
            db.session.commit()
        return redirect(url_for("index"))

    questions = Question.query.all()
    return render_template("index.html", questions=questions)

@app.route("/admin")
def admin():
    questions = Question.query.all()
    return render_template("admin.html", questions=questions)

# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(debug=True)

