from contextlib import nullcontext
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bin import optimize_text as ot

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String(10000), nullable=False)
    verbs = db.Column(db.String(1000), nullable=False)
    synonyms = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Entry {self.id}>"

db.drop_all()
db.create_all()

@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        Entry.query.delete()

        resume_content = request.form["resume_text"]
        job_content = request.form["job_desc"]

        o = ot.Optimizer(job_content)
        output_data = o.optimize_body(resume_content)
        new_entries = []
        for k, v in output_data.items():
            def disp_list(ls):
                ret = ""
                for term in ls:
                    ret += f"{term}\n"

                return ret[:-1]

            new_entries.append(Entry(
                line = k,
                verbs = disp_list(v[0]),
                synonyms = disp_list(v[1])
            ))

        for e in new_entries:
            db.session.add(e)

        try:
            db.session.commit()
            return redirect("/")

        except:
            return "There was an issue adding your resume."

    else:
        entries = Entry.query.order_by(Entry.date_created).all()
        return render_template("index.html", entries=entries)

if __name__ == "__main__":
    app.run(debug=True)