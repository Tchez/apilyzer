import asyncio

import httpx
import respx

from apilizer.verify import check_swagger


@respx.mock
def test_check_swagger_with_openapi_endpoint():
    respx.get('http://127.0.0.1:8000/openapi.json').mock(
        return_value=httpx.Response(200, json={})
    )

    result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
    assert result == {
        'status': 'success',
        'message': 'Swagger/OpenAPI documentation found at http://127.0.0.1:8000/openapi.json.',
    }


@respx.mock
def test_check_swagger_with_swagger_endpoint():
    respx.get('http://127.0.0.1:8000/openapi.json').mock(
        return_value=httpx.Response(404)
    )
    respx.get('http://127.0.0.1:8000/swagger.json').mock(
        return_value=httpx.Response(200, json={})
    )

    result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
    assert result == {
        'status': 'success',
        'message': 'Swagger/OpenAPI documentation found at http://127.0.0.1:8000/swagger.json.',
    }


@respx.mock
def test_check_swagger_with_api_and_no_documentation():
    respx.get('http://127.0.0.1:8000/openapi.json').mock(
        return_value=httpx.Response(404)
    )
    respx.get('http://127.0.0.1:8000/swagger.json').mock(
        return_value=httpx.Response(404)
    )

    result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
    assert result == {
        'status': 'failure',
        'message': "Could not find Swagger/OpenAPI documentation. Errors encountered: ['404 Client Error: Not Found for url: http://127.0.0.1:8000/openapi.json', '404 Client Error: Not Found for url: http://127.0.0.1:8000/swagger.json']",
    }


@respx.mock
def test_check_swagger_no_api():
    respx.get('http://127.0.0.1:8000/openapi.json').mock(
        side_effect=httpx.NetworkError('Error')
    )
    respx.get('http://127.0.0.1:8000/swagger.json').mock(
        side_effect=httpx.NetworkError('Error')
    )

    result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
    assert result['status'] == 'failure'
    assert (
        'Could not find Swagger/OpenAPI documentation. Errors encountered: ['
        in result['message']
    )


def test_check_swagger_invalid_url():
    result = asyncio.run(check_swagger('invalid_url'))
    assert result['status'] == 'failure'
    assert (
        'Could not find Swagger/OpenAPI documentation. Errors encountered: ['
        in result['message']
    )
