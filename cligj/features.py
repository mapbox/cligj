from itertools import chain
import json
import re

import click


def normalize_feature_inputs(ctx, param, features_like):
    """ Click callback which accepts the following values:
    * Path to file(s), each containing single FeatureCollection or Feature
    * Coordinate pair(s) of the form "[0, 0]" or "0, 0" or "0 0"
    * if not specified or '-', process STDIN stream containing
        - line-delimited features
        - ASCII Record Separator (0x1e) delimited features
        - FeatureCollection or Feature object
    and yields GeoJSON Features.
    """
    if len(features_like) == 0:
        features_like = ('-',)

    for flike in features_like:
        try:
            # It's a file/stream with GeoJSON
            src = iter(click.open_file(flike, mode='r'))
            for feature in iter_features(src):
                yield feature
        except IOError:
            # It's a coordinate string
            coords = list(coords_from_query(flike))
            feature = {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'Point',
                    'coordinates': coords}}
            yield feature


def iter_features(geojsonfile, func=None):
    """Extract GeoJSON features from a GeoJSON file object.

    Given a file-like object containing a single GeoJSON feature
    collection text or a sequence of GeoJSON, iter_features() iterates
    over lines of the file and yields GeoJSON features.

    Parameters
    ----------
    geojsonfile: a file-like object
        The geojsonfile implements the iterator protocol and yields
        lines of JSON text.
    func: function, optional
        A function that will be applied to each extracted feature. It
        takes a feature object and returns a replacement feature.
    """
    func = func or (lambda x: x)
    first_line = next(geojsonfile)

    # If input is RS-delimited JSON sequence.
    if first_line.startswith(u'\x1e'):
        text_buffer = first_line.strip(u'\x1e')
        for line in geojsonfile:
            if line.startswith(u'\x1e'):
                if text_buffer:
                    yield func(json.loads(text_buffer))
                text_buffer = line.strip(u'\x1e')
            else:
                text_buffer += line
        else:
            yield func(json.loads(text_buffer))
    else:
        try:
            feat = json.loads(first_line)
            assert feat['type'] == 'Feature'
            yield func(feat)
            for line in geojsonfile:
                yield func(json.loads(line))
        except (TypeError, KeyError, AssertionError, ValueError):
            text = "".join(chain([first_line], geojsonfile))
            feats = json.loads(text)
            if feats['type'] == 'Feature':
                yield func(feats)
            elif feats['type'] == 'FeatureCollection':
                for feat in feats['features']:
                    yield func(feat)


def iter_query(query):
    """Accept a filename, stream, or string.
    Returns an iterator over lines of the query."""
    try:
        itr = click.open_file(query).readlines()
    except IOError:
        itr = [query]
    return itr


def coords_from_query(query):
    """Transform a query line into a (lng, lat) pair of coordinates."""
    try:
        coords = json.loads(query)
    except ValueError:
        vals = re.split(r"\,*\s*", query.strip())
        coords = [float(v) for v in vals]
    return tuple(coords[:2])


def normalize_feature_objects(feature_objs):
    """Takes an iterable of GeoJSON-like Feature mappings or
    an iterable of objects with a geo interface and
    normalizes it to the former."""
    for obj in feature_objs:
        if hasattr(obj, "__geo_interface__") and \
           'type' in obj.__geo_interface__.keys() and \
           obj.__geo_interface__['type'] == 'Feature':
            yield obj.__geo_interface__
        elif isinstance(obj, dict) and 'type' in obj and \
                obj['type'] == 'Feature':
            yield obj
        else:
            raise ValueError("Did not recognize object {0}"
                             "as GeoJSON Feature".format(obj))
