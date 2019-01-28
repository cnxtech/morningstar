# Morningstar API Client

This project provides a client to the Morningsar Web Services endpoints.

## Setup

Install as a dependency using pip:

```
# Not ready yet
pip install morningstar
```
or using pip directly accessing the git repository:

```
pip install git+ssh://git@gitlab.com/aaaccell/morningstar.git
```

Once installed, a configuration file is required within your home folder (~):

```
mkdir -p ~/morningstar-py & touch $_/config.yml
```

The content of the config file can be derived from [config-morningstar.yml.dist](https://gitlab.com/aaaccell/morningstar/blob/master/config-morningstar.yml.dist)

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
