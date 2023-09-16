import httpx


async def check_swagger(uri: str) -> bool:
    """
    Check if the given base URI of the API has Swagger documentation.

    Parameters:
        uri (str): The base URI of the API.

    Returns:
        A dictionary containing the 'status' key with values 'success' or 'failure', and a 'message' key with detailed information.

    Examples:
        >>> import asyncio
        >>> asyncio.run(check_swagger('http://127.0.0.1:8000')) # doctest: +SKIP
        {'status': 'success', 'message': 'Swagger documentation found.'}

        >>> import asyncio
        >>> asyncio.run(check_swagger('http://127.0.0.1:8000')) # doctest: +SKIP
        {'status': 'failure', 'message': 'Could not reach the API: ...'}
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{uri}/swagger.json')
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'message': 'Swagger documentation found.',
                }
            else:
                return {
                    'status': 'failure',
                    'message': f'Unexpected status code: {response.status_code}',
                }
        except httpx.RequestError as exc:
            return {
                'status': 'failure',
                'message': f'Could not reach the API: {exc}',
            }
