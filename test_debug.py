#!/usr/bin/env python3
from main import app, db, Cafe

# Test script to debug the cafes route
with app.app_context():
    print("Testing database connection...")
    
    # Check if we can query the database
    try:
        cafes_count = db.session.execute(db.select(Cafe)).scalars().all()
        print(f"Found {len(cafes_count)} cafes in database")
        
        for cafe in cafes_count:
            print(f"- {cafe.name}: {cafe.location}")
            
    except Exception as e:
        print(f"Error querying database: {e}")
        
    print("\nTesting route manually...")
    with app.test_client() as client:
        response = client.get('/cafes')
        print(f"Response status: {response.status_code}")
        print(f"Response length: {len(response.data)} bytes")
        if response.status_code == 200:
            print("Route is working correctly!")
            # Check if 'cafes' template variable is populated
            if b'All Cafes' in response.data:
                print("Template is rendering!")
                if b'<tr>' in response.data and b'</tr>' in response.data:
                    print("Table rows are being generated!")
                else:
                    print("No table rows found - cafes variable might be empty")
            else:
                print("Template is not rendering properly")
        else:
            print(f"Route failed: {response.data}")