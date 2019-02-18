# Morningstar API Client ![build](https://travis-ci.com/aaaccell/morningstar.svg?branch=master)

This project provides a client to the Morningsar Web Services endpoints.

## Setup

Install as a dependency using pip:

```
pip install morningstar
```
or install from source:

```
git clone git@github.com:aaaccell/morningstar.git
cd morningstar
python setup.py install
```

Once installed, a configuration file (`config-morningstar.yml` or `.config-morningstar.yml`) is required within your home folder (~). The content can be derived from [config-morningstar.yml.dist](/config-morningstar.yml.dist):

```
cp config-morningstar.yml.dist ~/.config-morningstar.yml
```

## Usage

```python
from morningstar.morningstar_client import MorningstarClient
client = MorningstarClient()
```

The most recommended way to use this module is to instantiate `MorningstarClient` directly, and if necessary extend funcationality using inheritance: `class MyMorningstarClient(MorningstarClient)`.

```
client.get_instrument_prices(instrument='28.10.F00000JQA9', start_date='01-01-2019', end_date='02-01-2019')
```

Alternatively, the underlying provider can be accessed using the client instance and therefore provides the full scope of the Morningstar web service API:

```python
client.provider.search({'isin': "CH0038863350"})
```
