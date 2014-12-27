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
