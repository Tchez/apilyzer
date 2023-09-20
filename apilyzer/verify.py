import json

import httpx
from bs4 import BeautifulSoup


async def is_rest_api(uri: str) -> bool:
    """Verifies if the given URI belongs to a REST API.

    This function sends a GET request to the URI and checks the response headers and content to determine whether it is a REST API.

    Parameters:
        uri (str): The URI to be checked.

    Returns:
        bool: True if the API is REST, False otherwise.

    Raises:
        httpx.HTTPError: If there was an error making the request (handled within the function and reported to the console).

    Examples:
        >>> import asyncio
        >>> asyncio.run(is_rest_api('http://127.0.0.1:8000')) # doctest: +SKIP
        True
    """
    try:
        async with httpx.AsyncClient(
            follow_redirects=True, headers={'User-Agent': 'API Checker'}
        ) as client:
            url = uri.rstrip('/') + '/'
            response = await client.get(url)

        if (
            'application/json' in response.headers.get('Content-Type', '')
            or 'Access-Control-Allow-Origin' in response.headers
        ):
            return True

        response_text = response.text
        try:
            parsed_json = json.loads(response_text)
            if 'swagger' in parsed_json or 'openapi' in parsed_json:
                return True
        except json.JSONDecodeError:
            pass

        soup = BeautifulSoup(response_text, 'html.parser')
        if (
            'api' in response_text.lower()
            or 'documentation' in response_text.lower()
            or soup.find(name='paths')
        ):
            return True

        common_endpoints = ['/api', '/v1']
        for endpoint in common_endpoints:
            response = await client.get(url + endpoint)
            if response.status_code in {200, 201}:
                return True

    except httpx.HTTPError as e:
        print(f'An HTTP error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

    return False


async def check_swagger_rest(uri: str) -> dict:
    """Check if the given base URI of an API has REST API documentation available at various common endpoints.

    Parameters:
        uri (str): The base URI of the API.

    Returns:
        dict: A dictionary containing the 'status', 'message', and 'response' keys detailing the outcome of the check.

    Examples:
        >>> import asyncio
        >>> asyncio.run(check_swagger_rest('http://127.0.0.1:8000')) # doctest: +SKIP
        {'status': 'success', 'message': 'Potential REST API documentation found at http://127.0.0.1:8000/', 'response': '{...}'}
    """
    is_rest = await is_rest_api(uri)

    if not is_rest:
        return {
            'status': 'error',
            'message': f'{uri} does not appear to be a REST API.',
            'response': [],
        }

    async with httpx.AsyncClient(
        follow_redirects=True, headers={'User-Agent': 'API Checker'}
    ) as client:
        _errors = set()
        endpoints = [
            'openapi.json',
            'swagger.json',
            'docs',
            'api-docs',
            'swagger',
            'swagger-ui.html',
            'redoc',
            'api/docs',
            'swagger/ui',
            '',
        ]
        url = uri.rstrip('/')

        for endpoint in endpoints:
            try:
                response = await client.get(f'{url}/{endpoint}', timeout=10)
                if response.status_code // 100 == 2:
                    if 'application/json' in response.headers.get(
                        'Content-Type', ''
                    ):
                        _response = response.json()
                    else:
                        _response = response.text

                    if any(
                        term in str(_response).lower()
                        for term in [
                            'swagger',
                            'openapi',
                            'api',
                            'endpoints',
                            'documentation',
                        ]
                    ):
                        return {
                            'status': 'success',
                            'message': f'Potential REST API documentation found at {url}/{endpoint}',
                            'response': _response,
                        }
                else:
                    _errors.add(
                        f'{response.status_code} Client Error: {response.reason_phrase} for url: {response.url}'
                    )
                    continue
            except httpx.RequestError as exc:
                _errors.add(
                    f'An error occurred while requesting {url}/{endpoint}: {exc}'
                )
                continue

        return {
            'status': 'error',
            'message': 'No REST API documentation found.',
            'response': list(_errors),
        }
