import asyncio

from apilyzer.verify import (
    _is_json_rest_api,
    _supports_https,
    analyze_api_maturity,
    check_documentation_json,
    estimate_rate_limit,
)


def test_is_json_rest_api_true():
    is_rest, response = asyncio.run(
        _is_json_rest_api(
            'https://picpay.github.io/picpay-docs-digital-payments/swagger/checkout.json'
        )
    )

    assert is_rest is True
    assert response is not None


def test_is_json_rest_api_false():
    is_rest, response = asyncio.run(_is_json_rest_api('http://google.com'))

    assert is_rest is False
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']


def test_url_is_json_rest_api_invalid():
    is_rest, response = asyncio.run(_is_json_rest_api('https://invalid_url'))

    assert is_rest is False
    assert response is None


def test_is_json_rest_api_no_http():
    is_rest, response = asyncio.run(
        _is_json_rest_api('petstore.swagger.io/v2/swagger')
    )

    assert is_rest is False
    assert response is None


def test_is_json_rest_api_no_json():
    is_rest, response = asyncio.run(
        _is_json_rest_api('http://rss.cnn.com/rss/cnn_topstories.rss')
    )

    assert is_rest is False
    assert response.status_code == 200
    assert 'text/xml' in response.headers['content-type']


def test_check_documentation_json_success_doc():
    result = asyncio.run(
        check_documentation_json(
            'https://petstore.swagger.io/v2', 'swagger.json'
        )
    )
    assert result['status'] == 'success'
    assert (
        'REST API JSON documentation found at https://petstore.swagger.io/v2/swagger.json'
        in result['message']
    )
    assert 'swagger' in result['response'] or 'openapi' in result['response']


def test_check_documentation_json_success_no_doc():
    result = asyncio.run(
        check_documentation_json('https://petstore.swagger.io/v2')
    )
    assert result['status'] == 'success'
    assert (
        'REST API JSON documentation found at https://petstore.swagger.io/v2/swagger.json'
        in result['message']
    )
    assert 'swagger' in result['response'] or 'openapi' in result['response']


def test_check_documentation_json_no_api_doc():
    result = asyncio.run(
        check_documentation_json('https://google.com', 'swagger.json')
    )
    assert result['status'] == 'error'
    assert 'No REST API documentation found' in result['message']
    assert (
        'The URL https://google.com/swagger.json does not seem to be a JSON REST API'
        in result['response']
    )


def test_check_documentation_json_no_api_no_doc():
    result = asyncio.run(check_documentation_json('https://google.com'))
    assert result['status'] == 'error'
    assert 'No REST API documentation found' in result['message']
    assert (
        '(Endpoint not specified, and we could not identify it with the base URL alone)'
        in result['message']
    )


def test_check_documentation_json_invalid_url_doc():
    invalid_url = 'https://invalid_url.com'
    result = asyncio.run(check_documentation_json(invalid_url))
    assert result['status'] == 'error'
    assert 'No REST API documentation found' in result['message']
    assert (
        '(Endpoint not specified, and we could not identify it with the base URL alone)'
        in result['message']
    )
    assert (
        'The base URL provided (https://invalid_url.com) does not seem to be a JSON REST API. Try specifying the documentation endpoint'
        in result['response']
    )


def test_check_documentation_json_invalid_url_no_doc():
    invalid_url = 'invalid_url.com'
    result = asyncio.run(check_documentation_json(invalid_url, 'swagger.json'))
    assert result['status'] == 'error'
    assert 'No REST API documentation found' in result['message']
    assert (
        '(Endpoint not specified, and we could not identify it with the base URL alone)'
        not in result['message']
    )
    assert (
        f'The URL {invalid_url}/swagger.json does not seem to be a JSON REST API'
        in result['response']
    )


def test_check_documentation_json_potential_doc_but_no_json_no_doc():
    uri = 'https://developer.twitter.com/en/docs/twitter-api/'
    result = asyncio.run(check_documentation_json(uri))
    assert result['status'] == 'warning'
    assert (
        f'Potential REST API documentation found at {uri}, but not in JSON format'
        in result['message']
    )
    assert (
        '(Endpoint not specified, please provide the JSON documentation endpoint)'
        in result['message']
    )


def test_analyze_api_maturity():
    result = asyncio.run(
        analyze_api_maturity('https://petstore.swagger.io/v2/swagger.json')
    )
    assert result['status'] == 'success'
    assert result['feedback']['messages'] is not None


def test_analyze_api_maturity_invalid_url():
    result = asyncio.run(analyze_api_maturity('https://invalid_url'))
    assert result['status'] == 'error'
    assert 'No REST API documentation found' in result['message']


def test_supports_https_success():
    result = asyncio.run(
        _supports_https('https://nv-research-tlv.netlify.app/')
    )
    assert result['status'] == 'success'
    assert 'URI supports HTTPS' in result['message']


def test_supports_https_failure():
    result = asyncio.run(_supports_https('https://petstore.swagger.io/v2'))
    assert result['status'] == 'error'
    assert 'URI does not support HTTPS' in result['message']


def test_estimate_rate_limit_success():
    api_url = 'https://petstore.swagger.io/v2/pet/1'
    max_requests = 100
    result = asyncio.run(estimate_rate_limit(api_url, max_requests))
    assert result['status'] == 'success'
    assert 'requests were successful without 429 errors' in result['message']


def test_estimate_rate_limit_request_error():
    api_url = 'https://api-with-request-error.com'
    max_requests = 100
    result = asyncio.run(estimate_rate_limit(api_url, max_requests))
    assert result['status'] == 'error'
    assert 'An error occurred while requesting' in result['message']
