from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def get_agent(self):
        pass

    @abstractmethod
    def build_agent(self):
        pass

    @abstractmethod
    def pre_train(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def post_train(self):
        pass

    @abstractmethod
    def pre_test(self):
        pass

    @abstractmethod
    def test_model(self):
        pass

    @abstractmethod
    def post_test(self):
        pass
