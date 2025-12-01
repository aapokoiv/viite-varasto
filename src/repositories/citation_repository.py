import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from sqlalchemy import text
from config import db, app
from entities.citation import Citation

def get_all_citations():
    sql = text("SELECT * FROM citations")
    result = db.session.execute(sql)
    citations = []
    for row in result.fetchall():
        citations.append(Citation(row[0], row[1],row[2], row[3], row[4], row[5],
                                  row[6], row[7], row[8], row[9], row[10]))
    return citations

def get_citation_by_id(ref_id):
    sql = text("SELECT * FROM citations WHERE id = :ref_id")
    result = db.session.execute(sql, {"ref_id": ref_id}).fetchone()
    return Citation(result[0],
                    result[1],
                    result[2],
                    result[3],
                    result[4],
                    result[5],
                    result[6],
                    result[7],
                    result[8],
                    result[9],
                    result[10]) if result else None

def get_citations(page: int=1, per_page: int=10, filters = None):
    filters = {"query":"","type":""} if filters is None else filters

    offset = (page - 1) * per_page
    sql = "SELECT id, keyword, type, author, title, year FROM citations WHERE 1=1"
    count_sql = "SELECT COUNT(*) FROM citations WHERE 1=1"

    if filters["query"]:
        sql += " AND (title ILIKE :query OR author ILIKE :query OR keyword ILIKE :query)"
        count_sql += " AND (title ILIKE :query OR author ILIKE :query OR keyword ILIKE :query)"
    if filters["type"] and filters["type"] != "-":
        sql += " AND type = :type"
        count_sql += " AND type = :type"

    sql += " ORDER BY id LIMIT :limit OFFSET :offset"

    result = db.session.execute(text(sql), {
        "limit": per_page,
        "offset": offset,
        "query": f"%{filters["query"]}%",
        "type": filters["type"]
        })
    count_result = db.session.execute(text(count_sql), {
        "query": f"%{filters["query"]}%",
        "type": filters["type"]
        })

    infos = result.fetchall()
    total = count_result.scalar()

    return {
        "items": [Citation(info[0], info[1], info[2], info[3], info[4], info[5]) for info in infos],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }

def get_filters():
    sql = text("SELECT DISTINCT type FROM citations")
    sql2 = text("SELECT DISTINCT year FROM citations")
    # Clean queries to include only relevant information.
    types = ["-"] + [type[0] for type in db.session.execute(sql).fetchall()]
    years = ["-"] + [year[0] for year in db.session.execute(sql2).fetchall()]

    return {"types": types,
            "years": years}

def create_ref(ref_type, keyword, author, title, year, journal=None, volume=None, pages=None, publisher=None, booktitle=None):
    params = {
        "type": ref_type,
        "keyword": keyword,
        "author": author, 
        "title": title, 
        "year": year,
        "journal": journal,
        "volume": volume,
        "pages": pages,
        "publisher": publisher,
        "booktitle": booktitle
    }

    sql = text(
    "INSERT INTO citations (type, keyword, author, title, year, journal, volume, pages, publisher, booktitle) "
    "VALUES (:type, :keyword, :author, :title, :year, :journal, :volume, :pages, :publisher, :booktitle)"
    )

    db.session.execute(sql, params)
    db.session.commit()

def create_test_refs_quickly(amount: int):
    with app.app_context():
        for i in range(1, amount + 1):
            sql = text(
                """INSERT INTO citations (type, keyword, author, title, year)
                   VALUES (:type, :keyword, :author, :title, :year)"""
            )
            db.session.execute(sql, {
                'type': 'article',
                'keyword': f'kw{i}',
                'author': f'Author {i}',
                'title': f'Ref {i}',
                'year': '2000'})
        db.session.commit()

def update_ref(ref_id, ref_type, keyword, author, title, year, journal=None, volume=None, pages=None, publisher=None, booktitle=None):
    params = {
        "ref_id": ref_id,
        "type": ref_type,
        "keyword": keyword,
        "author": author, 
        "title": title, 
        "year": year,
        "journal": journal,
        "volume": volume,
        "pages": pages,
        "publisher": publisher,
        "booktitle": booktitle
    }
    sql = text("""UPDATE citations SET type = :type, keyword = :keyword, author = :author, title = :title, year = :year,
            journal = :journal, volume= :volume, pages = :pages, publisher = :publisher, booktitle = :booktitle 
            WHERE id = :ref_id""")

    db.session.execute(sql, params)
    db.session.commit()

def delete_ref(ref_id):
    sql = text("DELETE FROM citations WHERE id = :ref_id")
    db.session.execute(sql, {"ref_id": ref_id})
    db.session.commit()
