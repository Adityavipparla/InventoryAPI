
from app import create_app, db
from app.models import Category, Product

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created (if they didn't already exist).")

if __name__ == '__main__':
    app.run(debug=True)
