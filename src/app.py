from flask import (
    Response,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy.exc import SQLAlchemyError

from config import app, test_env
from db_helper import reset_db
from repositories.bibtex_repository import all_citations_to_bibtex
from repositories.citation_repository import (
    create_ref,
    delete_ref,
    get_citation_by_id,
    get_citations,
    get_filters,
    update_ref,
)
from util import UserInputError, get_page_range, validate_article_fields, validate_ref


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/new_ref")
def new():
    option = request.args.get("ref_type", "article")
    return render_template("new_ref.html", option=option)


@app.route("/view_refs")
def ref_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("ref_amount", 10, type=int)

    filters = {
        "query": request.args.get("query", ""),
        "type": request.args.get("type"),
        "category": request.args.get("category"),
        "year_from": request.args.get("year_from", 0, type=int),
        "year_to": request.args.get("year_to", 2025, type=int)
    }

    data = get_citations(page, per_page, filters)

    return render_template(
        "ref_list.html",
        refs=data["items"],
        page=data["page"],
        pages=data["pages"],
        page_range=get_page_range(data["page"], data["pages"]),
        available_filters=get_filters(),
        per_page=per_page,
        active_filters={
            "query": filters["query"],
            "type": filters["type"],
            "category": filters["category"],
            "year_from": filters["year_from"],
            "year_to": filters["year_to"]
        }
    )


@app.route("/create_ref", methods=["POST"])
def ref_creation():
    ref_type = request.form.get("ref_type")
    keyword = request.form.get("ref_keyword")
    category = request.form.get("ref_category") or None
    author = request.form.get("ref_author")
    title = request.form.get("ref_title")
    year = request.form.get("ref_year")
    doi = request.form.get("ref_doi") or None
    journal = request.form.get("ref_journal") or None
    volume = request.form.get("ref_volume") or None
    pages = request.form.get("ref_pages") or None
    publisher = request.form.get("ref_publisher") or None
    booktitle = request.form.get("ref_booktitle") or None


    try:
        if ref_type == "article":
            volume = validate_article_fields(journal, volume, pages)
        year_int = validate_ref(ref_type, keyword, author, title, year)
    except UserInputError as error:
        flash(str(error))
        return redirect("/new_ref")

    try:
        create_ref(ref_type, keyword, author, title, year_int, doi, category, journal, volume, pages, publisher, booktitle)
    except SQLAlchemyError:
        flash("Database error while creating reference")
        return redirect("/new_ref")

    flash("Reference succesfully created.", "success")
    return redirect(url_for('index'))


@app.route("/edit_ref/<int:ref_id>", methods=["GET", "POST"])
def ref_edit(ref_id):
    ref = get_citation_by_id(ref_id)
    if not ref:
        abort(404)

    option = request.args.get("ref_type", ref.type)

    if request.method == "GET":
        return render_template("edit_ref.html", ref=ref, option=option)

    if request.method == "POST":
        ref_type = request.form.get("ref_type")
        keyword = request.form.get("ref_keyword")
        category = request.form.get("ref_category") or None
        author = request.form.get("ref_author")
        title = request.form.get("ref_title")
        year = request.form.get("ref_year")
        doi = request.form.get("ref_doi") or None
        journal = request.form.get("ref_journal") or None
        volume = request.form.get("ref_volume") or None
        pages = request.form.get("ref_pages") or None
        publisher = request.form.get("ref_publisher") or None
        booktitle = request.form.get("ref_booktitle") or None


        try:
            if ref_type == "article":
                volume = validate_article_fields(journal, volume, pages)
            year_int = validate_ref(ref_type, keyword, author, title, year)
        except UserInputError as error:
            flash(str(error))
            return redirect("/edit_ref/" + str(ref_id))

        try:
            update_ref(ref.id, ref_type, keyword, author, title,
                       year_int, doi, category, journal, volume, pages, publisher, booktitle)
        except SQLAlchemyError:
            flash("Database error while updating reference")
            return redirect("/edit_ref/" + str(ref_id))

        flash("Reference succesfully edited.", "success")
        return redirect("/view_refs")

    return redirect(url_for('ref_list'))


@app.route("/delete_ref/<int:ref_id>", methods=["POST"])
def ref_delete(ref_id):
    ref = get_citation_by_id(ref_id)
    if not ref:
        abort(404)
    delete_ref(ref.id)
    flash("Reference succesfully deleted.", "success")
    return redirect("/view_refs")

@app.route("/export_bibtex")
def export_bibtex():
    bibtex_data = all_citations_to_bibtex()
    return Response(
        bibtex_data,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": "attachment;filename=citations.bib"}
    )

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({'message': "db reset"})
