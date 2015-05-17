cligj
======

.. image:: https://travis-ci.org/mapbox/cligj.svg
   :target: https://travis-ci.org/mapbox/cligj

.. image:: https://coveralls.io/repos/mapbox/cligj/badge.png?branch=master
   :target: https://coveralls.io/r/mapbox/cligj?branch=master

Common arguments and options for GeoJSON processing commands, using Click.

Example
-------

Here's an example of a command that writes out GeoJSON features as a collection
or, optionally, a sequence of individual features. Since most software that
reads and writes GeoJSON expects a text containing a single feature collection,
that's the default, and a LF-delimited sequence of texts containing one GeoJSON
feature each is a feature that is turned on using the ``--sequence`` option.
To write sequences of feature texts that conform to the `JSON Text Sequences
proposed standard
<http://tools.ietf.org/html/draft-ietf-json-text-sequence-13>`__ (and might
contain pretty-printed JSON) with the ASCII Record Separator (0x1e) as
a delimiter, use the ``--rs`` option

.. code-block:: python

    import click
    import cligj
    import json

    @click.command()
    @cligj.sequence_opt
    @cligj.use_rs_opt
    def features(sequence, use_rs):
        features = [
            {'type': 'Feature', 'id': '1'}, {'type': 'Feature', 'id': '2'}]
        if sequence:
            for feature in features:
                if use_rs:
                    click.echo(b'\x1e', nl=False)
                click.echo(json.dumps(feature))
        else:
            click.echo(json.dumps(
                {'type': 'FeatureCollection', 'features': features}))

On the command line it works like this.

.. code-block:: console

    $ features
    {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': '1'}, {'type': 'Feature', 'id': '2'}]}

    $ features --sequence
    {'type': 'Feature', 'id': '1'}
    {'type': 'Feature', 'id': '2'}

    $ features --sequence --rs
    ^^{'type': 'Feature', 'id': '1'}
    ^^{'type': 'Feature', 'id': '2'}

In this example, ``^^`` represents 0x1e.


Plugins
-------

``cligj`` can also facilitate loading external `click-based <http://click.pocoo.org/4/>`_
plugins via `setuptools entry points <https://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins>`_.
The ``cligj.plugins`` module contains a special ``group()`` decorator that behaves exactly like
``click.group()`` except that it offers the opportunity load plugins and attach them to the
group as it is istantiated.

.. code-block:: python

    from pkg_resources import iter_entry_points

    import cligj.plugins
    import click

    @cligj.plugins.group(plugins=iter_entry_points('module.entry_points'))
    def cli():

        """A CLI application."""

        pass

    @cli.command()
    @click.argument('arg')
    def printer(arg):

        """Print arg."""

        click.echo(arg)

    @cli.group(plugins=iter_entry_points('other_module.more_plugins'))
    def plugins():

        """A sub-group that contains plugins from a different module."""
        pass
