<img src="https://apilyzer.readthedocs.io/en/latest/assets/logo.png" width="400" style="display: block; margin: 20px auto;">


# APIlyzer


[![Documentation Status](https://readthedocs.org/projects/apilyzer/badge/?version=latest)](https://apilyzer.readthedocs.io/en/latest/?badge=latest)
[![CI](https://github.com/tchez/apilyzer/actions/workflows/pipeline.yaml/badge.svg)](https://github.com/tchez/apilyzer/actions/workflows/pipeline.yaml)
[![codecov](https://codecov.io/gh/tchez/apilyzer/branch/main/graph/badge.svg?token=OVQQF4IQY2)](https://codecov.io/gh/tchez/apilyzer)
[![PyPI version](https://badge.fury.io/py/apilyzer.svg)](https://badge.fury.io/py/apilyzer)
[![pt_br doc](https://img.shields.io/badge/pt_br-doc-00a3cc.svg)](https://github.com/Tchez/apilyzer/blob/main/README_PT.md)


## Table of Contents:

- [Description and context](#description-and-context)
- [Documentation](#documentation)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [How to use?](#how-to-use)
- [Dependencies](#dependencies)
- [How to contribute](#how-to-contribute)
- [Team](#team)
- [License](#license)


## Description and context

APIlyzer is a Python library aimed at analyzing the maturity level of REST APIs, following the Richardson maturity model. The goal of this library is to evaluate APIs and generate a report on their maturity level, along with recommendations for improvements so that the API reaches the desired maturity level.
> Note: The library is still in development, so it does not have all the features we want to implement.


## Documentation

The complete documentation, containing all the details of the project, can be accessed at:
[https://apilyzer.readthedocs.io/en/latest/](https://apilyzer.readthedocs.io/en/latest/)

## Prerequisites

Make sure you have Python 3.9 or higher installed on your system before proceeding with the installation.


## Installation Guide

We recommend creating a virtual environment to install the library in an isolated manner. Follow the commands below for installation:


```bash
# Create virtual environment
python -m venv .venv
```	

```bash
# Activate virtual environment
source .venv/bin/activate # Linux
.venv\Scripts\activate # Windows
```

```bash
# Install the library
pip install apilyzer
```

## How to use?

APIlyzer offers a command line interface (CLI) for analyzing REST APIs. To know the available commands, run:

```bash
apilyzer
```

Currently, there are 3 subcommands available for this application:

- `verify-rest`: Checks if a REST API is documented based on the provided URL and if it is, returns the API response.

- `verify-maturity`: Analyzes the maturity level of a REST API based on the Richardson maturity model.

- `test-rate`: Performs a number of requests (100 by default) to the API with the aim of validating whether the API has a limit for the number of requests.

Examples of use:

```bash
apilyzer verify-rest https://petstore.swagger.io -e v2/swagger
```
```bash
apilyzer verify-maturity https://picpay.github.io/picpay-docs-digital-payments/swagger/checkout.json
```
```bash
apilyzer test-rate https://petstore.swagger.io/v2/pet
```

## More information about the CLI

For more information about the CLI, just run the command below:

```bash
apilyzer --help
```

For more information on CLI subcommands, just run the command below:

```bash
apilyzer <subcommand> --help
```


## Dependencies

Main project dependencies:

    # Production
    python = "^3.9"
    httpx = "^0.25.0"
    typer = "^0.9.0"
    rich = "^13.5.2"

    # Development
    pytest = "^7.4.2"
    pytest-cov = "^4.1.0"
    blue = "^0.9.1"
    isort = "^5.12.0"
    taskipy = "^1.12.0"

    # Documentation
    mkdocs-material = "^9.3.1"
    mkdocstrings = "^0.23.0"
    mkdocstrings-python = "^1.7.0"


## How to contribute

There are several ways to contribute to the project, be it with code, tests, documentation, among others. See the project documentation in the [Documentation](#documentation) section to learn more about how to contribute to the project.

## Team

### Author

#### Marco Antônio Martins Porto Netto

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Tchez/)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tchez/)

### Developers

#### Yan Sardinha

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/YanSardinha/)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yan-sardinha/)


## License

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
