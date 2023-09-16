from typer.testing import CliRunner

from apilizer.cli import app

runner = CliRunner()


def test_cli_returns_success():
    result = runner.invoke(app)
    assert result.exit_code == 0


def test_verify_swagger_command_returns_status_and_message():
    result = runner.invoke(app)

    assert 'status' in result.stdout
    assert 'message' in result.stdout
