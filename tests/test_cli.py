from typer.testing import CliRunner

from apilyzer.cli import app

runner = CliRunner()


def test_main():
    result = runner.invoke(app)
    assert result.exit_code == 0


def test_cli_returns_success():
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0


def test_cli_verify_rest_return_success_with_flag():
    result = runner.invoke(
        app,
        [
            'verify-rest',
            'https://petstore.swagger.io',
            '--doc-endpoint',
            'v2/swagger',
        ],
    )
    "'status': 'success'" in result.stdout


def test_cli_verify_rest_return_success_with_alias():
    result = runner.invoke(
        app,
        ['verify-rest', 'https://petstore.swagger.io', '-e', 'v2/swagger'],
    )
    "'status': 'success'" in result.stdout


def test_cli_verify_rest_return_success_without_flag():
    result = runner.invoke(
        app, ['verify-rest', 'https://petstore.swagger.io/v2/swagger']
    )
    "'status': 'success'" in result.stdout


def test_cli_verify_maturity_return_success_with_flag():
    result = runner.invoke(
        app,
        [
            'verify-maturity',
            'https://picpay.github.io',
            '--doc-endpoint',
            'picpay-docs-digital-payments/swagger/checkout.json',
        ],
    )
    "'status': 'success'" in result.stdout


def test_cli_verify_matutiry_return_success_with_alias():
    result = runner.invoke(
        app,
        [
            'verify-maturity',
            'https://picpay.github.io',
            '-e',
            'picpay-docs-digital-payments/swagger/checkout.json',
        ],
    )
    "'status': 'success'" in result.stdout


def test_cli_verify_maturity_return_success_without_flag():
    result = runner.invoke(
        app,
        [
            'verify-maturity',
            'https://picpay.github.io/picpay-docs-digital-payments/swagger/checkout.json',
        ],
    )
    "'status': 'success'" in result.stdout


def test_cli_test_rate_return_success_default_arg():
    result = runner.invoke(
        app, ['test-rate', 'https://petstore.swagger.io/v2/pet']
    )
    "'status': 'success'" in result.stdout


def test_cli_test_rate_return_success_with_arg():
    result = runner.invoke(
        app, ['test-rate', 'https://petstore.swagger.io/v2/pet', '50']
    )
    "'status': 'success'" in result.stdout
