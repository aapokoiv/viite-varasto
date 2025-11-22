from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citation_by_id(ref_id):
    sql = text("SELECT * FROM citations WHERE id = :ref_id")
    result = db.session.execute(sql, {"ref_id": ref_id}).fetchone()
    return Citation(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9]) if result else None

def get_citations(page: int=1, per_page: int=10, filters = None):
    filters = {"query":"","type":""} if filters is None else filters

    offset = (page - 1) * per_page
    sql = "SELECT id, type, author, title, year FROM citations WHERE 1=1"
    count_sql = "SELECT COUNT(*) FROM citations WHERE 1=1"

    if filters["query"]:
        sql += " AND (title ILIKE :query OR author ILIKE :query)"
        count_sql += " AND (title ILIKE :query OR author ILIKE :query)"
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

def create_ref(ref_type, author, title, year, journal, volume, pages, publisher, booktitle):
    params = {
        "type": ref_type,
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
    "INSERT INTO citations (type, author, title, year, journal, volume, pages, publisher, booktitle) "
    "VALUES (:type, :author, :title, :year, :journal, :volume, :pages, :publisher, :booktitle)"
    )

    db.session.execute(sql, params)
    db.session.commit()

def update_ref(ref_id, ref_type, author, title, year, booktitle, journal, volume, pages, publisher):
    params = {
        "ref_id": ref_id,
        "type": ref_type,
        "author": author, 
        "title": title, 
        "year": year,
        "journal": journal,
        "volume": volume,
        "pages": pages,
        "publisher": publisher,
        "booktitle": booktitle
    }
    sql = text("""UPDATE citations SET type = :type, author = :author, title = :title, year = :year, 
            journal = :journal, volume= :volume, pages = :pages, publisher = :publisher, booktitle = :booktitle 
            WHERE id = :ref_id""")
        
    db.session.execute(sql, params)
    db.session.commit()