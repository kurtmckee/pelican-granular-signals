# This file is part of the pelican-granular-signals plugin.
# Copyright 2021-2022 Kurt McKee <contactme@kurtmckee.org>
# Released under the MIT license.

import pathlib
import time
from unittest.mock import Mock, patch

import pytest

import pelican.plugins.granular_signals as gs


def finalized_send(*args, **kwargs):
    return [(finalized_send, True)]


@pytest.fixture
def pelican_signals():
    signals_module = Mock()
    signals_module.finalized.send = finalized_send
    with patch("pelican.plugins.granular_signals.pelican.signals", signals_module):
        yield signals_module


@pytest.fixture
def blinker():
    blinker_module = Mock()
    blinker_signal = Mock()
    blinker_signal.return_value = blinker_signal
    blinker_signal.send.return_value = [("signal", True)]
    blinker_module.signal = blinker_signal

    with patch("pelican.plugins.granular_signals.blinker", blinker_module):
        yield blinker_module


@pytest.fixture
def registered():
    with patch("pelican.plugins.granular_signals.REGISTERED", True):
        yield


@pytest.fixture
def unregistered():
    with patch("pelican.plugins.granular_signals.REGISTERED", False):
        yield


def test_registered_flag(pelican_signals, blinker, registered):
    """Verify the REGISTERED flag prevents double registration."""

    gs.register()

    assert gs.REGISTERED is True
    assert blinker.signal.call_count == 0
    assert pelican_signals.finalized.send is finalized_send


def test_finalized_send_override(pelican_signals, blinker, unregistered):
    """Verify the plugin overrides the ``finalized.send()`` method."""

    gs.register()

    assert gs.REGISTERED is True
    assert blinker.signal.call_count == len(gs.signal_names)
    assert pelican_signals.finalized.send is not finalized_send


def test_finalized_send(pelican_signals, blinker, unregistered):
    """Verify the plugin successfully sends additional signals."""

    gs.register()

    assert gs.REGISTERED is True
    assert blinker.signal.call_count == len(gs.signal_names)
    assert not isinstance(pelican_signals.finalized.send, Mock)

    signal_mock = blinker.signal("deploy")
    assert signal_mock.send

    result = pelican_signals.finalized.send("bogus")

    message = "``finalized.send()`` must be called before new signals"
    assert result[0] == (finalized_send, True), message

    assert len(result) == len(gs.signal_names) + 1


root = pathlib.Path(__file__).parent.parent
copyrighted_files = [
    *list(root.glob("*.ini")),
    *list(root.glob("*.rst")),
    *list(root.glob("*.txt")),
    *list((root / "src").rglob("*.py")),
    *list((root / "tests").rglob("*.py")),
]


@pytest.mark.parametrize("path", copyrighted_files)
def test_copyrights(path):
    with path.open("r", encoding="utf8") as file:
        assert f"2021-{time.gmtime().tm_year}" in file.read(
            100
        ), f"{path.name} has an incorrect copyright date"
