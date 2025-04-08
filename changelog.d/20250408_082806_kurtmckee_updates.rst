Development
-----------

*   ``blinker`` is now an explicit dependency.

    No lower bound is enforced, however, because it is included with Pelican.
    Adding it allows other plugins to be tested more easily without requiring Pelican itself.

*   Migrate to PEP 621 metadata in ``pyproject.toml``.
*   Use ``scriv`` to manage the CHANGELOG.
*   Include a ``py.typed`` marker.
