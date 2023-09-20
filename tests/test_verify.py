import asyncio

from apilyzer.verify import check_swagger_rest, is_rest_api


def test_rest_api_true():
    assert asyncio.run(is_rest_api('https://petstore.swagger.io/v2')) is True


def test_is_rest_api_false():
    assert asyncio.run(is_rest_api('https://google.com')) is False


def test_url_is_rest_api_invalid():
    assert asyncio.run(is_rest_api('invalid_url')) is False


def test_check_swagger_rest_success_doc():
    result = asyncio.run(check_swagger_rest('https://petstore.swagger.io/v2'))
    assert result['status'] == 'success'
    assert (
        'Potential REST API documentation found at https://petstore.swagger.io/v2'
        in result['message']
    )


def test_check_swagger_rest_no_doc():
    result = asyncio.run(check_swagger_rest('https://google.com'))
    assert result['status'] == 'error'
    assert (
        'https://google.com does not appear to be a REST API'
        in result['message']
    )


def test_check_swagger_rest_invalid_url():
    invalid_url = 'invalid_url.com'
    result = asyncio.run(check_swagger_rest(invalid_url))
    assert result['status'] == 'error'
    assert (
        f'{invalid_url} does not appear to be a REST API.' in result['message']
    )
