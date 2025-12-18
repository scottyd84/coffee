#!/usr/bin/env python3
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, '/home/scott/py/coffee')

from main import app, db, Cafe

def check_database():
    with app.app_context():
        # Check if table exists
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Available tables: {tables}")
        
        if 'cafes' in tables:
            # Count cafes
            cafes = db.session.execute(db.select(Cafe)).scalars().all()
            print(f"Number of cafes in database: {len(cafes)}")
            
            if cafes:
                print("Cafes found:")
                for cafe in cafes:
                    print(f"  - {cafe.name} at {cafe.location}")
            else:
                print("No cafes found in the database!")
        else:
            print("Cafes table does not exist!")

if __name__ == "__main__":
    check_database()