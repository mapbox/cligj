cligj
======

.. image:: https://travis-ci.org/mapbox/cligj.svg
   :target: https://travis-ci.org/mapbox/cligj

.. image:: https://coveralls.io/repos/mapbox/cligj/badge.png
   :target: https://coveralls.io/r/mapbox/cligj

Common arguments and options for GeoJSON processing commands, using Click.

Example
-------

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

On the command line:

.. code-block:: console

    $ features
    {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': '1'}, {'type': 'Feature', 'id': '2'}]}
    $ features --sequence --rs
    ^^{'type': 'Feature', 'id': '1'}
    ^^{'type': 'Feature', 'id': '2'}

