import pytest
from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Smoke tests — every page loads without error
# ---------------------------------------------------------------------------

class TestSmoke:
    def test_landing_page_loads(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_add_page_loads(self, client):
        response = client.get("/add")
        assert response.status_code == 200

    def test_multiply_page_loads(self, client):
        response = client.get("/multiply")
        assert response.status_code == 200

    def test_result_page_loads(self, client):
        response = client.get("/result?action=Addition&a=1&b=2&result=3")
        assert response.status_code == 200

    def test_landing_page_contains_add_link(self, client):
        response = client.get("/")
        assert b"/add" in response.data

    def test_landing_page_contains_multiply_link(self, client):
        response = client.get("/")
        assert b"/multiply" in response.data


# ---------------------------------------------------------------------------
# Addition operation tests
# ---------------------------------------------------------------------------

class TestAddition:
    def test_add_redirects_on_post(self, client):
        response = client.post("/add", data={"a": "3", "b": "4"})
        assert response.status_code == 302

    def test_add_redirect_points_to_result(self, client):
        response = client.post("/add", data={"a": "3", "b": "4"})
        assert "/result" in response.headers["Location"]

    def test_add_result_value(self, client):
        response = client.post("/add", data={"a": "3", "b": "4"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"7" in response.data

    def test_add_result_shows_action(self, client):
        response = client.post("/add", data={"a": "3", "b": "4"}, follow_redirects=True)
        assert b"Addition" in response.data

    def test_add_result_shows_operands(self, client):
        response = client.post("/add", data={"a": "3", "b": "4"}, follow_redirects=True)
        assert b"3" in response.data
        assert b"4" in response.data

    def test_add_with_floats(self, client):
        response = client.post("/add", data={"a": "1.5", "b": "2.5"}, follow_redirects=True)
        assert b"4" in response.data

    def test_add_with_negative_numbers(self, client):
        response = client.post("/add", data={"a": "-5", "b": "3"}, follow_redirects=True)
        assert b"-2" in response.data

    def test_add_with_zeros(self, client):
        response = client.post("/add", data={"a": "0", "b": "0"}, follow_redirects=True)
        assert b"0" in response.data

    def test_add_large_numbers(self, client):
        response = client.post("/add", data={"a": "1000000", "b": "2000000"}, follow_redirects=True)
        assert b"3000000" in response.data


# ---------------------------------------------------------------------------
# Multiplication operation tests
# ---------------------------------------------------------------------------

class TestMultiplication:
    def test_multiply_redirects_on_post(self, client):
        response = client.post("/multiply", data={"a": "6", "b": "7"})
        assert response.status_code == 302

    def test_multiply_redirect_points_to_result(self, client):
        response = client.post("/multiply", data={"a": "6", "b": "7"})
        assert "/result" in response.headers["Location"]

    def test_multiply_result_value(self, client):
        response = client.post("/multiply", data={"a": "6", "b": "7"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"42" in response.data

    def test_multiply_result_shows_action(self, client):
        response = client.post("/multiply", data={"a": "6", "b": "7"}, follow_redirects=True)
        assert b"Multiplication" in response.data

    def test_multiply_result_shows_operands(self, client):
        response = client.post("/multiply", data={"a": "6", "b": "7"}, follow_redirects=True)
        assert b"6" in response.data
        assert b"7" in response.data

    def test_multiply_with_floats(self, client):
        response = client.post("/multiply", data={"a": "2.5", "b": "4"}, follow_redirects=True)
        assert b"10" in response.data

    def test_multiply_with_zero(self, client):
        response = client.post("/multiply", data={"a": "99", "b": "0"}, follow_redirects=True)
        assert b"0" in response.data

    def test_multiply_with_negative_numbers(self, client):
        response = client.post("/multiply", data={"a": "-3", "b": "4"}, follow_redirects=True)
        assert b"-12" in response.data

    def test_multiply_large_numbers(self, client):
        response = client.post("/multiply", data={"a": "1000", "b": "1000"}, follow_redirects=True)
        assert b"1000000" in response.data


# ---------------------------------------------------------------------------
# Result page tests
# ---------------------------------------------------------------------------

class TestResultPage:
    def test_result_shows_addition_action(self, client):
        response = client.get("/result?action=Addition&a=5&b=3&result=8")
        assert b"Addition" in response.data

    def test_result_shows_multiplication_action(self, client):
        response = client.get("/result?action=Multiplication&a=5&b=3&result=15")
        assert b"Multiplication" in response.data

    def test_result_shows_all_values(self, client):
        response = client.get("/result?action=Addition&a=10&b=20&result=30")
        assert b"10" in response.data
        assert b"20" in response.data
        assert b"30" in response.data

    def test_result_page_has_back_button(self, client):
        response = client.get("/result?action=Addition&a=1&b=1&result=2")
        assert b"/" in response.data  # home link exists in the page
