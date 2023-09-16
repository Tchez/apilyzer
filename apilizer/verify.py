import httpx


async def check_swagger(uri: str) -> dict:
    """
    Check if the given base URI of an API has Swagger or OpenAPI documentation available at the default '/openapi.json' or '/swagger.json' endpoints.

    Parameters:
        uri (str): The base URI of the API.

    Returns:
        A dictionary containing the 'status' key with values 'success' or 'failure', and a 'message' key with detailed information on the status or errors encountered.

    Raises:
        httpx.RequestError: If there was an error making the request (note: this is handled within the function and reported in the return dict).

    Examples:
        >>> import asyncio
        >>> asyncio.run(check_swagger('http://127.0.0.1:8000')) # doctest: +SKIP
        {'status': 'success', 'message': 'Swagger/OpenAPI documentation found at /openapi.json.'}

        >>> import asyncio
        >>> asyncio.run(check_swagger('http://127.0.0.1:8000')) # doctest: +SKIP
        {'status': 'failure', 'message': 'Could not find Swagger/OpenAPI documentation.'}
    """
    async with httpx.AsyncClient() as client:
        errors = []
        for endpoint in ('openapi.json', 'swagger.json'):
            try:
                response = await client.get(f'{uri}/{endpoint}')
                if response.status_code == 200:
                    return {
                        'status': 'success',
                        'message': f'Swagger/OpenAPI documentation found at /{endpoint}.',
                    }
                else:
                    errors.append(
                        f'{response.status_code} Client Error: {response.reason_phrase} for url: {response.url}'
                    )
            except httpx.RequestError as exc:
                errors.append(str(exc))
                continue

        return {
            'status': 'failure',
            'message': f'Could not find Swagger/OpenAPI documentation. Errors encountered: {errors}',
        }
