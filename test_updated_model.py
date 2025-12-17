#!/usr/bin/env python3
from main import app, db, Cafe

# Test script to verify the updated model works
with app.app_context():
    print("Testing database connection with updated model...")
    
    try:
        # Test querying the database with new model
        cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
        print(f"Found {len(cafes)} cafes in database")
        
        for cafe in cafes[:3]:  # Show first 3 cafes
            print(f"- {cafe.name}")
            print(f"  Location: {cafe.location}")
            print(f"  Map URL: {cafe.map_url}")
            print(f"  Has WiFi: {cafe.has_wifi}")
            print(f"  Has Sockets: {cafe.has_sockets}")
            print()
            
    except Exception as e:
        print(f"Error querying database: {e}")
        
    print("\nTesting /cafes route...")
    with app.test_client() as client:
        response = client.get('/cafes')
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print("✅ /cafes route is working!")
            if b'<tr>' in response.data and b'</tr>' in response.data:
                print("✅ Table rows are being generated!")
            else:
                print("❌ No table rows found")
        else:
            print(f"❌ Route failed: {response.data}")
            
    print("\nTesting /random route...")
    with app.test_client() as client:
        response = client.get('/random')
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print("✅ /random route is working!")
        else:
            print(f"❌ Random route failed: {response.data}")