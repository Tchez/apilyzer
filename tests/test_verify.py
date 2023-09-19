import asyncio

import pytest

from apilizer.verify import check_swagger_rest, find_docs_in_links, is_rest_api


def test_rest_api_true():
    assert asyncio.run(is_rest_api('https://pokeapi.co/api/v2/')) is True


@pytest.mark.skip(reason='Needs to be fixed. Error known.')
def test_is_rest_api_false():
    assert asyncio.run(is_rest_api('https://google.com')) is False


def test_url_is_rest_api_invalid():
    assert asyncio.run(is_rest_api('invalid_url')) is False


def test_check_swagger_rest_success_doc():
    result = asyncio.run(check_swagger_rest('https://pokeapi.co/api/v2/'))
    assert result['status'] == 'success'
    assert (
        'Potential REST API documentation found at https://pokeapi.co/api/v2/'
        in result['message']
    )


@pytest.mark.skip(reason='Needs to be fixed. Error known.')
def test_check_swagger_rest_no_doc():
    result = asyncio.run(check_swagger_rest('https://google.com'))
    assert result['status'] == 'failure'
    assert (
        'Could not find REST API documentation. Errors encountered: ['
        in result['message']
    )


def test_check_swagger_rest_invalid_url():
    invalid_url = 'invalid_url.com'
    result = asyncio.run(check_swagger_rest(invalid_url))
    assert result['status'] == 'error'
    assert (
        f'{invalid_url} does not appear to be a REST API.' in result['message']
    )


# @respx.mock
# def test_check_swagger_with_openapi_endpoint():
#     respx.get('http://127.0.0.1:8000/openapi.json').mock(
#         return_value=httpx.Response(200, json={})
#     )

#     result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
#     assert result == {
#         'status': 'success',
#         'message': 'Swagger/OpenAPI documentation found at http://127.0.0.1:8000/openapi.json.',
#         'paths': {},
#     }


# @respx.mock
# def test_check_swagger_with_swagger_endpoint():
#     respx.get('http://127.0.0.1:8000/openapi.json').mock(
#         return_value=httpx.Response(404)
#     )
#     respx.get('http://127.0.0.1:8000/swagger.json').mock(
#         return_value=httpx.Response(200, json={})
#     )

#     result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
#     assert result == {
#         'status': 'success',
#         'message': 'Swagger/OpenAPI documentation found at http://127.0.0.1:8000/swagger.json.',
#         'paths': {},
#     }


# @respx.mock
# def test_check_swagger_with_api_and_no_documentation():
#     respx.get('http://127.0.0.1:8000/openapi.json').mock(
#         return_value=httpx.Response(404)
#     )
#     respx.get('http://127.0.0.1:8000/swagger.json').mock(
#         return_value=httpx.Response(404)
#     )

#     result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
#     assert result == {
#         'status': 'failure',
#         'message': "Could not find Swagger/OpenAPI documentation. Errors encountered: ['404 Client Error: Not Found for url: http://127.0.0.1:8000/openapi.json', '404 Client Error: Not Found for url: http://127.0.0.1:8000/swagger.json']",
#         'paths': {},
#     }


# @respx.mock
# def test_check_swagger_no_api():
#     respx.get('http://127.0.0.1:8000/openapi.json').mock(
#         side_effect=httpx.NetworkError('Error')
#     )
#     respx.get('http://127.0.0.1:8000/swagger.json').mock(
#         side_effect=httpx.NetworkError('Error')
#     )

#     result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
#     assert result['status'] == 'failure'
#     assert (
#         'Could not find Swagger/OpenAPI documentation. Errors encountered: ['
#         in result['message']
#     )


# def test_check_swagger_invalid_url():
#     result = asyncio.run(check_swagger('invalid_url'))
#     assert result['status'] == 'failure'
#     assert (
#         'Could not find Swagger/OpenAPI documentation. Errors encountered: ['
#         in result['message']
#     )
