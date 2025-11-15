from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citations():
    result = db.session.execute(text("SELECT id, type, author, title, year FROM citations"))
    infos = result.fetchall()
    return [Citation(info[0], info[1], info[2], info[3], info[4]) for info in infos]

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