from unittest.mock import patch, AsyncMock

import pytest


@pytest.mark.asyncio
async def test_search_jobs_with_external_source(client):
    mock_response = {
        "Argentina": [["Py Dev", 50000, "<skills><skill>Python</skill></skills>"]]
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.json = AsyncMock(return_value=mock_response)
        mock_get.return_value.status_code = 200

        response = await client.get("/api/v1/jobs", params={"country": "Argentina"})
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["title"] == "Py Dev"
        assert data[0]["source"] == "external"