from flask import Flask, render_template, request, redirect, url_for, g
from database import db, Todo
import os
from flask_cors import CORS
app = Flask(__name__, template_folder="templates")
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
todo_file = os.path.join(basedir, 'todo_list.txt')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "todos.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.before_request
def load_data_to_g():
    todos = Todo.query.all()
    g.todos = todos
    g.todo = None
    
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=4000)

@app.route("/add", methods=["POST"])
def add_todo():
    import pdb; pdb.set_trace()
    todo = Todo (
        name=request.form["todo"],
    )
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/test")
def test():
    import pdb; pdb.set_trace()
    todo = Todo (
        name=request.form["todo"],
    )
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/remove/<int:id>", methods=["GET", "POST"])
def remove_todo(id):
    db.session.delete(Todo.query.filter_by(id=id).first())
    db.session.commit()
    return redirect(url_for("index"))