from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citations(page: int=1, per_page: int=10, filters: dict=None):
    offset = (page - 1) * per_page
    sql = "SELECT id, type, author, title, year FROM citations WHERE 1=1"
    count_sql = "SELECT COUNT(*) FROM citations WHERE 1=1"

    if filters["type"] and filters["type"] != "-":
        sql += " AND type = :type"
        count_sql += " AND type = :type"

    sql += " ORDER BY id LIMIT :limit OFFSET :offset"
    
    result = db.session.execute(text(sql), {
        "limit": per_page,
        "offset": offset,
        "type": filters["type"]
        })
    count_result = db.session.execute(text(count_sql), {"type": filters["type"]})

    infos = result.fetchall()
    total = count_result.scalar()
    
    return {
        "items": [Citation(info[0], info[1], info[2], info[3], info[4]) for info in infos],
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

def create_ref(ref_type, author, title, year):
    sql = text(
    "INSERT INTO citations (type, author, title, year) "
    "VALUES (:type, :author, :title, :year)"
    )
    params = {
        "type": ref_type,
        "author": author,
        "title": title,
        "year": year
    }
    db.session.execute(sql, params)
    db.session.commit()