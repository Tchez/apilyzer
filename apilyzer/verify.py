import asyncio
import json

import httpx


async def _is_json_rest_api(uri: str) -> (bool, httpx.Response):
    """Verifies if the given URI belongs to a JSON REST API and returns the response.

    This function sends a GET request to the URI and checks the response headers and content to determine whether it is a REST API.
    Currently, this function recognizes only APIs that return JSON content.

    Parameters:
        uri (str): The URI to be checked.

    Returns:
        bool: True if the API is JSON REST, False otherwise.
        httpx.Response: The response of the GET request.

    Raises:
        httpx.HTTPError: If there was an error making the request (handled within the function).

    Examples:
        >>> import asyncio
        >>> asyncio.run(_is_json_rest_api('http://127.0.0.1:8000')) # doctest: +SKIP
        True, <Response [200 OK]>
    """
    if not (uri.startswith('http') or uri.startswith('https')):
        return False, None

    try:
        async with httpx.AsyncClient(
            follow_redirects=True, headers={'User-Agent': 'API Checker'}
        ) as client:
            url = uri.rstrip('/')
            response = await client.get(url, timeout=10)
    except httpx.ConnectError:
        return False, None

    if response.status_code // 100 != 2:
        return False, response

    content_type = response.headers.get('Content-Type', '')

    if 'application/json' in content_type:
        data = response.json()
        if isinstance(data, (list, dict)):
            return True, response

    allow_header = response.headers.get('Allow', '')
    if any(
        verb in allow_header
        for verb in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    ):
        return True, response

    return False, response


async def check_swagger_rest(uri: str, doc_endpoint: str = None) -> dict:
    """Check if the given base URI of an API has REST API documentation available.

    Parameters:
        uri (str): The base URI of the API.
        doc_endpoint (str, optional): The endpoint where the documentation is available. Defaults to None.

    Returns:
        dict: A dictionary containing the 'status', 'message', and 'response' keys detailing the outcome of the check.

    Examples:
        >>> import asyncio
        >>> asyncio.run(check_swagger_rest('http://127.0.0.1:8000')) # doctest: +SKIP
        {'status': 'success', 'message': 'REST API JSON documentation found at http://127.0.0.1:8000/', 'response': '{...}'}
    """
    _errors = set()
    url = uri.rstrip('/')

    api_terms = [
        'swagger',
        'openapi',
        'endpoints',
        'paths',
        'documentation',
    ]

    if doc_endpoint:
        doc_endpoint = doc_endpoint.lstrip('/')
        endpoints = [doc_endpoint]
    else:
        endpoints = [
            'openapi.json',
            'swagger.json',
            'docs',
            'api-docs',
            'swagger',
            'redoc',
            'api/docs',
            'swagger/ui',
            '',
        ]

    for endpoint in endpoints:
        full_url = f'{url}/{endpoint}'
        try:
            is_rest, response = await _is_json_rest_api(full_url)

            if not is_rest:
                _errors.add(
                    f'The URL {full_url} does not seem to be a JSON REST API'
                )
                continue

            if response.status_code // 100 != 2:
                _errors.add(
                    f'{response.status_code} Client Error: {response.reason_phrase} for url: {response.url}'
                )
                continue

            if any(term in response.text.lower() for term in api_terms):
                if 'application/json' in response.headers.get(
                    'Content-Type', ''
                ):
                    return {
                        'status': 'success',
                        'message': f'REST API JSON documentation found at {full_url}',
                        'response': response.json(),
                    }
                else:
                    message = f'Potential REST API documentation found at {full_url}, but not in JSON format'
                    if not doc_endpoint:
                        message += ' (Endpoint not specified, please provide the JSON documentation endpoint)'
                    return {
                        'status': 'warning',
                        'message': message,
                        'response': None,
                    }

        except Exception as e:
            _errors.add(f'An error occurred while requesting {full_url}: {e}')

    message = 'No REST API documentation found'

    if not doc_endpoint:
        message += ' (Endpoint not specified, and we could not identify it with the base URL alone)'

    return {
        'status': 'error',
        'message': message,
        'response': list(_errors),
    }


async def _supports_https(uri: str) -> dict:
    """Check if the given base URI of an API has support to HTTPS protocol.

    Parameters:
        uri (str): The base URI of the API.

    Returns:
        dict: A dictionary containing the 'status', 'message', and 'response' keys detailing the outcome of the check.

    Examples:
        >>> import asyncio
        >>> asyncio.run(_supports_https('http://127.0.0.1:8000')) # doctest: +SKIP
        {'status': 'success', 'message': '✅ The URI does not support HTTPS at http://127.0.0.1:8000/. ', 'response': '{...}'}
    """

    https_uri = (
        uri.replace('http://', 'https://')
        if uri.startswith('http://')
        else uri
    )

    async with httpx.AsyncClient() as client:
        _errors = set()
        try:
            response = await client.get(https_uri)
            if response.status_code // 100 == 2:
                if 'application/json' in response.headers.get(
                    'Content-Type', ''
                ):
                    _response = response.json()
                else:
                    _response = response.text
                return {
                    'status': 'success',
                    'message': f'✅ The URI supports HTTPS at {uri}',
                    'response': _response,
                }
            else:
                _errors.add(
                    f'{response.status_code} Client Error: {response.reason_phrase} for URL: {https_uri}'
                )
        except httpx.RequestError as exc:
            _errors.add(
                f'An error occurred while requesting {https_uri}: {exc}'
            )

    return {
        'status': 'error',
        'message': f'🚫 The URI does not support HTTPS at {uri}',
        'response': list(_errors),
    }


async def _verify_maturity_paths(paths: dict) -> dict:
    """Verify the maturity level of the API's paths according to Richardson's maturity model.

    Parameters:
        paths (dict): The paths of the API.

    Returns:
        dict: A dictionary containing feedback on the maturity level of the API's paths.
    """
    feedback = {}
    messages = []
    _has_only_post_method = True
    valid_methods = ['get', 'post', 'put', 'patch', 'delete']

    for path, path_info in paths.items():
        for method in path_info.keys():
            if method not in valid_methods:
                messages.append(
                    f'🚫   Error! The {path} method uses a non-conventional {method.upper()} method. '
                    f'Consider following the standard RESTful methods for better maturity'
                )

        if 'get' in path_info:
            _has_only_post_method = False

        for method, expected_status, expected_description in [
            ('post', '201', 'Created'),
            ('put', '200', 'OK'),
            ('patch', '200', 'OK'),
            ('delete', '200', 'OK'),
        ]:
            if method in path_info:
                _has_only_post_method = (
                    False if method != 'post' else _has_only_post_method
                )

                actual_status = next(
                    iter(path_info[method].get('responses', {}).keys()), None
                )
                actual_description = (
                    path_info[method]
                    .get('responses', {})
                    .get(expected_status, {})
                    .get('description', '')
                )

                if actual_status == expected_status:
                    if actual_description != expected_description:
                        messages.append(
                            f'✅   Congratulations! The {path} method returns the correct status code for {method.upper()} requests'
                        )
                        messages.append(
                            f'⚠️   Warning! Richardson\'s maturity model recommends using "{expected_description}" as the description for {method.upper()} requests'
                        )
                    else:
                        messages.append(
                            f'✅   Congratulations! The {path} method returns the correct status code and description for {method.upper()} requests. '
                            f"It aligns with Richardson's maturity model."
                        )
                else:
                    if actual_description:
                        messages.append(
                            f'🚫   Error! The {path} method returns the wrong status code for {method.upper()} requests. '
                            f'Expected: {expected_status} but got: {actual_status}. '
                            f"It is at level 0 of Richardson's maturity model."
                        )
                    else:
                        messages.append(
                            f'🚫   Error! The {path} method does not provide any response status or description for {method.upper()} requests. '
                            f"It is at level 0 of Richardson's maturity model."
                        )

    if _has_only_post_method:
        message = "🚫   Error! The API only has POST methods. It is at level 0 of Richardson's maturity model."
    else:
        message = "✅   Congratulations! The API has methods other than POST. It is at least at level 1 of Richardson's maturity model."

    messages.append(message)

    feedback['messages'] = messages
    return feedback


async def analyze_api_maturity(uri: str) -> dict:
    """Analyze the maturity level of a REST API using Richardson's maturity model.

    Parameters:
        uri (str): The base URI of the API.

    Returns:
        dict: A dictionary containing feedback on the API's maturity level according to Richardson's maturity model.
    """
    feedbacks = {}

    swagger_doc = await check_swagger_rest(uri)

    if swagger_doc['status'] == 'error':
        return swagger_doc

    response = swagger_doc['response']

    if isinstance(response, str):
        try:
            response = json.loads(response)

        except json.JSONDecodeError:
            return {
                'status': 'error',
                'message': f'The API is documented, but the documentation is not valid JSON. Please check the documentation at {uri}',
                'check_swagger_response': swagger_doc,
            }

    try:
        paths = response.get('paths', {})

    except AttributeError:
        return {
            'status': 'error',
            'message': 'The API is documented, but no paths were found',
            'check_swagger_response': swagger_doc,
        }

    feedback = await _verify_maturity_paths(paths)
    https = await _supports_https(uri)

    status = 'success' if feedback['messages'] else 'error'

    feedbacks['status'] = status
    feedbacks['https'] = https['message']
    feedbacks['feedback'] = feedback

    return feedbacks


async def estimate_rate_limit(uri: str, max_requests: int):
    """Analyze the rate limit of a REST API using multiple requests in parallel.

    Parameters:
        uri (str): The base URI of the API.
        max_requests (int): The max quantity of requests the users want to test.

    Returns:
        dict: A dictionary containing feedback on how the API was able to support multiple parallel requests.

    Examples:
        >>> import asyncio
        >>> asyncio.run(estimate_rate_limit('http://127.0.0.1:8000', 100)) # doctest: +SKIP
        {'status': 'success', 'message': 'The API returned a 429 error (too many requests). This indicates that the rate limit has been exceeded', 'response': '{...}'}
    """

    async def make_request(session, uri):
        try:
            response = await session.get(uri)
            if response.status_code == 429:
                return {
                    'status': 'error',
                    'message': f'The API returned a 429 error (too many requests). This indicates that the rate limit has been exceeded',
                    'response_code': response.status_code,
                }
            return {
                'status': 'success',
                'message': 'All requests were successful',
                'response_code': response.status_code,
            }
        except httpx.RequestError as exc:
            return {
                'status': 'error',
                'message': f'An error occurred while requesting {uri}: {exc}',
                'response_code': None,
            }

    async with httpx.AsyncClient() as client:
        tasks = []
        for _ in range(max_requests):
            tasks.append(make_request(client, uri))
        results = await asyncio.gather(*tasks)

        for result in results:
            if result['status'] == 'error':
                return result

    return {
        'status': 'success',
        'message': f'All of {max_requests} requests were successful without 429 errors. This suggests that the API can support the specified number of requests',
        'response_code': None,
    }
