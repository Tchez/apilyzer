from pytest import mark
from typer.testing import CliRunner

from apilyzer.cli import app

runner = CliRunner()


def test_cli_returns_success():
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0


@mark.parametrize('command', ['maturity', 'verify-rest'])
def test_cli_subcommands_return_success(command):
    result = runner.invoke(app, [command])
    assert result.exit_code == 0
