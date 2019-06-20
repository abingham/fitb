====
fitb
====

Practical configuration system.

With `fitb`, you specify a collection of "configuration options" that your program/library/whatever needs. `fitb` then
helps you construct configuration objects and merge them together.

A *configuration object* is simply a `dict`, so `fitb` is helping you build dicts. A *configuration option* specifies a
path into the dict - that is, a sequence of keys into the dict and subdicts - along with a description of the option and
a default value.

Quick start
===========

The first thing you do with `fitb` is define a collection of config options:

.. code-block:: python

    options = [(('my-app', 'screen'), fitb.Option('width', 'Width of screen', 100)), 
               (('my-app', 'screen'), fitb.Option('height', 'Height of screen', 200))]

Each entry in the list specifies a prefix path and the option itself. From this we can build a 
default config option:

.. code-block:: python

    config = fitb.build_default_config(options)
    
This gives us an object like this:

.. code-block:: python

    {'my-app': {}, 'screen': {'width': 100, 'height': 200}}

with which can do things like this:

.. code-block:: python

    print(config['my-app']['screen']['width']

or work with subconfigs:

.. code-block:: python

    screen_config = config['my-app']['screen']
    print(screen_config['width'])

You can also merge configs together, putting entries from one config into another, possibly overwriting exiting options.
That looks like this:

.. code-block:: python

    fitb.merge(dest=config, src={'my-app': {'screen': {'width': 400}}})

    # The `dest` config has been updated
    assert config['my-app']['screen']['width'] == 400

This ability to `merge` is useful because you can do things like:

  1. Create a default config
  2. Load user configs from files (e.g. TOML, ini, or whatever)
  3. Merge user configs into the default config.
