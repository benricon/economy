from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import SubTransaction
from models import db, init_db, Transaction, Category
import csv
from io import StringIO
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy.orm import aliased

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
migrate = Migrate(app, db)
# Initialize database and migrations

@app.route("/")
def home():
    # Redirect to the home route
    return redirect('/transactions')

def get_id(name):
    id = (
        Category.query
        .with_entities(Category.id)
        .filter_by(name=name, level=1)
        .scalar()
    )
    return id


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


@app.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    """View to display and manage categories."""
    if request.method == 'POST':
        # Handle form submission for adding or editing a category
        category_id = request.form.get('id')  # For editing existing categories
        name = request.form.get('name')
        level = int(request.form.get('level'))
        parent_id = request.form.get('parent')  # Parent category, optional
        
        if not name or not level:
            flash("Name and Level are required!", "error")
            return redirect(url_for('manage_categories'))
        
        if category_id:  # Update an existing category
            category = Category.query.get(category_id)
            if category:
                category.name = name
                category.level = level
                category.parent = parent_id if parent_id else None
                db.session.commit()
                flash("Category updated successfully!", "success")
            else:
                flash("Category not found!", "error")
        else:  # Add a new category
            new_category = Category(
                name=name,
                level=level,
                parent=parent_id if parent_id else None
            )
            db.session.add(new_category)
            db.session.commit()
            flash("Category added successfully!", "success")
        
        return redirect(url_for('manage_categories'))
    
    # Fetch categories grouped by levels for display
    categories_level_1 = Category.query.filter_by(level=1).all()
    categories_level_2 = Category.query.filter_by(level=2).all()
    categories_level_3 = Category.query.filter_by(level=3).all()

    return render_template(
        'manage_categories.html',
        level_1_categories=categories_level_1,
        level_2_categories=categories_level_2,
        level_3_categories=categories_level_3
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


@app.route('/sub_transactions/<int:transaction_id>', methods=['GET', 'POST'])
def divided_trasaction(transaction_id):

    if "create" in request.form:
        transaction = Transaction.query.filter(Transaction.id == transaction_id).one()
        print(request.form.get("category_1"))
        new_entry = SubTransaction(
            date = transaction.date,
            account = transaction.account,
            description = "ID " + str(transaction_id) + ": " + request.form.get("description"),
            amount = request.form.get("amount", 0),
            category_level_1 = request.form.get("category_1") if len(request.form.get("category_1")) > 0 else None,
            category_level_2 = request.form.get("category_2") if len(request.form.get("category_2")) > 0 else None,
            category_level_3 = request.form.get("category_3") if len(request.form.get("category_3")) > 0 else None,
            parent_transaction = transaction
        )
        transaction.category_level_1 = Category.query.filter_by(level=1, name="Delt Betaling").one().id
        transaction.category_level_2 = None
        transaction.category_level_3 = None
        try: 
            db.session.add(new_entry)
            db.session.commit()
        except Exception as e:
            print("Error while adding new subcategory " + e)
        
        return redirect('/sub_transactions/' + str(transaction_id))
    

    if "delete" in request.form:
        transaction = Transaction.query.filter(Transaction.id == transaction_id).one()
        try:
            SubTransaction.query.filter_by(id=request.form.get("id")).delete()
            db.session.commit()
        except Exception as e:
            print("Error while deleting subcategory " + e)
        return redirect('/sub_transactions/' + str(transaction_id))



    category1 = aliased(Category)
    category2 = aliased(Category)
    category3 = aliased(Category)
    record = (
        db.session.query(
            Transaction,
            category1.name.label('category_level_1_name'),
            category2.name.label('category_level_2_name'),
            category3.name.label('category_level_3_name')  # Add the resolved name
        )
        .select_from(Transaction)
        .outerjoin(category1, Transaction.category_level_1 == category1.id)
        .outerjoin(category2, Transaction.category_level_2 == category2.id)
        .outerjoin(category3, Transaction.category_level_3 == category3.id)
        .filter(Transaction.id == transaction_id)
        .one()
    )
            
    subtransactions = record.Transaction.sub_transactions
    categories_level_1 = Category.query.filter_by(level=1).all()
    categories_level_2 = Category.query.filter_by(level=2).all()
    categories_level_3 = Category.query.filter_by(level=3).all()
    sum = 0
    for subtrans in subtransactions:
        sum += subtrans.amount

    remaining = record.Transaction.amount - sum
    return render_template(
        "sub_transactions.html",
        transaction=record,
        sub_transactions=subtransactions,
        remaining=remaining,
        category1s=categories_level_1 if len(categories_level_1) > 0 else [],
        category2s=categories_level_2 if len(categories_level_2) > 0 else [],
        category3s=categories_level_3 if len(categories_level_3) > 0 else [],
    )
    

if __name__ == "__main__":
    app.run(debug=True)
