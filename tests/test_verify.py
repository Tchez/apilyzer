import asyncio

from apilyzer.verify import (
    _is_json_rest_api,
    _supports_https,
    _verify_maturity_paths,
    analyze_api_maturity,
    check_documentation_json,
    estimate_rate_limit,
)


def test_is_json_rest_api_true():
    is_rest, response = asyncio.run(
        _is_json_rest_api('https://petstore.swagger.io/v2/swagger.json')
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


def test_is_json_rest_api_json_response(monkeypatch):
    class FakeResponse:
        status_code = 200
        headers = {'Content-Type': 'application/json'}

        def json(self):
            return {'paths': {}}

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, uri, timeout=None):
            return FakeResponse()

    import apilyzer.verify as verify_module

    monkeypatch.setattr(verify_module.httpx, 'AsyncClient', FakeAsyncClient)

    is_rest, response = asyncio.run(
        _is_json_rest_api('https://example.com/swagger.json')
    )

    assert is_rest is True
    assert response is not None



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


def test_check_documentation_json_no_response_from_base_url(monkeypatch):
    async def fake_is_json_rest_api(uri):
        return False, None

    import apilyzer.verify as verify_module

    monkeypatch.setattr(verify_module, '_is_json_rest_api', fake_is_json_rest_api)

    result = asyncio.run(check_documentation_json('https://example.com'))

    assert result['status'] == 'error'
    assert (
        '(Endpoint not specified, and we could not identify it with the base URL alone)'
        in result['message']
    )
    assert (
        'The base URL provided (https://example.com) does not seem to be a JSON REST API. Try specifying the documentation endpoint'
        in result['response']
    )


def test_check_documentation_json_request_exception(monkeypatch):
    async def fake_is_json_rest_api(uri):
        raise RuntimeError('boom')

    import apilyzer.verify as verify_module

    monkeypatch.setattr(verify_module, '_is_json_rest_api', fake_is_json_rest_api)

    result = asyncio.run(check_documentation_json('https://example.com'))

    assert result['status'] == 'error'
    assert any('An error occurred while requesting' in msg for msg in result['response'])


def test_check_documentation_json_json_payload_no_api_terms(monkeypatch):
    class FakeResponse:
        status_code = 200
        headers = {'Content-Type': 'application/json'}

        def json(self):
            return {'foo': {}}

        @property
        def text(self):
            return '{"foo": {}}'

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, uri, *args, **kwargs):
            return FakeResponse()


    import apilyzer.verify as verify_module

    monkeypatch.setattr(verify_module.httpx, 'AsyncClient', FakeAsyncClient)

    result = asyncio.run(check_documentation_json('https://example.com'))

    assert result['status'] == 'error'
    assert 'No REST API documentation found' in result['message']


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
    assert 'Potential REST API documentation found at' in result['message']
    assert 'but not in JSON format' in result['message']
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


def test_analyze_api_maturity_invalid_json(monkeypatch):
    async def fake_check_documentation_json(uri, doc_endpoint=None):
        return {'status': 'success', 'response': 'not-a-dict'}

    import apilyzer.verify as verify_module

    monkeypatch.setattr(
        verify_module,
        'check_documentation_json',
        fake_check_documentation_json,
    )

    result = asyncio.run(analyze_api_maturity('https://example.com/swagger.json'))

    assert result['status'] == 'error'
    assert 'not valid JSON' in result['message']


def test_analyze_api_maturity_response_list(monkeypatch):
    async def fake_check_documentation_json(uri, doc_endpoint=None):
        return {'status': 'success', 'response': []}

    import apilyzer.verify as verify_module

    monkeypatch.setattr(
        verify_module,
        'check_documentation_json',
        fake_check_documentation_json,
    )

    result = asyncio.run(analyze_api_maturity('https://example.com/swagger.json'))

    assert result['status'] == 'error'
    assert 'no paths were found' in result['message']


def test_analyze_api_maturity_with_mocked_https_check(monkeypatch):
    async def fake_check_documentation_json(uri, doc_endpoint=None):
        return {
            'status': 'success',
            'response': {
                'paths': {
                    '/pets': {
                        'get': {'responses': {'200': {'description': 'OK'}}}
                    }
                }
            },
        }

    async def fake_supports_https(uri):
        return {
            'status': 'error',
            'message': '🚫 The URI does not support HTTPS at https://example.com',
        }

    import apilyzer.verify as verify_module

    monkeypatch.setattr(
        verify_module,
        'check_documentation_json',
        fake_check_documentation_json,
    )
    monkeypatch.setattr(verify_module, '_supports_https', fake_supports_https)

    result = asyncio.run(analyze_api_maturity('https://example.com/swagger.json'))

    assert result['status'] == 'success'
    assert result['https'] == '🚫 The URI does not support HTTPS at https://example.com'
    assert result['feedback']['messages'] is not None


def test_verify_maturity_paths_non_conventional_and_correct_get():
    result = asyncio.run(
        _verify_maturity_paths(
            {
                '/pets': {
                    'trace': {'responses': {}},
                    'get': {'responses': {'200': {'description': 'OK'}}},
                }
            }
        )
    )

    assert any('non-conventional TRACE' in msg for msg in result['messages'])
    assert any(
        'returns the correct status code (200) and description' in msg
        for msg in result['messages']
    )


def test_verify_maturity_paths_only_post_methods():
    result = asyncio.run(
        _verify_maturity_paths(
            {
                '/pets': {
                    'post': {'responses': {'201': {'description': 'Created'}}},
                }
            }
        )
    )

    assert any('API only has POST methods' in msg for msg in result['messages'])


def test_verify_maturity_paths_missing_expected_response():
    result = asyncio.run(
        _verify_maturity_paths(
            {
                '/pets': {
                    'get': {'responses': {}},
                }
            }
        )
    )

    assert any(
        'missing the expected 200 status code' in msg for msg in result['messages']
    )


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


def test_supports_https_request_error(monkeypatch):
    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, uri):
            import apilyzer.verify as verify_module

            request = verify_module.httpx.Request('GET', uri)
            raise verify_module.httpx.RequestError('boom', request=request)

    import apilyzer.verify as verify_module

    monkeypatch.setattr(verify_module.httpx, 'AsyncClient', FakeAsyncClient)

    result = asyncio.run(_supports_https('https://example.com'))

    assert result['status'] == 'error'
    assert 'does not support HTTPS' in result['message']
    assert any(
        'An error occurred while requesting' in msg for msg in result['response']
    )


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


def test_estimate_rate_limit_too_many_requests(monkeypatch):
    class FakeResponse:
        status_code = 429

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            self.timeout = kwargs.get('timeout')

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, uri):
            return FakeResponse()

    import apilyzer.verify as verify_module

    monkeypatch.setattr(verify_module.httpx, 'AsyncClient', FakeAsyncClient)

    result = asyncio.run(estimate_rate_limit('https://example.com', 3))

    assert result['status'] == 'error'
    assert '429 error (too many requests)' in result['message']


def test_check_documentation_json_request_exception_with_doc_endpoint(monkeypatch):
    async def fake_is_json_rest_api(uri):
        raise RuntimeError('boom')

    import apilyzer.verify as verify_module

    monkeypatch.setattr(verify_module, '_is_json_rest_api', fake_is_json_rest_api)

    result = asyncio.run(
        check_documentation_json('https://example.com', 'swagger.json')
    )

    assert result['status'] == 'error'
    assert any(
        'An error occurred while requesting https://example.com/swagger.json'
        in msg
        for msg in result['response']
    )
