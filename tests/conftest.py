import pytest

from urqse.calibrate.invert import calibrate
from urqse.model.params import Params
from urqse.synthetic import synthetic_state


@pytest.fixture(scope="session")
def data():
    return synthetic_state()


@pytest.fixture(scope="session")
def params():
    return Params()


@pytest.fixture(scope="session")
def cal(data, params):
    return calibrate(data, params)
