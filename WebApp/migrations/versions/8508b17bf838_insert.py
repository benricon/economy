"""Insert

Revision ID: 8508b17bf838
Revises: b96c2f92b6dc
Create Date: 2024-12-13 23:03:17.625256

"""
from alembic import op
from models import Category
import sqlalchemy as sa
from models import db


# revision identifiers, used by Alembic.
revision = '8508b17bf838'
down_revision = 'b96c2f92b6dc'
branch_labels = None
depends_on = 'b96c2f92b6dc'


def upgrade():
    try:
        # Add level 1  and 3 categories
        categories = [
            Category(id=1, name='Dagligvarer', level=1),
            Category(id=2, name='Bolig', level=1),
            Category(id=3, name='Transport', level=1),
            Category(id=4, name='Personlig pleje', level=1),
            Category(id=5, name='Fornøjelser/Fritid', level=1),
            Category(id=6, name='Personforsikringer', level=1),
            Category(id=7, name='Anden gæld', level=1),
            Category(id=8, name='Opsparing', level=1),
            Category(id=9, name='Øvrige udgifter', level=1),
            Category(id=10, name='Hobby', level=1),
            Category(id=11, name='Intern Overførsel', level=1),
            Category(id=12, name='Delt Betaling', level=1),
            Category(id=13, name='Bjarne', level=3),
            Category(id=14, name='Rebecca', level=3),
            Category(id=15, name='Fælles', level=3),

            Category(id=16, name='Bager', level=2, parent=1),
            Category(id=17, name='Takeaway', level=2, parent=1),
            Category(id=18, name='Fiskeforretning', level=2, parent=1),
            Category(id=19, name='Grønhandel', level=2, parent=1),
            Category(id=20, name='Kioskvarer', level=2, parent=1),
            Category(id=21, name='Slagter', level=2, parent=1),
            Category(id=22, name='Specialforretning', level=2, parent=1),
            Category(id=23, name='Supermarked', level=2, parent=1),
            Category(id=24, name='Vinhandel', level=2, parent=1),
            Category(id=25, name='Novo Food', level=2, parent=1),
            Category(id=26, name='Andet indkøb', level=2, parent=1),

            Category(id=27, name='El', level=2, parent=2),
            Category(id=28, name='Husleje', level=2, parent=2),
            Category(id=29, name='Forsikring', level=2, parent=2),
            Category(id=30, name='Vand', level=2, parent=2),
            Category(id=31, name='Varme', level=2, parent=2),
            Category(id=32, name='Andet bolig', level=2, parent=2),
            
            Category(id=33, name='Bilforsikring', level=2, parent=3),
            Category(id=34, name='Billån', level=2, parent=3),
            Category(id=35, name='Brændstof', level=2, parent=3),
            Category(id=36, name='Bus/Tog', level=2, parent=3),
            Category(id=37, name='Færge/Bro', level=2, parent=3),
            Category(id=38, name='Vægtafgift', level=2, parent=3),
            Category(id=39, name='Parkering', level=2, parent=3),
            Category(id=40, name='Mekaniker', level=2, parent=3),
            Category(id=41, name='Taxa', level=2, parent=3),
            Category(id=42, name='Udstyr', level=2, parent=3),
            Category(id=43, name='Andet transport', level=2, parent=3),

            Category(id=44, name='Briller', level=2, parent=4),
            Category(id=45, name='Frisør', level=2, parent=4),
            Category(id=46, name='Plejeprodukter', level=2, parent=4),
            Category(id=47, name='Psykolog', level=2, parent=4),
            Category(id=48, name='Massage mm', level=2, parent=4),
            Category(id=49, name='Smykker/Accessories', level=2, parent=4),
            Category(id=50, name='Sportsudstyr', level=2, parent=4),
            Category(id=51, name='Tandlæge', level=2, parent=4),
            Category(id=52, name='Medicin', level=2, parent=4),
            Category(id=53, name='Tasker/Tøj/Sko', level=2, parent=4),
            Category(id=54, name='Andet personlig', level=2, parent=4),

            Category(id=55, name='Aviser/Blade/Bøger', level=2, parent=5),
            Category(id=56, name='Bytur', level=2, parent=5),
            Category(id=57, name='Cafe/Restaurant', level=2, parent=5),
            Category(id=58, name='Biograf', level=2, parent=5),
            Category(id=59, name='Koncert', level=2, parent=5),
            Category(id=60, name='Teater', level=2, parent=5),
            Category(id=61, name='Ferie', level=2, parent=5),
            Category(id=62, name='Film/Musik', level=2, parent=5),
            Category(id=63, name='Fritidsaktivitet', level=2, parent=5),
            Category(id=64, name='Gaver', level=2, parent=5),
            Category(id=65, name='Kurser', level=2, parent=5),
            Category(id=66, name='Kæledyr', level=2, parent=5),
            Category(id=67, name='Velgørenhed', level=2, parent=5),
            Category(id=68, name='Anden underholdning', level=2, parent=5),
            
            Category(id=69, name='A-Kasse', level=2, parent=6),
            Category(id=70, name='Kritisk Sygdom', level=2, parent=6),
            Category(id=71, name='Livsforsikring', level=2, parent=6),
            Category(id=72, name='Lønforsikring', level=2, parent=6),
            Category(id=73, name='Rejseforsikring', level=2, parent=6),
            Category(id=74, name='Sundhedsforsikring', level=2, parent=6),
            Category(id=75, name='Ulykkesforsikring', level=2, parent=6),
            Category(id=76, name='Anden forsikring', level=2, parent=6),

            Category(id=77, name='Forbrugslån', level=2, parent=7),
            Category(id=78, name='Private Lån', level=2, parent=7),
            Category(id=79, name='Renter', level=2, parent=7),
            Category(id=80, name='Studielån', level=2, parent=7),
            Category(id=81, name='Andet gæld', level=2, parent=7),
            
            Category(id=82, name='Kapitalpension', level=2, parent=8),
            Category(id=83, name='Livrente', level=2, parent=8),
            Category(id=84, name='Ratepension', level=2, parent=8),
            Category(id=85, name='Værdipapirkøb', level=2, parent=8),
            Category(id=86, name='Andet opsparing', level=2, parent=8),

            Category(id=87, name='Bøder', level=2, parent=9),
            Category(id=88, name='Elartikler/Hvidevarer', level=2, parent=9),
            Category(id=89, name='Elektronik', level=2, parent=9),
            Category(id=90, name='Fagforening', level=2, parent=9),
            Category(id=91, name='Internet', level=2, parent=9),
            Category(id=92, name='Kabeltv', level=2, parent=9),
            Category(id=93, name='Kontanthævninger', level=2, parent=9),
            Category(id=94, name='Mobiltelefon', level=2, parent=9),
            Category(id=95, name='Møbler', level=2, parent=9),
            Category(id=96, name='Overførsler', level=2, parent=9),
            Category(id=97, name='Skat', level=2, parent=9),
            Category(id=98, name='Udlæg', level=2, parent=9),
            Category(id=99, name='Andet', level=2, parent=9),
            
            Category(id=100, name='3D Print', level=2, parent=10),
            Category(id=101, name='Projekter', level=2, parent=10),
            Category(id=102, name='Stickers', level=2, parent=10),
            Category(id=103, name='Stationary', level=2, parent=10),
            Category(id=104, name='Anden hobby', level=2, parent=10),

            Category(id=105, name='Budget', level=2, parent=11),
            Category(id=106, name='Anden overførsel', level=2, parent=11),
            Category(id=107, name='Indkomst', level=1),
            Category(id=108, name='Privat udlån', level=2, parent=7),
            Category(id=109, name='Løn', level=2, parent=107),
            Category(id=110, name='Overskydende Skat', level=2, parent=107),
            Category(id=111, name='Danmark', level=2, parent=107),
            Category(id=112, name='Backup/Antivirus', level=2, parent=9),
            Category(id=113, name='Computerspil', level=2, parent=10),
            Category(id=114, name='Brætspil', level=2, parent=10),
            Category(id=115, name='Humblebundle', level=2, parent=10),
            Category(id=116, name='Lagerrum', level=2, parent=2),
        ]
        db.session.add_all(categories)
        db.session.execute("ALTER SEQUENCE categories_id_seq RESTART WITH 117")
        db.session.commit()

        

        print("Initial rows inserted successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding the database: {e}")


def downgrade():

    try:
        num_rows_deleted = db.session.query(Category).delete()
        db.session.execute("ALTER SEQUENCE categories_id_seq RESTART WITH 1")
        db.session.commit()
    except:
        db.session.rollback()
