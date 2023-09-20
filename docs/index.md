![logo temporária](assets/temp_logo.jpg){ width="300" .center }
# Analisador de API
> Documentação em construção

## Como usar?

Você pode analisar sua API via linha de comando. Para isso, basta executar o seguinte comando:

```bash
apilyzer
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
apilyzer <url>
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
apilyzer --help
```
