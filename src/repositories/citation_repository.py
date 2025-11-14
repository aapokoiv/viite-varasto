from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citations():
    result = db.session.execute(text("SELECT id, type, author, title, year FROM citations"))
    todos = result.fetchall()
    return [Citation(todo[0], todo[1], todo[2]) for todo in todos] 

def set_done(todo_id):
    sql = text("UPDATE citations SET done = TRUE WHERE id = :id")
    db.session.execute(sql, { "id": todo_id })
    db.session.commit()

def create_todo(content):
    sql = text("INSERT INTO citations (content) VALUES (:content)")
    db.session.execute(sql, { "content": content })
    db.session.commit()
