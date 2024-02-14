# This file is part of the pelican-granular-signals plugin.
# Copyright 2021-2024 Kurt McKee <contactme@kurtmckee.org>
# Released under the MIT license.

from __future__ import annotations

import functools
import typing

import blinker
import pelican

signal_names: tuple[str, ...] = (
    "sitemap",
    "optimize",
    "minify",
    "compress",
    "deploy",
)


REGISTERED: bool = False


# mypy wants `typing.Callable`, below, to have type arguments.
# blinker itself doesn't do this, so this mypy error is disabled.
# mypy: disable-error-code="type-arg"


def register() -> None:
    """Add additional signals to Pelican.

    To help ensure that site finalization plugins can be called in
    the correct order, the ``finalized`` signal is wrapped so that
    additional signals can be sent.
    """

    global REGISTERED
    if REGISTERED:
        return

    # Create new signals.
    for signal_name_ in signal_names:
        blinker.signal(signal_name_)

    # Create a wrapper for the ``finalized`` signal.
    def augment_finalized(original_send: typing.Callable) -> typing.Callable:
        @functools.wraps(original_send)
        def wrapper(sender: typing.Any) -> list[tuple[typing.Callable, typing.Any]]:
            results: list[tuple[typing.Callable, typing.Any]] = original_send(sender)
            for signal_name in signal_names:
                signal: blinker.base.NamedSignal = blinker.signal(signal_name)
                results.extend(signal.send(sender))
            return results

        return wrapper

    # Wrap Pelican's ``finalized`` signal.
    pelican.signals.finalized.send = augment_finalized(pelican.signals.finalized.send)

    REGISTERED = True
