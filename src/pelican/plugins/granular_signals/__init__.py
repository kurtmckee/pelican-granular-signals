# This file is part of the pelican-granular-signals plugin.
# Copyright 2021 Kurt McKee <contactme@kurtmckee.org>
# Released under the MIT license.

import functools
from typing import Any, Callable, List, Tuple

import blinker
import pelican


signal_names: Tuple[str, ...] = (
    "sitemap",
    "optimize",
    "minify",
    "compress",
    "deploy",
)


REGISTERED: bool = False


def register():
    """Add additional signals to Pelican.

    To help ensure that site finalization plugins can be called in
    the correct order, the ``finalized`` signal is wrapped so that
    additional signals can be sent.
    """

    global REGISTERED
    if REGISTERED:
        return

    # Create new signals.
    for signal_name in signal_names:
        blinker.signal(signal_name)

    # Create a wrapper for the ``finalized`` signal.
    def augment_finalized(original_send: Callable) -> Callable:
        @functools.wraps(original_send)
        def wrapper(sender):
            results: List[Tuple[Callable, Any]] = original_send(sender)
            for signal_name in signal_names:
                signal: blinker.base.NamedSignal = blinker.signal(signal_name)
                results.extend(signal.send(sender))
            return results

        return wrapper

    # Wrap Pelican's ``finalized`` signal.
    pelican.signals.finalized.send = augment_finalized(pelican.signals.finalized.send)

    REGISTERED = True
