#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/scott/py/coffee')

from main import app, db, Cafe

def populate_database():
    """Add sample cafes to the database"""
    with app.app_context():
        # Check if database is already populated
        existing_cafes = db.session.execute(db.select(Cafe)).scalars().all()
        if existing_cafes:
            print(f"Database already has {len(existing_cafes)} cafes. Skipping population.")
            return

        # Sample cafe data
        sample_cafes = [
            {
                'name': 'The Coffee Bean',
                'location': 'Downtown',
                'map_url': 'https://maps.google.com/?q=coffee+bean+downtown',
                'img_url': 'https://via.placeholder.com/300x200?text=Coffee+Bean',
                'has_sockets': True,
                'has_toilet': True,
                'has_wifi': True,
                'can_take_calls': False,
                'seats': '20-30',
                'coffee_price': '$3.50'
            },
            {
                'name': 'Brew & Bytes',
                'location': 'Tech District',
                'map_url': 'https://maps.google.com/?q=brew+bytes+tech+district',
                'img_url': 'https://via.placeholder.com/300x200?text=Brew+Bytes',
                'has_sockets': True,
                'has_toilet': True,
                'has_wifi': True,
                'can_take_calls': True,
                'seats': '15-20',
                'coffee_price': '$4.00'
            },
            {
                'name': 'Central Perk',
                'location': 'City Center',
                'map_url': 'https://maps.google.com/?q=central+perk+city+center',
                'img_url': 'https://via.placeholder.com/300x200?text=Central+Perk',
                'has_sockets': False,
                'has_toilet': True,
                'has_wifi': True,
                'can_take_calls': False,
                'seats': '10-15',
                'coffee_price': '$2.75'
            },
            {
                'name': 'Code Cafe',
                'location': 'University Area',
                'map_url': 'https://maps.google.com/?q=code+cafe+university',
                'img_url': 'https://via.placeholder.com/300x200?text=Code+Cafe',
                'has_sockets': True,
                'has_toilet': False,
                'has_wifi': True,
                'can_take_calls': True,
                'seats': '25-30',
                'coffee_price': '$3.25'
            }
        ]

        # Add cafes to database
        for cafe_data in sample_cafes:
            cafe = Cafe(
                name=cafe_data['name'],
                location=cafe_data['location'],
                map_url=cafe_data['map_url'],
                img_url=cafe_data['img_url'],
                has_sockets=cafe_data['has_sockets'],
                has_toilet=cafe_data['has_toilet'],
                has_wifi=cafe_data['has_wifi'],
                can_take_calls=cafe_data['can_take_calls'],
                seats=cafe_data['seats'],
                coffee_price=cafe_data['coffee_price']
            )
            db.session.add(cafe)

        # Commit all changes
        db.session.commit()
        print(f"Successfully added {len(sample_cafes)} sample cafes to the database!")

        # Verify the data was added
        cafes = db.session.execute(db.select(Cafe)).scalars().all()
        print(f"Total cafes in database: {len(cafes)}")
        for cafe in cafes:
            print(f"  - {cafe.name} at {cafe.location}")

if __name__ == "__main__":
    populate_database()