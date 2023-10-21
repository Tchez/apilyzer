<img src="https://apilyzer.readthedocs.io/en/latest/assets/logo.png" width="400" style="display: block; margin: 20px auto;">


# APIlyzer


[![Documentation Status](https://readthedocs.org/projects/apilyzer/badge/?version=latest)](https://apilyzer.readthedocs.io/en/latest/?badge=latest)
[![CI](https://github.com/tchez/apilyzer/actions/workflows/pipeline.yaml/badge.svg)](https://github.com/tchez/apilyzer/actions/workflows/pipeline.yaml)
[![codecov](https://codecov.io/gh/tchez/apilyzer/branch/main/graph/badge.svg?token=OVQQF4IQY2)](https://codecov.io/gh/tchez/apilyzer)
[![PyPI version](https://badge.fury.io/py/apilyzer.svg)](https://badge.fury.io/py/apilyzer)

## Tabela de conteúdos:

- [Descrição e contexto](#descrição-e-contexto)
- [Documentação](#documentação)
- [Pré-requisitos](#pré-requisitos)
- [Guia de instalação](#guia-de-instalação)
- [Como usar?](#como-usar)
- [Dependências](#dependências)
- [Como contribuir](#como-contribuir)
- [Equipe](#equipe)
- [Licença](#licença)


## Descrição e contexto

APIlyzer é uma biblioteca Python destinada a analisar o nível de maturidade de APIs REST, seguindo o modelo de maturidade de Richardson. O objetivo desta biblioteca é avaliar APIs e gerar um relatório sobre o seu nível de maturidade, juntamente com recomendações de melhorias para que a API atinja o nível de maturidade desejado.
> Observação: A biblioteca ainda está em desenvolvimento, portanto, não possui todas as funcionalidades que queremos implementar.


## Documentação

A documentação completa, contendo todos os detalhes do projeto, pode ser acessada em:
[https://apilyzer.readthedocs.io/en/latest/](https://apilyzer.readthedocs.io/en/latest/)

## Pré-requisitos

Certifique-se de ter o Python 3.9 ou superior instalado em seu sistema antes de prosseguir com a instalação.


## Guia de instalação

Recomendamos a criação de um ambiente virtual para instalar a biblioteca de forma isolada. Siga os comandos abaixo para instalação:


```bash
# Criar ambiente virtual
python -m venv .venv
```	

```bash
# Ativar ambiente virtual
source .venv/bin/activate # Linux
.venv\Scripts\activate # Windows
```

```bash
# Instalar a biblioteca
pip install apilyzer
```

## Como usar?

APIlyzer oferece uma interface de linha de comando (CLI) para análise de APIs REST. Para conhecer os comandos disponíveis, execute:

```bash
apilyzer
```

Atualmente, existem 3 subcomandos disponíveis para esta aplicação:

- `verify-rest`: Verifica se uma API REST está documentada com base na URL fornecida e caso esteja, retorna o retorno da API.

- `verify-maturity`: Analisa o nível de maturidade de uma API REST com base no modelo de maturidade de Richardson.

- `test-rate`: Efetua uma quantidade de requisições (100 por padrão) para a API com o objetivo de validar se a API tem um limite para a quantidade de requisições.

Exemplos de uso:

```bash
apilyzer verify-rest https://petstore.swagger.io -e v2/swagger
```
```bash
apilyzer verify-maturity https://picpay.github.io/picpay-docs-digital-payments/swagger/checkout.json
```
```bash
apilyzer test-rate https://petstore.swagger.io/v2/pet
```

## Mais informações sobre o CLI

Para mais informações sobre o CLI, basta executar o comando abaixo:

```bash
apilyzer --help
```

Para mais informações sobre os subcomandos do CLI, basta executar o comando abaixo:

```bash
apilyzer <subcomando> --help
```


## Dependências

Principais dependências do projeto:

    # Produção
    python = "^3.9"
    httpx = "^0.25.0"
    typer = "^0.9.0"
    rich = "^13.5.2"

    # Desenvolvimento
    pytest = "^7.4.2"
    pytest-cov = "^4.1.0"
    blue = "^0.9.1"
    isort = "^5.12.0"
    taskipy = "^1.12.0"

    # Documentação
    mkdocs-material = "^9.3.1"
    mkdocstrings = "^0.23.0"
    mkdocstrings-python = "^1.7.0"


## Como contribuir

Existem várias formas de contribuir com o projeto, seja com código, testes, documentação, entre outros. Consulte a documentação do projeto na seção [Documentação](#documentação) para saber mais sobre como contribuir para o projeto.

## Equipe

### Autor

#### Marco Antônio Martins Porto Netto

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Tchez/)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tchez/)

### Desenvolvedores

#### Yan Sardinha

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/YanSardinha/)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yan-sardinha/)


## Licença

MIT License

Copyright (c) 2023 Marco Antônio Martins Porto Netto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
