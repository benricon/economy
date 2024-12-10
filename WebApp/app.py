from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import SubTransaction
from models import db, init_db, Transaction, Category
import csv
from io import StringIO
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
migrate = Migrate(app, db)
# Initialize database and migrations

@app.route("/")
def home():
    # Redirect to the home route
    return redirect('/transactions')



@app.cli.command('seed1')
def seed1():
    """Insert initial rows into the database."""
    try:
        # Add level 1  and 3 categories
        categories = [
            Category(name='Faste udgifter', level=1),
            Category(name='Underholdning', level=1),
            Category(name='Hobby', level=1),
            Category(name='Bjarne', level=3),
            Category(name='Rebecca', level=3),
            Category(name='Fælles', level=3)
        ]
        db.session.add_all(categories)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding the database: {e}")

@app.cli.command('seed2')
def seed2():
    """Insert initial rows into the database."""
    try:

        # Add level 2 categories
        FasteUdgifter_id = db.session.query(Category.id).filter(Category.name=="Faste udgifter").one()[0]
        Underholdning_id = db.session.query(Category.id).filter(Category.name=="Underholdning").one()[0]
        Hobby_id = db.session.query(Category.id).filter(Category.name=="Hobby").one()[0]
        print(FasteUdgifter_id, Underholdning_id, Hobby_id)
        subcategories = [
            Category(name='Husleje', level=2, parent=FasteUdgifter_id),
            Category(name='El', level=2, parent=FasteUdgifter_id),
            Category(name='Varme', level=2, parent=FasteUdgifter_id),
            Category(name='Vand', level=2, parent=FasteUdgifter_id),
            Category(name='Internet', level=2, parent=FasteUdgifter_id),
            Category(name='Telefon', level=2, parent=FasteUdgifter_id),
            Category(name='Forsikring', level=2, parent=FasteUdgifter_id),
            Category(name='Lagerrum', level=2, parent=FasteUdgifter_id),
            Category(name='A-Kasse', level=2, parent=FasteUdgifter_id),
            Category(name='Fagforening', level=2, parent=FasteUdgifter_id),

            Category(name='Streaming', level=2, parent=Underholdning_id),
            Category(name='Restaurant', level=2, parent=Underholdning_id),
            Category(name='Biograf', level=2, parent=Underholdning_id),

            Category(name='3D Print', level=2, parent=Hobby_id),
            Category(name='Stickers', level=2, parent=Hobby_id),
            Category(name='Stationary', level=2, parent=Hobby_id),
            Category(name='Electronik', level=2, parent=Hobby_id)
        ]
        db.session.add_all(subcategories)
        db.session.commit()

        

        print("Initial rows inserted successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding the database: {e}")


@app.route('/api/categories/<int:category_id>/subcategories', methods=['GET'])
def get_subcategories(category_id):
    subcategories = Category.query.filter_by(parent=category_id).all()  # Adjust if necessary
    return jsonify([{'id': sub.id, 'name': sub.name} for sub in subcategories])




@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    query = Transaction.query
    if "update" in request.form:
        record = query.filter(Transaction.id == request.form.get("id")).one()
        if len(request.form.get("category_1")) > 0:
            record.category_level_1 = request.form.get("category_1")
        else:
            record.category_level_1 = None
        if len(request.form.get("category_2")) > 0:
            record.category_level_2 = request.form.get("category_2")
        else:
            record.category_level_2 = None
        if len(request.form.get("category_3")) > 0:
            record.category_level_3 = request.form.get("category_3")
        else:
            record.category_level_3 = None
        record.is_categorized = True
        db.session.commit()

    """View for filtering and displaying transactions."""
    # Fetch all accounts for the dropdown
    accounts = db.session.query(Transaction.account).distinct().all()
    account_names = [account[0] for account in accounts]
    categories_level_1 = Category.query.filter_by(level=1).all()
    categories_level_2 = Category.query.filter_by(level=2).all()
    categories_level_3 = Category.query.filter_by(level=3).all()
    

    # Retrieve filters from the query parameters
    selected_account = request.args.get("account")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    is_categorized = request.args.get("is_categorized")


    # Build the query
    if selected_account:
        query = query.filter(Transaction.account == selected_account)
    if start_date and end_date:
        query = query.filter(Transaction.date.between(start_date, end_date))
    if is_categorized =="yes":
        query = query.filter(Transaction.is_categorized == True)
    if is_categorized =="no":
        query = query.filter(Transaction.is_categorized == False)

    # Fetch filtered transactions
    transactions = query.order_by(Transaction.date.asc()).limit(50).all()



    return render_template(
        "transactions.html",
        transactions=transactions,
        accounts=account_names,
        selected_account=selected_account,
        start_date=start_date,
        end_date=end_date,
        is_categorized=is_categorized,
        category1s=categories_level_1 if len(categories_level_1) > 0 else [],
        category2s=categories_level_2 if len(categories_level_2) > 0 else [],
        category3s=categories_level_3 if len(categories_level_3) > 0 else [],
        
        
    )


@app.route("/categories", methods=["GET", "POST"])
def manage_categories():
    """View to display and add categories."""
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        level = request.form.get("level")

        if name and level:
            # Add the new category to the database
            category = Category(name=name, level=int(level))
            db.session.add(category)
            db.session.commit()
            return redirect(url_for("manage_categories"))

    # Fetch all categories grouped by levels
    level_1_categories = Category.query.filter_by(level=1).all()
    level_2_categories = Category.query.filter_by(level=2).all()
    level_3_categories = Category.query.filter_by(level=3).all()

    return render_template(
        "categories.html",
        level_1_categories=level_1_categories,
        level_2_categories=level_2_categories,
        level_3_categories=level_3_categories,
    )
       

@app.route('/upload-csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        # Check if the post request has the file part
        file = request.files.get('file')
        
        if not file:
            flash('No file part', 'error')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        
        if filename.endswith('.csv'):
            # Read the file content
            file_content = file.stream.read().decode('utf-8')
            csv_reader = csv.DictReader(StringIO(file_content), delimiter=';')
            i = 0 
            for row in csv_reader:
                try:
                    # Extract the data from CSV
                    date_str = row['Dato']
                    amount = float(row['Beløb'].replace(',', ''))  # Handle comma decimal if needed
                    text = row['Tekst']

                    # Parse date
                    date = datetime.strptime(date_str, '%d.%m.%Y')  # Adjust format if needed
                    # Insert into the database
                    transaction = Transaction(
                        date=date,
                        amount=amount,
                        description=text,
                        account=filename.split('.')[0]
                    )
                    db.session.add(transaction)
                    i+=1
                except Exception as e:
                    # General error for file reading or database issues
                    db.session.rollback()  # Rollback in case of failure
                    flash(f"An error occurred while processing the file: {str(e)}", 'error')
                    
            
            try:
                db.session.commit()
            except:
                flash(f'Error during transactions commit')
            flash(f'Successfully uploaded {i} transactions', 'success')
        else:
            flash('Please upload a CSV file', 'error')
        return redirect(url_for('upload_csv'))

    return render_template('upload_csv.html')

if __name__ == "__main__":
    app.run(debug=True)
