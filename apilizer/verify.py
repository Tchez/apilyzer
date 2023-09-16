import httpx


async def check_swagger(uri: str) -> bool:
    """
    Check if the given base URI of the API has Swagger documentation.

    Parameters:
        uri (str): The base URI of the API.
        uri (str): The base URI of the API.

    Returns:
        Returns `True` if the API has Swagger documentation, and `False` otherwise.

    Examples:
        >>> import asyncio
        >>> asyncio.run(check_swagger('http://127.0.0.1:8000'))
        True
        
        >>> import asyncio
        >>> asyncio.run(check_swagger('http://127.0.0.1:8000'))
        False
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{uri}/swagger.json')
            return response.status_code == 200
        except httpx.RequestError as exc:
            print(f'Request error: {exc}')
            return False


async def check_post_201(uri: str) -> dict:
    """
    Check if the API's POST endpoints return the 201 status code.

    Parameters:
        uri (str): The base URI of the API.

    Returns:
        A dictionary mapping endpoints to their response status when a POST request is made.

    Examples:
        >>> import asyncio
        >>> asyncio.run(check_post_201('http://127.0.0.1:8000'))
        {'http://127.0.0.1:8000/endpoint1': 201, 'http://127.0.0.1:8000/endpoint2': 'Error: ...'}
        
        >>> import asyncio
        >>> asyncio.run(check_post_201('http://127.0.0.1:8000'))
        {'http://127.0.0.1:8000/endpoint1': 201, 'http://127.0.0.1:8000/endpoint2': 201}
    """
    results = {}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{uri}/swagger.json')
            spec_dict = response.json()
        except httpx.RequestError as exc:
            print(f'Request error: {exc}')
            return results

        for path, path_item in spec_dict.get('paths', {}).items():
            if 'post' in path_item:
                endpoint_url = f'{uri}{path}'
                post_data = {}

                try:
                    response = await client.post(endpoint_url, json=post_data)
                    results[endpoint_url] = response.status_code
                except httpx.RequestError as exc:
                    results[endpoint_url] = f'Error: {exc}'

    return results
