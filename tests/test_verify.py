import asyncio

import httpx
import respx

from apilizer.verify import check_swagger


@respx.mock
def test_check_swagger_with_api_and_swagger():
    respx.get('http://127.0.0.1:8000/swagger.json').mock(
        return_value=httpx.Response(200, json={})
    )

    result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
    assert result == {
        'status': 'success',
        'message': 'Swagger documentation found.',
    }


@respx.mock
def test_check_swagger_with_api_and_no_swagger():
    respx.get('http://127.0.0.1:8000/swagger.json').mock(
        return_value=httpx.Response(404)
    )

    result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
    assert result == {
        'status': 'failure',
        'message': 'Unexpected status code: 404',
    }


@respx.mock
def test_check_swagger_no_api():
    respx.get('http://127.0.0.1:8000/swagger.json').mock(
        side_effect=httpx.NetworkError('Error')
    )

    result = asyncio.run(check_swagger('http://127.0.0.1:8000'))
    assert result['status'] == 'failure'
    assert 'Could not reach the API' in result['message']


def test_check_swagger_invalid_url():
    result = asyncio.run(check_swagger('invalid_url'))
    assert result['status'] == 'failure'
    assert 'Could not reach the API:' in result['message']
