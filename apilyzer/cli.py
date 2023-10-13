import asyncio

from rich.console import Console
from typer import Argument, Context, Option, Typer

from apilyzer.verify import (
    analyze_api_maturity,
    check_documentation_json,
    estimate_rate_limit,
)

console = Console()
app = Typer()


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
):
    message = """

Forma de uso: [green]apilyzer [SUBCOMANDO] [ARGUMENTOS] [FLAGS] [/]

Atualmente, existem 3 subcomandos disponíveis para essa aplicação:

- [b]verify-rest[/]: Verifica se uma API REST está documentada com base na URL fornecida e caso esteja, retorna o retorno da API
- [b]verify-maturity[/]: Analisa o nível de maturidade de uma API REST com base no modelo de maturidade de Richardson
- [b]test-rate[/]: Efetua uma quantidade de requisições (100 por padrão) para a API com o objetivo de validar se a API tem um limite para a quantidade de requisições

[b]Mais informações de cada comando:[/]

[green]apilyzer verify-rest --help [/]
[green]apilyzer verify-maturity --help [/]
[green]apilyzer test-rate --help [/]

[b]Exemplos de uso:[/]

[green]apilyzer verify-rest https://petstore.swagger.io -e v2/swagger[/]
[green]apilyzer verify-maturity https://picpay.github.io/picpay-docs-digital-payments/swagger/checkout.json[/]
[green]apilyzer test-rate https://petstore.swagger.io/v2/pet[/]
"""
    if ctx.invoked_subcommand:
        return
    console.print(message)


@app.command()
def verify_rest(
    url: str = Argument(
        'http://127.0.0.1:8000', help='URL of the API to verify'
    ),
    doc_endpoint: str = Option(
        None,
        '--doc-endpoint',
        '-e',
        help='Endpoint of the API documentation. If not provided, we will try to identify it with the base URL alone',
    ),
):
    result = asyncio.run(check_documentation_json(url, doc_endpoint))
    console.print(result)


@app.command()
def verify_maturity(
    url: str = Argument(
        'http://127.0.0.1:8000', help='URL of the API to verify'
    ),
    doc_endpoint: str = Option(
        None,
        '--doc-endpoint',
        '-e',
        help='Endpoint of the API documentation. If not provided, we will try to identify it with the base URL alone',
    ),
):
    result = asyncio.run(analyze_api_maturity(url, doc_endpoint))
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
