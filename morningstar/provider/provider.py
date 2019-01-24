from abc import ABC, abstractmethod


class Provider(ABC):

    @abstractmethod
    def __init__(self, config):
        """
        Args:
            config (dict): dictionary containing configuration parameters
        """
        self.config = config

    @abstractmethod
    def search(self, params: dict):
        """Search endpoint

        Args:
            params (dict): e.g. {"isin": "US46625H1005"}

        Returns:

        """
        pass

    @abstractmethod
    def index(self, params: dict):
        """Index endpoint

        Args:
            params (dict): e.g. {"isin": "US46625H1005"}

        Returns:

        """
        pass

    @abstractmethod
    def index_ts(self, params: dict):
        """IndexTS endpoint

        Args:
            params (dict): e.g. {"isin": "US46625H1005"}

        Returns:

        """
        pass
