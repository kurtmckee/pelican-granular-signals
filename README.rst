..  This file is part of the pelican-granular-signals plugin.
..  Copyright 2021 Kurt McKee <contactme@kurtmckee.org>
..  Released under the MIT license.

pelican-granular-signals
************************

*Ensure that your Pelican plugin is called at the right time, every time.*

----

Love `Pelican`_ but hate that your finalization plugin isn't always called in the right order?
Don't let your plugin get lost in the shuffle of the ``finalized`` signal!
**pelican-granular-signals** adds new finalization signals
that guarantee your plugin is called at the right time, every time.



New Pelican signals
===================

When **pelican-granular-signals** is installed,
the following signals will be called immediately after the ``finalized`` signal:

*   ``sitemap``
*   ``optimize``
*   ``minify``
*   ``compress``
*   ``deploy``

Each signal will be sent with the same argument that is sent to the ``finalized`` signal.



Connecting to granular signals
==============================

Your plugin must register with `blinker`_ directly.
Here's a complete example:

..  code-block:: python

    import blinker

    import pelican.plugins.granular_signals


    def register():
        # This line is highly recommended so users
        # don't have to update their configurations.
        pelican.plugins.granular_signals.register()

        # Connect your awesome plugin to a granular signal.
        blinker.signal("deploy").connect(deploy_site)


    # -----------------------------------------------------
    # Put your awesome plugin code here.

    import subprocess

    def deploy_site(instance):
        subprocess.run(instance.settings["DEPLOY_COMMAND"])



Helping users out
=================

To make life easier for users, consider taking these two steps:

1.  List **pelican-granular-signals** as a dependency so it will be automatically installed with your plugin.
2.  When Pelican calls your plugin's ``register()`` function, call ``pelican.plugins.granular_signals.register()``.

Pelican 4.5 introduced a new, automatic plugin loading feature
and **pelican-granular-signals** is designed to work with this feature!
Unfortunately, if a user specifies which plugins to load in their configuration file
then automatic plugin loading will be disabled.
It is therefore recommended that you call ``pelican.plugins.granular_signals.register()``
in your plugin's ``register()`` function.

``pelican.plugins.granular_signals.register()`` can be called multiple times without creating any problems.




..  Links
..  =====

..  _Pelican: https://getpelican.com/
..  _blinker: https://github.com/jek/blinker
