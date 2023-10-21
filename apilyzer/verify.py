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

    Examples:
        >>> import asyncio
        >>> asyncio.run(_is_json_rest_api('http://127.0.0.1:8000')) # doctest: +SKIP
        True, <Response [200 OK]>
    """
    if not (uri.startswith('http')):
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

    allow_header = response.headers.get('access-control-allow-methods', '')
    if any(
        verb in allow_header
        for verb in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    ):
        return True, response

    content_type = response.headers.get('Content-Type', '')

    if 'application/json' in content_type:
        data = response.json()
        if isinstance(data, (list, dict)):
            return True, response

    return False, response


async def check_documentation_json(uri: str, doc_endpoint: str = None) -> dict:
    """Check if the given base URI of an API has REST API documentation available. If the documentation endpoint is not specified, the function will try to identify it.

    Parameters:
        uri (str): The base URI of the API.
        doc_endpoint (str, optional): The endpoint where the documentation is available. Defaults to None.

    Returns:
        dict: A dictionary containing the 'status', 'message', and 'response' keys detailing the outcome of the check.

    Examples:
        >>> import asyncio
        >>> asyncio.run(check_documentation_json('http://127.0.0.1:8000')) # doctest: +SKIP
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

            if not is_rest and doc_endpoint:
                _errors.add(
                    f'The URL {full_url} does not seem to be a JSON REST API'
                )

            if not response and not doc_endpoint:
                _errors.add(
                    f'The base URL provided ({uri}) does not seem to be a JSON REST API. Try specifying the documentation endpoint'
                )

            if response and response.status_code // 100 != 2 and doc_endpoint:
                _errors.add(
                    f'{response.status_code} Client Error: {response.reason_phrase} for url: {response.url}'
                )

            if response and any(
                term in response.text.lower() for term in api_terms
            ):
                if 'application/json' in response.headers.get(
                    'Content-Type', ''
                ):
                    return {
                        'status': 'success',
                        'message': f'REST API JSON documentation found at {full_url}',
                        'response': response.json(),
                    }
                elif response.status_code // 100 == 2:
                    message = f'Potential REST API documentation found at {full_url}, but not in JSON format'
                    if not doc_endpoint:
                        message += ' (Endpoint not specified, please provide the JSON documentation endpoint)'
                    return {
                        'status': 'warning',
                        'message': message,
                        'response': response.text,
                    }

        except Exception as e:
            if doc_endpoint:
                _errors.add(
                    f'An error occurred while requesting {full_url}: {e}'
                )
            else:
                _errors.add(
                    f'An error occurred while requesting {uri}: Endpoint not specified, and we could not identify it with the base URL alone. Please provide the JSON documentation endpoint'
                )

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

    async with httpx.AsyncClient(timeout=10) as client:
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
    expected_responses = {
        'get': {
            '200': 'OK',
        },
        'post': {
            '201': 'Created',
        },
        'put': {
            '200': 'OK',
        },
        'patch': {
            '200': 'OK',
        },
        'delete': {
            '200': 'OK',
        },
    }
    valid_methods = set(expected_responses.keys())

    for path, path_info in paths.items():
        for method, method_info in path_info.items():
            if method not in valid_methods:
                messages.append(
                    f'🚫   Alert! The {path} path uses a non-conventional {method.upper()} method.'
                    f' Consider following the standard RESTful methods for better maturity.'
                )
                continue

            if method != 'post':
                _has_only_post_method = False

            responses = method_info.get('responses', {})
            for status, expected_description in expected_responses.get(
                method, {}
            ).items():
                actual_description = responses.get(status, {}).get(
                    'description'
                )
                if status in responses:
                    if actual_description == expected_description:
                        messages.append(
                            f'✅   Congratulations! The {path} path for {method.upper()} requests returns the correct status code ({status}) and description'
                        )
                    else:
                        messages.append(
                            f'✅   Congratulations! The {path} method returns the correct status code for {method.upper()} requests'
                        )
                        messages.append(
                            f'⚠️   Warning! The {path} path for {method.upper()} requests should return the description "{expected_description}" for the {status} status code, but it returns "{actual_description}" instead'
                        )
                else:
                    messages.append(
                        f'🚫   Error! The {path} path for {method.upper()} requests is missing the expected {status} status code'
                    )

    if _has_only_post_method:
        messages.append(
            "🚫   Error! The API only has POST methods. It is at level 0 of Richardson's maturity model"
        )
    else:
        messages.append(
            "✅   Congratulations! The API has methods other than POST. It is at least at level 1 of Richardson's maturity model"
        )

    feedback['messages'] = messages
    return feedback


async def analyze_api_maturity(uri: str, doc_endpoint: str = None) -> dict:
    """Analyze the maturity level of a REST API using Richardson's maturity model.

    Parameters:
        uri (str): The base URI of the API.
        doc_endpoint (str, optional): The endpoint where the documentation is available. Defaults to None.

    Returns:
        dict: A dictionary containing feedback on the API's maturity level according to Richardson's maturity model.
    """
    feedbacks = {}

    swagger_doc = await check_documentation_json(uri, doc_endpoint)

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


async def estimate_rate_limit(uri: str, max_requests: int) -> dict:
    """Analyze the rate limit of a REST API using multiple requests in parallel.

    Parameters:
        uri (str): The base URI of the API.
        max_requests (int): The max quantity of requests the users want to test.

    Returns:
        dict: A dictionary containing feedback on how the API was able to support multiple parallel requests.

    Examples:
        >>> import asyncio
        >>> asyncio.run(estimate_rate_limit('http://127.0.0.1:8000', 100)) # doctest: +SKIP
        {'status': 'success', 'message': 'The API returned a 429 error (too many requests). This indicates that the rate limit has been exceeded'}
    """

    async def make_request(session, uri):
        try:
            response = await session.get(uri)
            if response.status_code == 429:
                return {
                    'status': 'error',
                    'message': f'The API returned a 429 error (too many requests). This indicates that the rate limit has been exceeded',
                }
            return {
                'status': 'success',
                'message': 'All requests were successful',
            }
        except httpx.RequestError as exc:
            return {
                'status': 'error',
                'message': f'An error occurred while requesting {uri}: {exc}',
            }

    async with httpx.AsyncClient(timeout=10) as client:
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
    }
