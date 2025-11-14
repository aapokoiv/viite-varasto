from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citations():
    result = db.session.execute(text("SELECT id, type, author, title, year FROM citations"))
    infos = result.fetchall()
    return [Citation(info[0], info[1], info[2], info[3], info[4]) for info in infos]

def create_todo(content):
    sql = text("INSERT INTO citations (content) VALUES (:content)")
    db.session.execute(sql, { "content": content })
    db.session.commit()
