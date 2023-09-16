![logo temporária](assets/temp_logo.png){ width="300" .center }
# Analisador de API

## Como usar?

Você pode analisar sua API via linha de comando. Para isso, basta executar o seguinte comando:

```bash
poetry run verify
```

Retorno esperado:

```json
{
    'status': '...',
    'message': '...'
}
```

Caso queira analisar uma API que não esteja rodando em `localhost`, basta passar a URL como parâmetro:

```bash
poetry run verify <url>
```

Retorno esperado:

```json
{
    'status': '...',
    'message': '...'
}
```

## mais informações sobre o CLI

Para mais informações sobre o CLI, basta usar a flag `--help`:

```bash
poetry run verify --help
```
