import json
import xml.etree.ElementTree as ET

import httpx


async def _is_rest_api(uri: str) -> bool:
    """Verifies if the given URI belongs to a REST API.

    This function sends a GET request to the URI and checks the response headers and content to determine whether it is a REST API.
    Currently, this function recognizes only APIs that return JSON or XML content.

    Parameters:
        uri (str): The URI to be checked.

    Returns:
        bool: True if the API is REST, False otherwise.

    Raises:
        httpx.HTTPError: If there was an error making the request (handled within the function and reported to the console).

    Examples:
        >>> import asyncio
        >>> asyncio.run(_is_rest_api('http://127.0.0.1:8000')) # doctest: +SKIP
        True
    """
    if not uri.startswith('http') or not uri.startswith('https'):
        return False

    try:
        async with httpx.AsyncClient(
            follow_redirects=True, headers={'User-Agent': 'API Checker'}
        ) as client:
            url = uri.rstrip('/') + '/'
            response = await client.get(url, timeout=10)

        if response.status_code // 100 != 2:
            return False

        content_type = response.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            try:
                data = response.json()
                if isinstance(data, (list, dict)):
                    return True
            except json.JSONDecodeError:
                pass

        elif 'application/xml' in content_type:
            try:
                tree = ET.fromstring(response.text)
                if tree is not None:
                    return True
            except ET.ParseError:
                pass

        allow_header = response.headers.get('Allow', '')
        if any(
            verb in allow_header
            for verb in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        ):
            return True

    except httpx.HTTPError as e:
        print(f'An HTTP error occurred: {e}')
    except json.JSONDecodeError:
        print('Error decoding JSON response')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

    return False


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
    async with httpx.AsyncClient(
        follow_redirects=True, headers={'User-Agent': 'API Checker'}
    ) as client:
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
            try:
                response = await client.get(f'{url}/{endpoint}', timeout=10)
                if response.status_code // 100 != 2:
                    _errors.add(
                        f'{response.status_code} Client Error: {response.reason_phrase} for url: {response.url}'
                    )
                    continue

                if 'application/json' in response.headers.get(
                    'Content-Type', ''
                ):
                    _response = response.json()
                    if any(
                        term in str(_response).lower() for term in api_terms
                    ):
                        message = f'REST API JSON documentation found at {url}/{endpoint}'
                        if not doc_endpoint:
                            message += ' (Endpoint not specified, but we identified it)'
                        return {
                            'status': 'success',
                            'message': message,
                            'response': _response,
                        }
                elif any(term in response.text.lower() for term in api_terms):
                    message = f'Potential REST API documentation found at {url}/{endpoint}, but not in JSON format.'
                    if not doc_endpoint:
                        message += ' (Endpoint not specified, please provide the JSON documentation endpoint)'
                    return {
                        'status': 'warning',
                        'message': message,
                        'response': None,
                    }

            except httpx.RequestError as exc:
                _errors.add(
                    f'An error occurred while requesting {url}/{endpoint}: {exc}'
                )
                continue

        message = 'No REST API documentation found.'

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
        {'status': 'success', 'message': 'The URI does not support HTTPS at http://127.0.0.1:8000/. ', 'response': '{...}'}
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
                    'message': 'The URI supports HTTPS at {uri}.',
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
        'message': 'The URI does not support HTTPS at {uri}.',
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
                    f'Consider following the standard RESTful methods for better maturity.'
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
                            f'✅   Congratulations! The {path} method returns the correct status code for {method.upper()} requests.'
                        )
                        messages.append(
                            f'⚠️   Warning! Richardson\'s maturity model recommends using "{expected_description}" as the description for {method.upper()} requests.'
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
                'message': f'The API is documented, but the documentation is not valid JSON. Please check the documentation at {uri}.',
                'check_swagger_response': swagger_doc,
            }

    try:
        paths = response.get('paths', {})

    except AttributeError:
        return {
            'status': 'error',
            'message': 'The API is documented, but no paths were found.',
            'check_swagger_response': swagger_doc,
        }

    feedback = await _verify_maturity_paths(paths)
    https = await _supports_https(uri)

    status = 'success' if feedback['messages'] else 'error'

    feedbacks['status'] = status
    feedbacks['feedback'] = feedback
    feedbacks['https'] = https

    return feedbacks
