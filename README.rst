cligj
======

.. image:: https://travis-ci.org/mapbox/cligj.svg
   :target: https://travis-ci.org/mapbox/cligj

.. image:: https://coveralls.io/repos/mapbox/cligj/badge.png?branch=master
   :target: https://coveralls.io/r/mapbox/cligj?branch=master

Common arguments and options for GeoJSON processing commands, using Click.

TODO what it does and who it is for

Arguments
---------
TODO

Options
--------
TODO

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
    @cligj.features_in_arg
    @cligj.sequence_opt
    @cligj.use_rs_opt
    def pass_features(features, sequence, use_rs):
        if sequence:
            for feature in features:
                if use_rs:
                    click.echo(b'\x1e', nl=False)
                click.echo(json.dumps(feature))
        else:
            click.echo(json.dumps(
                {'type': 'FeatureCollection', 'features': list(features)}))

On the command line it works like this.

.. code-block:: console

    $ cat data.geojson
    {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': '1'}, {'type': 'Feature', 'id': '2'}]}

    $ pass_features data.geojson
    {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': '1'}, {'type': 'Feature', 'id': '2'}]}

    $ cat data.geojson | pass_features
    {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': '1'}, {'type': 'Feature', 'id': '2'}]}

    $ cat data.geojson | pass_features --sequence
    {'type': 'Feature', 'id': '1'}
    {'type': 'Feature', 'id': '2'}

    $ cat data.geojson | pass_features --sequence --rs
    ^^{'type': 'Feature', 'id': '1'}
    ^^{'type': 'Feature', 'id': '2'}

In this example, ``^^`` represents 0x1e.


Plugins
-------

.. warning::
   The cligj.plugins module is deprecated and will be removed at version 1.0.
   Use `click-plugins <https://github.com/click-contrib/click-plugins>`_
   instead.
