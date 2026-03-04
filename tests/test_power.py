import pytest
from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Smoke tests
# ---------------------------------------------------------------------------

class TestPowerSmoke:
    def test_power_page_loads(self, client):
        response = client.get("/power")
        assert response.status_code == 200

    def test_power_page_returns_html(self, client):
        response = client.get("/power")
        assert b"text/html" in response.content_type.encode()

    def test_landing_page_contains_power_link(self, client):
        response = client.get("/")
        assert b"/power" in response.data

    def test_power_page_contains_form(self, client):
        response = client.get("/power")
        assert b"<form" in response.data

    def test_power_page_contains_input(self, client):
        response = client.get("/power")
        assert b'name="a"' in response.data


# ---------------------------------------------------------------------------
# Operation tests
# ---------------------------------------------------------------------------

class TestPowerOperation:
    def test_post_redirects(self, client):
        response = client.post("/power", data={"a": "5"})
        assert response.status_code == 302

    def test_post_redirects_to_result(self, client):
        response = client.post("/power", data={"a": "5"})
        assert "/result" in response.headers["Location"]

    def test_integer_squared(self, client):
        response = client.post("/power", data={"a": "5"}, follow_redirects=True)
        assert b"25" in response.data

    def test_zero_squared(self, client):
        response = client.post("/power", data={"a": "0"}, follow_redirects=True)
        assert b"0" in response.data

    def test_one_squared(self, client):
        response = client.post("/power", data={"a": "1"}, follow_redirects=True)
        assert b"1" in response.data

    def test_negative_number_squared(self, client):
        # negative squared is always positive
        response = client.post("/power", data={"a": "-4"}, follow_redirects=True)
        assert b"16" in response.data

    def test_float_squared(self, client):
        response = client.post("/power", data={"a": "2.5"}, follow_redirects=True)
        assert b"6.25" in response.data

    def test_large_number_squared(self, client):
        response = client.post("/power", data={"a": "100"}, follow_redirects=True)
        assert b"10000" in response.data


# ---------------------------------------------------------------------------
# Result page tests
# ---------------------------------------------------------------------------

class TestPowerResult:
    def test_result_page_loads(self, client):
        response = client.get("/result?action=Power&a=5&result=25")
        assert response.status_code == 200

    def test_result_shows_power_action(self, client):
        response = client.get("/result?action=Power&a=5&result=25")
        assert b"Power" in response.data

    def test_result_shows_input_number(self, client):
        response = client.get("/result?action=Power&a=5&result=25")
        assert b"5" in response.data

    def test_result_shows_computed_value(self, client):
        response = client.get("/result?action=Power&a=5&result=25")
        assert b"25" in response.data

    def test_result_has_back_button(self, client):
        response = client.get("/result?action=Power&a=5&result=25")
        assert b"Back to Home" in response.data

    def test_result_end_to_end(self, client):
        # submit the form and verify the full result page in one flow
        response = client.post("/power", data={"a": "7"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Power" in response.data
        assert b"7" in response.data
        assert b"49" in response.data
