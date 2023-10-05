import asyncio

from rich.console import Console
from typer import Argument, Context, Typer

from apilyzer.verify import (
    _is_json_rest_api,
    analyze_api_maturity,
    check_swagger_rest,
    estimate_rate_limit,
)

console = Console()
app = Typer()


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
):
    message = """

Forma de uso: [green]apilyzer [SUBCOMANDO] [ARGUMENTOS][/]

Atualmente, existem 2 subcomandos disponíveis para essa aplicação:

- [b]verify-rest[/]: Verifica se uma API REST está documentada com base na URL fornecida e caso esteja, retorna o retorno da API
- [b]maturity[/]: Analisa o nível de maturidade de uma API REST com base no modelo de maturidade de Richardson
- [b]test-rate[/]: Efetua uma quantidade de requisições (100 por padrão) para a API com o objetivo de validar se a API tem um limite para a quantidade de requisições

[b]Exemplos de uso:[/]

[green]apilyzer verify-rest [/]
[green]apilyzer maturity [/]
[green]apilyzer test-rate [/]


[green]apilyzer verify-rest https://petstore.swagger.io v2/swagger[/]
[green]apilyzer maturity https://picpay.github.io/picpay-docs-digital-payments/swagger/checkout.json[/]
[green]apilyzer test-rate https://petstore.swagger.io/v2/pet[/]


[b]Para mais informações: [yellow]apilyzer --help[/]
"""
    if ctx.invoked_subcommand:
        return
    console.print(message)


@app.command()
def verify_rest(
    url: str = Argument(
        'http://127.0.0.1:8000', help='URL of the API to verify'
    ),
    endpoint: str = Argument(
        None,
        help='Endpoint of the API to verify. If not provided, we will try to identify it with the base URL alone',
    ),
):
    result = asyncio.run(check_swagger_rest(url, endpoint))
    console.print(result)


@app.command()
def maturity(
    url: str = Argument(
        'http://127.0.0.1:8000', help='URL of the API to verify'
    ),
):
    result = asyncio.run(analyze_api_maturity(url))
    console.print(result)


@app.command()
def test_rate(
    url: str = Argument(
        'http://127.0.0.1:8000', help='URL of the API to verify.'
    ),
    rate: int = Argument(
        '50', help='Number of requests to test if the API is able to resist.'
    ),
):
    result = asyncio.run(estimate_rate_limit(url, rate))
    console.print(result)


if __name__ == '__main__':
    app()
