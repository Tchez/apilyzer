<h1 align="center"> APIlizer </h1>
<p align="center"><img width=300px src="./docs/assets/temp_logo.png"></p>

[![Documentation Status](https://readthedocs.org/projects/apilizer/badge/?version=latest)](https://apilizer.readthedocs.io/en/latest/?badge=latest)
[![CI](https://github.com/tchez/apilizer/actions/workflows/pipeline.yaml/badge.svg)](https://github.com/tchez/apilizer/actions/workflows/pipeline.yaml)
[![codecov](https://codecov.io/gh/tchez/apilizer/branch/main/graph/badge.svg?token=OVQQF4IQY2)](https://codecov.io/gh/tchez/apilizer)
[![PyPI version](https://badge.fury.io/py/apilizer.svg)](https://badge.fury.io/py/apilizer)

## Tabela de conteúdos:

- [Descrição e contexto](#descrição-e-contexto)
- [Documentação](#documentação)
- [Guia de instalação](#guia-de-instalação)
- [Como usar?](#como-usar)
- [Dependências](#dependências)
- [Como contribuir](#como-contribuir)
- [Autores](#autores)
- [Licença](#licença)


## Descrição e contexto

O APIlizer é uma biblioteca python que tem como objetivo analizar o nível de maturidade de APIs REST, seguindo o modelo de maturidade de Richardson. O objetivo da biblioteca é ser capaz de analizar APIs e gerar um relatório com o nível de maturidade da mesma, além de recomendações de melhorias para que a API atinja o nível de maturidade desejado.
> Observação: A biblioteca ainda está em desenvolvimento, portanto, não possui todas as funcionalidades que queremos implementar.


## Documentação

Acesse a documentação contendo todos os detalhes do projeto em: 
[https://apilizer.readthedocs.io/en/latest/](https://apilizer.readthedocs.io/en/latest/)

 
## Guia de instalação

Para instalar a biblioteca, basta executar o comando abaixo:

```bash
pip install apilizer
```

## Como usar?

A biblioteca oferece uma CLI para que você possa analizar APIs REST via linha de comando. Para isso, basta executar o comando abaixo:

```bash
apilizer analyze <url>
```

Onde `<url>` é a url da API que você deseja analizar, que caso não seja informada, será utilizada a url `http://localhost:8000`. Por exemplo:

```bash
apilizer analyze https://myapi.com
```

O comando acima irá analizar a URL `https://myapi.com` e gerar um relatório com o nível de maturidade da mesma, além de recomendações de melhorias para que a API atinja o nível de maturidade desejado.
> Lembrando que a biblioteca ainda está em desenvolvimento, portanto, no momento a biblioteca analiza apenas se a API possui swagger e se os endpoints estão documentados corretamente.


## Mais informações sobre o CLI

Para mais informações sobre o CLI, basta executar o comando abaixo:

```bash
apilizer --help
```

Para mais informações sobre os subcomandos do CLI, basta executar o comando abaixo:

```bash
apilizer <subcomando> --help
```


## Dependências

Principais dependências do projeto:

    # Produção
    httpx = "^0.25.0"
    typer = "^0.9.0"
    rich = "^13.5.2"

    # Desenvolvimento
    pytest = "^7.4.2"
    pytest-cov = "^4.1.0"
    blue = "^0.9.1"
    isort = "^5.12.0"
    taskipy = "^1.12.0"
    respx = "^0.20.2"

    # Documentação
    mkdocs-material = "^9.3.1"
    mkdocstrings = "^0.23.0"
    mkdocstrings-python = "^1.7.0"


## Como contribuir

Há várias formas de contribuir com o projeto, com código, testes, documentação, etc.
Acesse a documentação do projeto na seção [Documentação](#documentação) para saber mais sobre como contribuir com o projeto.


## Autores

### Coordenador

#### Marco Antônio Martins Porto Netto

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Tchez)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tchez/)

### Desenvolvedores

#### Wendhel Valeriano De Almeida Cruz

[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/wendhelvaleriano/)

#### Yan Sardinha

[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yan-sardinha/)


## Licença


The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-----------------

[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)