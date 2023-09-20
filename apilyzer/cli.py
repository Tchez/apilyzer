import asyncio

from rich.console import Console
from typer import Argument, Context, Typer

from apilyzer.verify import check_swagger_rest, is_rest_api

console = Console()
app = Typer()


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
):
    message = """

Forma de uso: [green]apilyzer [SUBCOMANDO] [ARGUMENTOS][/]

Atualmente, existem apenas 2 subcomandos disponíveis para essa aplicação:

- [b]is-rest[/]: Verifica se uma URL pertece a uma API REST
- [b]verify-rest[/]: Verifica se uma API REST está documentada com base na URL fornecida

[b]Exemplos de uso:[/]

[green]apilyzer is-rest [/]
[green]apilyzer verify-rest [/]

[green]apilyzer verify-rest https://petstore.swagger.io/v2[/]


[b]Para mais informações: [yellow]apilyzer --help[/]
"""
    if ctx.invoked_subcommand:
        return
    console.print(message)


@app.command()
def is_rest(
    url: str = Argument(
        'http://127.0.0.1:8000', help='URL of the API to verify.'
    ),
):
    result = asyncio.run(is_rest_api(url))
    console.print(result)


@app.command()
def verify_rest(
    url: str = Argument(
        'http://127.0.0.1:8000', help='URL of the API to verify.'
    ),
):
    result = asyncio.run(check_swagger_rest(url))
    console.print(result)


if __name__ == '__main__':
    app()
