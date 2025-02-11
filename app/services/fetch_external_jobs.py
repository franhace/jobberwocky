import httpx

# TODO: make url customizable to adapt to multiple external sources


async def fetch_external_jobs(params: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://external-source:8080/jobs",
                params= params,
                timeout= 3.0
            )
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print("External API error: ".format(e))
        return {}