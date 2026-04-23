from app import app
import json

def test_home():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200

def test_add_training():
    tester = app.test_client()
    response = tester.post(
        '/add_training',
        data=json.dumps({
            "title": "Python Basics",
            "duration": 5
        }),
        content_type='application/json'
    )
    assert response.status_code == 200