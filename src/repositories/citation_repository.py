from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citations(page=1, per_page=10):
    offset = (page - 1) * per_page
    sql = text("SELECT id, type, author, title, year FROM citations ORDER BY id LIMIT :limit OFFSET :offset")
    result = db.session.execute(sql, {"limit": per_page, "offset": offset})
    infos = result.fetchall()
    
    total_result = db.session.execute(text("SELECT COUNT(*) FROM citations"))
    total = total_result.scalar()
    
    return {
        "items": [Citation(info[0], info[1], info[2], info[3], info[4]) for info in infos],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }

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