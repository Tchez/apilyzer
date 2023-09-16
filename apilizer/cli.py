import asyncio

from rich.console import Console
from typer import Argument, Typer

from apilizer.verify import check_swagger

console = Console()
app = Typer()


@app.command()
def verify_swagger(
    url: str = Argument(
        'http://127.0.0.1:8000', help='URL of the API to verify.'
    ),
):
    result = asyncio.run(check_swagger(url))
    console.print(result)
