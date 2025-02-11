from unittest.mock import patch

def test_external_job_aggregation(client):
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "Argentina": [["Python Dev", 50000, "<skills><skill>Python</skill></skills>"]]
        }
        response = client.get("/jobs/?country=Argentina")
        assert response.json() == {"Argentina": [["Python Dev", 50000, "<skills><skill>Python</skill></skills>"]]}