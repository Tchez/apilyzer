from unittest.mock import AsyncMock, patch

from typer.testing import CliRunner

from apilyzer.cli import app

runner = CliRunner()


def test_main():
    result = runner.invoke(app)
    assert result.exit_code == 0


def test_cli_returns_success():
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0


@patch('apilyzer.cli.check_documentation_json', new_callable=AsyncMock)
def test_cli_verify_rest_return_success_with_flag(check_documentation_json):
    check_documentation_json.return_value = {'status': 'success'}
    result = runner.invoke(
        app,
        [
            'verify-rest',
            'https://petstore.swagger.io',
            '--doc-endpoint',
            'v2/swagger',
        ],
    )
    assert result.exit_code == 0
    assert "'status': 'success'" in result.stdout
    check_documentation_json.assert_awaited_once_with(
        'https://petstore.swagger.io', 'v2/swagger'
    )


@patch('apilyzer.cli.check_documentation_json', new_callable=AsyncMock)
def test_cli_verify_rest_return_success_with_alias(check_documentation_json):
    check_documentation_json.return_value = {'status': 'success'}
    result = runner.invoke(
        app,
        ['verify-rest', 'https://petstore.swagger.io', '-e', 'v2/swagger'],
    )
    assert result.exit_code == 0
    assert "'status': 'success'" in result.stdout
    check_documentation_json.assert_awaited_once_with(
        'https://petstore.swagger.io', 'v2/swagger'
    )


@patch('apilyzer.cli.check_documentation_json', new_callable=AsyncMock)
def test_cli_verify_rest_return_success_without_flag(
    check_documentation_json,
):
    check_documentation_json.return_value = {'status': 'success'}
    result = runner.invoke(
        app, ['verify-rest', 'https://petstore.swagger.io/v2/swagger']
    )
    assert result.exit_code == 0
    assert "'status': 'success'" in result.stdout
    check_documentation_json.assert_awaited_once_with(
        'https://petstore.swagger.io/v2/swagger', None
    )


@patch('apilyzer.cli.analyze_api_maturity', new_callable=AsyncMock)
def test_cli_verify_maturity_return_success_with_flag(analyze_api_maturity):
    analyze_api_maturity.return_value = {'status': 'success'}
    result = runner.invoke(
        app,
        [
            'verify-maturity',
            'https://picpay.github.io',
            '--doc-endpoint',
            'picpay-docs-digital-payments/swagger/checkout.json',
        ],
    )
    assert result.exit_code == 0
    assert "'status': 'success'" in result.stdout
    analyze_api_maturity.assert_awaited_once_with(
        'https://picpay.github.io',
        'picpay-docs-digital-payments/swagger/checkout.json',
    )


@patch('apilyzer.cli.analyze_api_maturity', new_callable=AsyncMock)
def test_cli_verify_maturity_return_success_with_alias(analyze_api_maturity):
    analyze_api_maturity.return_value = {'status': 'success'}
    result = runner.invoke(
        app,
        [
            'verify-maturity',
            'https://picpay.github.io',
            '-e',
            'picpay-docs-digital-payments/swagger/checkout.json',
        ],
    )
    assert result.exit_code == 0
    assert "'status': 'success'" in result.stdout
    analyze_api_maturity.assert_awaited_once_with(
        'https://picpay.github.io',
        'picpay-docs-digital-payments/swagger/checkout.json',
    )


@patch('apilyzer.cli.analyze_api_maturity', new_callable=AsyncMock)
def test_cli_verify_maturity_return_success_without_flag(
    analyze_api_maturity,
):
    analyze_api_maturity.return_value = {'status': 'success'}
    result = runner.invoke(
        app,
        [
            'verify-maturity',
            'https://picpay.github.io/picpay-docs-digital-payments/swagger/checkout.json',
        ],
    )
    assert result.exit_code == 0
    assert "'status': 'success'" in result.stdout
    analyze_api_maturity.assert_awaited_once_with(
        'https://picpay.github.io/picpay-docs-digital-payments/swagger/checkout.json',
        None,
    )


@patch('apilyzer.cli.estimate_rate_limit', new_callable=AsyncMock)
def test_cli_test_rate_return_success_default_arg(estimate_rate_limit):
    estimate_rate_limit.return_value = {'status': 'success'}
    result = runner.invoke(
        app, ['test-rate', 'https://petstore.swagger.io/v2/pet']
    )
    assert result.exit_code == 0
    assert "'status': 'success'" in result.stdout
    estimate_rate_limit.assert_awaited_once_with(
        'https://petstore.swagger.io/v2/pet', 50
    )


@patch('apilyzer.cli.estimate_rate_limit', new_callable=AsyncMock)
def test_cli_test_rate_return_success_with_arg(estimate_rate_limit):
    estimate_rate_limit.return_value = {'status': 'success'}
    result = runner.invoke(
        app, ['test-rate', 'https://petstore.swagger.io/v2/pet', '50']
    )
    assert result.exit_code == 0
    assert "'status': 'success'" in result.stdout
    estimate_rate_limit.assert_awaited_once_with(
        'https://petstore.swagger.io/v2/pet', 50
    )
