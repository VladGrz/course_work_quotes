import requests, unittest

API_BASE_URL = "http://api_server:8000"

class TestApiMethods(unittest.TestCase):
    def test_get_quotes(self):
        response = requests.get(f"{API_BASE_URL}/quotes")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_add_quote(self):
        new_quote = {
            "text": "Life is what happens when you're busy making other plans.",
            "author": "John Lennon"
        }
        response = requests.post(f"{API_BASE_URL}/quotes", json=new_quote)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("text"), new_quote["text"])
        self.assertEqual(response.json().get("author"), new_quote["author"])

if __name__ == "__main__":
    unittest.main()
