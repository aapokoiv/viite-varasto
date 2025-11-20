from flask import redirect, render_template, request, jsonify, flash, abort
from db_helper import reset_db
from repositories.citation_repository import get_citations, get_filters, create_ref, get_citation_by_id, update_ref
from config import app, test_env
from util import validate_ref

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/new_ref")
def new():
    option = request.args.get("ref_type", "article")
    ref_author = request.args.get("author", "")
    ref_title = request.args.get("title", "")
    ref_year = request.args.get("year", "")
    return render_template("new_ref.html", option=option)

@app.route("/view_refs")
def ref_list():
    page = request.args.get("page", 1, type=int)
    per_page = 10

    filters = {
        "query": request.args.get("query", ""),
        "type": request.args.get("type")
    }

    data = get_citations(page, per_page, filters)
    
    return render_template(
        "ref_list.html",
        refs=data["items"],
        page=data["page"],
        pages=data["pages"],
        available_filters=get_filters(),
        active_filters={
            "query": filters["query"],
            "type": filters["type"]
        }
    )

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

@app.route("/edit_ref/<int:ref_id>", methods=["GET" ,"POST"])
def ref_edit(ref_id):
    ref = get_citation_by_id(ref_id)
    if not ref:
        abort(404)
    if request.method == "GET":
        return render_template("edit_ref.html", ref=ref)
    if request.method == "POST":
        author = request.form.get("ref_author")
        title = request.form.get("ref_title")
        year = request.form.get("ref_year")
        
        try:
            year_int = validate_ref(ref.type, author, title, year)
            update_ref(ref.id, author, title, year_int)
        except Exception as error:
            flash(str(error))
            return redirect("/edit_ref/"+ str(ref_id))
        return redirect("/view_refs")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
