"""
Citation Database Seeder

This script helps you populate your citation database with classic
computer science and software engineering references.

Usage: python3 add_many_citations.py
"""

from src.config import app, db
from sqlalchemy import text

def add_citation(keyword, citation_type, author, title, year):
    """Add a citation to the database."""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(
                text('INSERT INTO citations (keyword, type, author, title, year) VALUES (:keyword, :type, :author, :title, :year) RETURNING id'),
                {'keyword': keyword, 'type': citation_type, 'author': author, 'title': title, 'year': year}
            )
            conn.commit()
            citation_id = result.fetchone()[0]
            print(f'  [{citation_type}] {author}: "{title}" ({year}) -> {keyword}')
            return citation_id
    except Exception as e:
        print(f'  Failed to add {keyword}: {e}')
        return None

def main():
    """Adds 20 citations to the database."""
    print("\n" + "="*70)
    print("  Citation Database Seeder")
    print("="*70)
    print("\nAdding 20 classic computer science references...\n")
    
    citations = [
        # Books
        ('martin2008', 'book', 'Robert C. Martin', 'Clean Code: A Handbook of Agile Software Craftsmanship', 2008),
        ('fowler1999', 'book', 'Martin Fowler', 'Refactoring: Improving the Design of Existing Code', 1999),
        ('gamma1994', 'book', 'Erich Gamma et al.', 'Design Patterns: Elements of Reusable Object-Oriented Software', 1994),
        ('hunt1999', 'book', 'Andrew Hunt and David Thomas', 'The Pragmatic Programmer', 1999),
        ('evans2003', 'book', 'Eric Evans', 'Domain-Driven Design', 2003),
        ('beck2002', 'book', 'Kent Beck', 'Test Driven Development: By Example', 2002),
        ('martin2017', 'book', 'Robert C. Martin', 'Clean Architecture', 2017),
        ('mcconnell2004', 'book', 'Steve McConnell', 'Code Complete', 2004),
        
        # Articles
        ('dijkstra1968', 'article', 'Edsger W. Dijkstra', 'Go To Statement Considered Harmful', 1968),
        ('brooks1987', 'article', 'Frederick P. Brooks', 'No Silver Bullet', 1987),
        ('parnas1972', 'article', 'David Parnas', 'On the Criteria To Be Used in Decomposing Systems into Modules', 1972),
        ('liskov1987', 'article', 'Barbara Liskov', 'Data Abstraction and Hierarchy', 1987),
        ('hoare1969', 'article', 'C. A. R. Hoare', 'An Axiomatic Basis for Computer Programming', 1969),
        ('codd1970', 'article', 'Edgar F. Codd', 'A Relational Model of Data for Large Shared Data Banks', 1970),

        # Conference Papers
        ('beck2001', 'inproceedings', 'Kent Beck et al.', 'Manifesto for Agile Software Development', 2001),
        ('royce1970', 'inproceedings', 'Winston W. Royce', 'Managing the Development of Large Software Systems', 1970),
        ('ritchie1978', 'inproceedings', 'Dennis M. Ritchie and Ken Thompson', 'The UNIX Time-Sharing System', 1978),

        # Misc 
        ('pep8', 'misc', 'Guido van Rossum', 'PEP 8 -- Style Guide for Python Code', 2001),
        ('rest', 'misc', 'Roy Fielding', 'Architectural Styles and the Design of Network-based Software Architectures', 2000),
        ('microservices', 'misc', 'James Lewis and Martin Fowler', 'Microservices', 2014),
    ]

    with app.app_context():
        success_count = 0
        for citation in citations:
            if add_citation(*citation):
                success_count += 1

        print("\n" + "="*70)
        print(f"  Done! Successfully added {success_count} out of {len(citations)} citations")
        print("="*70 + "\n")

if __name__ == "__main__":
    main()
