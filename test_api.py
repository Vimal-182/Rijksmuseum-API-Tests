import requests

API_KEY = "0fiuZFh4"
BASE_URL = "https://www.rijksmuseum.nl/api/en/collection"

def test_get_collection():
    response = requests.get(f"{BASE_URL}?key={API_KEY}")
    assert response.status_code == 200
    data = response.json()
    assert "artObjects" in data, "Response does not contain 'artObjects' key."

def test_get_object_details():
    object_number = "SK-C-5"  # Example object number for "The Night Watch" by Rembrandt
    response = requests.get(f"{BASE_URL}/{object_number}?key={API_KEY}")
    assert response.status_code == 200
    data = response.json()
    assert "artObject" in data, "Response does not contain 'artObject' key."