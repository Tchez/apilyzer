from pytest import mark
from typer.testing import CliRunner

from apilyzer.cli import app

runner = CliRunner()


def test_cli_returns_success():
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0


def test_cli_verify_rest_return_success():
    result = runner.invoke(
        app, ['verify-rest', 'https://petstore.swagger.io', 'v2/swagger']
    )
    "'status': 'success'" in result.stdout


def test_cli_verify_maturity_return_success():
    result = runner.invoke(
        app,
        [
            'verify-maturity',
            'https://picpay.github.io/picpay-docs-digital-payments/swagger/checkout.json',
        ],
    )
    "'status': 'success'" in result.stdout


def test_cli_test_rate_return_success():
    result = runner.invoke(
        app, ['test-rate', 'https://petstore.swagger.io/v2/pet', '50']
    )
    "'status': 'success'" in result.stdout
