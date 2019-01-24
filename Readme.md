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

The content of the config file can be derived from [config.yml.dist](https://gitlab.com/aaaccell/morningstar/blob/master/config.yml.dist)

## Usage

```python
from morningstar.morningstar_client import MorningstarClient
```
