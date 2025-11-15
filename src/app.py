from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import get_citations, create_ref
from config import app, test_env
from util import validate_ref

@app.route("/")
def index():
    todos = get_citations()
    unfinished = len([todo for todo in todos if not todo.done])
    return render_template("index.html", todos=todos, unfinished=unfinished) 

@app.route("/new_ref")
def new():
    return render_template("new_ref.html")

@app.route("/create_ref", methods=["POST"])
def ref_creation():
    ref_type = request.form.get("ref_type")
    author = request.form.get("ref_author")
    title = request.form.get("ref_title")
    year = request.form.get("ref_year")

    try:
        year_int = validate_ref(ref_type, author, title, year)
        create_ref(ref_type, author, title, year_int)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_ref")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
