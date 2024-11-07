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

# Verify That Object Details Contain Expected Fields
def test_object_details_fields():
    object_id = 'SK-C-5'  # Example object ID; replace with an actual ID from the Rijksmuseum
    url = f"https://www.rijksmuseum.nl/api/en/collection/{object_id}?key=0fiuZFh4"
    response = requests.get(url)
    assert response.status_code == 200, "Failed to retrieve object details"
    
    data = response.json().get('artObject', {})
    # Verify key fields
    expected_fields = ['id', 'title', 'webImage', 'principalOrFirstMaker', 'description']
    for field in expected_fields:
        assert field in data, f"{field} is missing from object details"

# Validate Response Time
def test_response_time():
    url = "https://www.rijksmuseum.nl/api/en/collection?key=0fiuZFh4"
    response = requests.get(url)
    assert response.elapsed.total_seconds() < 2, "API response time is too slow"

# Test Pagination Works Correctly
def test_pagination():
    url_page_1 = "https://www.rijksmuseum.nl/api/en/collection?key=0fiuZFh4&p=1&ps=10"
    url_page_2 = "https://www.rijksmuseum.nl/api/en/collection?key=0fiuZFh4&p=2&ps=10"
    
    response_page_1 = requests.get(url_page_1)
    response_page_2 = requests.get(url_page_2)
    
    assert response_page_1.status_code == 200, "Failed to retrieve page 1 of collection"
    assert response_page_2.status_code == 200, "Failed to retrieve page 2 of collection"
    
    data_page_1 = response_page_1.json().get('artObjects', [])
    data_page_2 = response_page_2.json().get('artObjects', [])
    
    assert data_page_1 != data_page_2, "Pagination is not working correctly; page 1 and page 2 contain the same objects"

# Check That Search Functionality Returns Relevant Results
def test_search_functionality():
    search_term = "Rembrandt"
    url = f"https://www.rijksmuseum.nl/api/en/collection?key=0fiuZFh4&q={search_term}"
    response = requests.get(url)
    assert response.status_code == 200, "Failed to retrieve search results"
    
    data = response.json().get('artObjects', [])
    assert len(data) > 0, "No results found for search term"
    
    # Check if the search term is present in any of the returned object's titles
    assert any(search_term.lower() in obj['title'].lower() for obj in data), "Search term not found in any titles"

# Verify That the API Returns the Correct Language
def test_language_support():
    url = "https://www.rijksmuseum.nl/api/nl/collection?key=0fiuZFh4"
    response = requests.get(url)
    assert response.status_code == 200, "Failed to retrieve collection in Dutch"
    
    data = response.json().get('artObjects', [])
    # Check if the title or description is in Dutch (can vary by object)
    assert any('de' in obj.get('title', '').lower() or 'het' in obj.get('title', '').lower() for obj in data), "Response does not seem to be in Dutch"

