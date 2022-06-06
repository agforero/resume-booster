from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bin import optimize_text as ot

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(10000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Entry {self.id}>"
        
db.drop_all()
db.create_all()

@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        resume_content = request.form["resume_text"]
        job_content = request.form["job_desc"]

        o = ot.Optimizer(job_content)
        o.optimize_text(resume_content)

        output_text = str(o.display_optimized())
        new_entry = Entry(content=output_text)

        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect("/")

        except:
            return "There was an issue adding your resume."

    else:
        entry = Entry.query.order_by(Entry.date_created.desc()).first()
        return render_template("index.html", entry=entry)

if __name__ == "__main__":
    app.run(debug=True)