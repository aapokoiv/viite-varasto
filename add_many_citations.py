"""
Citation Database Seeder

This script helps you populate your citation database with classic
computer science and software engineering references.

Usage: python3 add_many_citations.py
"""

from src.config import app, db
from sqlalchemy import text

def add_citation(keyword, citation_type, author, title, year, category=None):
    """Add a citation to the database."""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(
                text('INSERT INTO citations (keyword, type, author, title, year, category) VALUES (:keyword, :type, :author, :title, :year, :category) RETURNING id'),
                {'keyword': keyword, 'type': citation_type, 'author': author, 'title': title, 'year': year, 'category': category}
            )
            conn.commit()
            citation_id = result.fetchone()[0]
            cat_str = f" [{category}]" if category else ""
            print(f'  [{citation_type}] {author}: "{title}" ({year}){cat_str} -> {keyword}')
            return citation_id
    except Exception as e:
        print(f'  Failed to add {keyword}: {e}')
        return None

def main():
    """Adds 52 citations to the database."""
    print("\n" + "="*70)
    print("  Citation Database Seeder")
    print("="*70)
    print("\nAdding 52 classic computer science references...\n")
    
    citations = [
        # Tärkeät - Software Engineering & Design (13 citations)
        ('martin2008', 'book', 'Robert C. Martin', 'Clean Code: A Handbook of Agile Software Craftsmanship', 2008, 'tärkeät'),
        ('fowler1999', 'book', 'Martin Fowler', 'Refactoring: Improving the Design of Existing Code', 1999, 'tärkeät'),
        ('gamma1994', 'book', 'Erich Gamma et al.', 'Design Patterns: Elements of Reusable Object-Oriented Software', 1994, 'tärkeät'),
        ('hunt1999', 'book', 'Andrew Hunt and David Thomas', 'The Pragmatic Programmer', 1999, 'tärkeät'),
        ('evans2003', 'book', 'Eric Evans', 'Domain-Driven Design', 2003, 'tärkeät'),
        ('beck2002', 'book', 'Kent Beck', 'Test Driven Development: By Example', 2002, 'tärkeät'),
        ('martin2017', 'book', 'Robert C. Martin', 'Clean Architecture', 2017, 'tärkeät'),
        ('mcconnell2004', 'book', 'Steve McConnell', 'Code Complete', 2004, 'tärkeät'),
        ('pressman2014', 'book', 'Roger S. Pressman', 'Software Engineering: A Practitioner\'s Approach', 2014, 'tärkeät'),
        ('sommerville2015', 'book', 'Ian Sommerville', 'Software Engineering', 2015, 'tärkeät'),
        ('dijkstra1968', 'article', 'Edsger W. Dijkstra', 'Go To Statement Considered Harmful', 1968, 'tärkeät'),
        ('brooks1987', 'article', 'Frederick P. Brooks', 'No Silver Bullet', 1987, 'tärkeät'),
        ('parnas1972', 'article', 'David Parnas', 'On the Criteria To Be Used in Decomposing Systems into Modules', 1972, 'tärkeät'),
        
        # Ei niin tärkeän - Algorithms & Data Structures (10 citations)
        ('cormen2009', 'book', 'Thomas H. Cormen et al.', 'Introduction to Algorithms', 2009, 'ei niin tärkeän'),
        ('sedgewick2011', 'book', 'Robert Sedgewick and Kevin Wayne', 'Algorithms', 2011, 'ei niin tärkeän'),
        ('knuth1997', 'book', 'Donald E. Knuth', 'The Art of Computer Programming', 1997, 'ei niin tärkeän'),
        ('liskov1987', 'article', 'Barbara Liskov', 'Data Abstraction and Hierarchy', 1987, 'ei niin tärkeän'),
        ('hoare1969', 'article', 'C. A. R. Hoare', 'An Axiomatic Basis for Computer Programming', 1969, 'ei niin tärkeän'),
        ('codd1970', 'article', 'Edgar F. Codd', 'A Relational Model of Data for Large Shared Data Banks', 1970, 'ei niin tärkeän'),
        ('floyd1967', 'article', 'Robert W. Floyd', 'Assigning Meanings to Programs', 1967, 'ei niin tärkeän'),
        
        # Systems & Databases (9 citations)
        ('tanenbaum2014', 'book', 'Andrew S. Tanenbaum', 'Modern Operating Systems', 2014, 'järjestelmät'),
        ('garcia2009', 'book', 'Hector Garcia-Molina et al.', 'Database Systems: The Complete Book', 2009, 'järjestelmät'),
        ('date2003', 'book', 'Christopher J. Date', 'An Introduction to Database Systems', 2003, 'järjestelmät'),
        ('turing1936', 'article', 'Alan Turing', 'On Computable Numbers', 1936, 'järjestelmät'),
        ('church1936', 'article', 'Alonzo Church', 'An Unsolvable Problem of Elementary Number Theory', 1936, 'järjestelmät'),
        ('godel1931', 'article', 'Kurt Godel', 'On Formally Undecidable Propositions', 1931, 'järjestelmät'),
        ('ritchie1978', 'inproceedings', 'Dennis M. Ritchie and Ken Thompson', 'The UNIX Time-Sharing System', 1978, 'järjestelmät'),
        ('unix1974', 'inproceedings', 'Ken Thompson and Dennis M. Ritchie', 'The UNIX Time-Sharing System', 1974, 'järjestelmät'),
        
        # Modern & AI (11 citations)
        ('beck2001', 'inproceedings', 'Kent Beck et al.', 'Manifesto for Agile Software Development', 2001, 'moderni'),
        ('royce1970', 'inproceedings', 'Winston W. Royce', 'Managing the Development of Large Software Systems', 1970, 'moderni'),
        ('hinton2012', 'inproceedings', 'Geoffrey Hinton et al.', 'ImageNet Classification with Deep Convolutional Neural Networks', 2012, 'moderni'),
        ('krizhevsky2012', 'inproceedings', 'Alex Krizhevsky et al.', 'ImageNet Large Scale Visual Recognition Challenge', 2012, 'moderni'),
        ('vaswani2017', 'inproceedings', 'Ashish Vaswani et al.', 'Attention is All You Need', 2017, 'moderni'),
        ('goodfellow2014', 'inproceedings', 'Ian Goodfellow et al.', 'Generative Adversarial Nets', 2014, 'moderni'),
        ('lecun1998', 'inproceedings', 'Yann LeCun et al.', 'Gradient-based learning applied to document recognition', 1998, 'moderni'),
        ('pep8', 'misc', 'Guido van Rossum', 'PEP 8 -- Style Guide for Python Code', 2001, 'moderni'),
        ('rest', 'misc', 'Roy Fielding', 'Architectural Styles and the Design of Network-based Software Architectures', 2000, 'moderni'),
        ('microservices', 'misc', 'James Lewis and Martin Fowler', 'Microservices', 2014, 'moderni'),
        ('cloudcomputing', 'misc', 'NIST', 'The NIST Definition of Cloud Computing', 2011, 'moderni'),
        
        # Arkkitehtuuri & Patterns (9 citations)
        ('cqrs', 'misc', 'Greg Young', 'CQRS', 2010, 'arkkitehtuuri'),
        ('eventstore', 'misc', 'Martin Fowler', 'Event Sourcing', 2005, 'arkkitehtuuri'),
        ('bdd', 'misc', 'Dan North', 'Behavior Driven Development', 2006, 'arkkitehtuuri'),
        ('hexagonal', 'misc', 'Alistair Cockburn', 'Hexagonal Architecture', 2005, 'arkkitehtuuri'),
        ('solid', 'misc', 'Robert C. Martin', 'SOLID Principles', 2000, 'arkkitehtuuri'),
        ('ddd', 'misc', 'Eric Evans', 'Domain-Driven Design', 2003, 'arkkitehtuuri'),
        ('tdd', 'misc', 'Kent Beck', 'Test-Driven Development', 2000, 'arkkitehtuuri'),
        ('xpath', 'misc', 'W3C', 'XML Path Language', 1999, 'arkkitehtuuri'),
        ('sql', 'misc', 'ISO/IEC', 'SQL Standard', 1986, 'arkkitehtuuri'),

         # --- Extra 20 citations ---
        ('lamport1978', 'article', 'Leslie Lamport', 'Time, Clocks, and the Ordering of Events in a Distributed System', 1978, 'järjestelmät'),
        ('shannon1948', 'article', 'Claude E. Shannon', 'A Mathematical Theory of Communication', 1948, 'järjestelmät'),
        ('merkle1989', 'article', 'Ralph Merkle', 'A Certified Digital Signature', 1989, 'moderni'),
        ('rivest1978', 'article', 'Ron Rivest, Adi Shamir, Leonard Adleman', 'A Method for Obtaining Digital Signatures and Public-Key Cryptosystems', 1978, 'järjestelmät'),
        ('saltzer1974', 'article', 'Saltzer & Schroeder', 'The Protection of Information in Computer Systems', 1974, 'järjestelmät'),
        ('age2014', 'inproceedings', 'Dario Amodei et al.', 'Deep Learning Scaling Hypothesis', 2014, 'moderni'),
        ('mccarthy1960', 'article', 'John McCarthy', 'Recursive Functions of Symbolic Expressions', 1960, 'järjestelmät'),
        ('knuth1984', 'book', 'Donald E. Knuth', 'Literate Programming', 1984, 'tärkeät'),
        ('boehm1981', 'book', 'Barry Boehm', 'Software Engineering Economics', 1981, 'tärkeät'),
        ('nielsen1994', 'book', 'Jakob Nielsen', 'Usability Engineering', 1994, 'ei niin tärkeän'),
        ('fielding2000a', 'article', 'Roy Fielding', 'REST Architectural Style and Principles', 2000, 'arkkitehtuuri'),
        ('erl2008', 'book', 'Thomas Erl', 'SOA: Principles of Service Design', 2008, 'arkkitehtuuri'),
        ('bishop2006', 'book', 'Christopher Bishop', 'Pattern Recognition and Machine Learning', 2006, 'moderni'),
        ('kay1967', 'misc', 'Alan Kay', 'The Reactive Engine', 1967, 'tärkeät'),
        ('parnas1978', 'article', 'David Parnas', 'Designing Software for Ease of Extension and Contraction', 1978, 'tärkeät'),
        ('brooks1975', 'book', 'Frederick P. Brooks', 'The Mythical Man-Month', 1975, 'tärkeät'),
        ('abadi2005', 'article', 'Daniel Abadi et al.', 'Column-Oriented Database Systems', 2005, 'järjestelmät'),
        ('stonebraker2007', 'article', 'Michael Stonebraker et al.', 'The End of an Architectural Era', 2007, 'järjestelmät'),
        ('bishop1995', 'article', 'Christopher Bishop', 'Neural Networks for Pattern Recognition', 1995, 'moderni'),
        ('grady1995', 'book', 'Grady Booch', 'Object-Oriented Analysis and Design', 1995, 'arkkitehtuuri'),
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
