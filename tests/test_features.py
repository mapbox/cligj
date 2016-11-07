import json
import sys

import pytest

from cligj.features import \
    coords_from_query, iter_query, to_feature, \
    normalize_feature_inputs, normalize_feature_objects


def test_iter_query_string():
    assert iter_query("lolwut") == ["lolwut"]


def test_iter_query_file(tmpdir):
    filename = str(tmpdir.join('test.txt'))
    with open(filename, 'w') as f:
        f.write("lolwut")
    assert iter_query(filename) == ["lolwut"]


def test_coords_from_query_json():
    assert coords_from_query("[-100, 40]") == (-100, 40)


def test_coords_from_query_csv():
    assert coords_from_query("-100, 40") == (-100, 40)


def test_coords_from_query_ws():
    assert coords_from_query("-100 40") == (-100, 40)


@pytest.fixture
def expected_features():
    with open("tests/twopoints.geojson") as src:
        fc = json.loads(src.read())
        return fc['features']


def _geoms(features):
    geoms = []
    for feature in features:
        geoms.append(feature['geometry'])
    return geoms


def test_featurecollection_file(expected_features):
    features = normalize_feature_inputs(
        None, 'features', ["tests/twopoints.geojson"])
    assert _geoms(features) == _geoms(expected_features)


def test_featurecollection_pretty_file(expected_features):
    features = normalize_feature_inputs(
        None, 'features', ["tests/twopoints-pretty.json"])
    assert _geoms(features) == _geoms(expected_features)


def test_featurecollection_stdin(expected_features):
    sys.stdin = open("tests/twopoints.geojson", 'r')
    features = normalize_feature_inputs(None, 'features', [])
    assert _geoms(features) == _geoms(expected_features)


def test_featuresequence(expected_features):
    features = normalize_feature_inputs(
        None, 'features', ["tests/twopoints_seq.txt"])
    assert _geoms(features) == _geoms(expected_features)

# TODO test path to sequence files fail

def test_featuresequence_stdin(expected_features):
    sys.stdin = open("tests/twopoints_seq.txt", 'r')
    features = normalize_feature_inputs(None, 'features', [])
    assert _geoms(features) == _geoms(expected_features)


def test_singlefeature(expected_features):
    features = normalize_feature_inputs(
        None, 'features', ["tests/onepoint.geojson"])
    assert _geoms(features) == _geoms([expected_features[0]])


def test_singlefeature_stdin(expected_features):
    sys.stdin = open("tests/onepoint.geojson", 'r')
    features = normalize_feature_inputs(None, 'features', [])
    assert _geoms(features) == _geoms([expected_features[0]])


def test_featuresequencers(expected_features):
    features = normalize_feature_inputs(
        None, 'features', ["tests/twopoints_seqrs.txt"])
    assert _geoms(features) == _geoms(expected_features)


def test_featuresequencers_stdin(expected_features):
    sys.stdin = open("tests/twopoints_seqrs.txt", 'r')
    features = normalize_feature_inputs(None, 'features', [])
    assert _geoms(features) == _geoms(expected_features)


def test_coordarrays(expected_features):
    inputs = ["[-122.7282, 45.5801]", "[-121.3153, 44.0582]"]
    features = normalize_feature_inputs(None, 'features', inputs)
    assert _geoms(features) == _geoms(expected_features)


def test_coordpairs_comma(expected_features):
    inputs = ["-122.7282, 45.5801", "-121.3153, 44.0582"]
    features = normalize_feature_inputs(None, 'features', inputs)
    assert _geoms(features) == _geoms(expected_features)


def test_coordpairs_space(expected_features):
    inputs = ["-122.7282 45.5801", "-121.3153 44.0582"]
    features = normalize_feature_inputs(None, 'features', inputs)
    assert _geoms(features) == _geoms(expected_features)


def test_geometrysequence(expected_features):
    features = normalize_feature_inputs(None, 'features', ["tests/twopoints_geom_seq.txt"])
    assert _geoms(features) == _geoms(expected_features)


def test_geometrysequencers(expected_features):
    features = normalize_feature_inputs(None, 'features', ["tests/twopoints_geom_seqrs.txt"])
    assert _geoms(features) == _geoms(expected_features)


def test_geometrypretty(expected_features):
    features = normalize_feature_inputs(None, 'features', ["tests/point_pretty_geom.txt"])
    assert _geoms(features)[0] == _geoms(expected_features)[0]

class MockGeo(object):
    def __init__(self, feature):
        self.__geo_interface__ = feature


def test_normalize_feature_objects(expected_features):
    objs = [MockGeo(f) for f in expected_features]
    assert expected_features == list(normalize_feature_objects(objs))
    assert expected_features == list(normalize_feature_objects(expected_features))


def test_normalize_feature_objects_bad(expected_features):
    objs = [MockGeo(f) for f in expected_features]
    objs.append(MockGeo(dict()))
    with pytest.raises(ValueError):
        list(normalize_feature_objects(objs))

def test_to_feature(expected_features):
    geom = expected_features[0]['geometry']
    feat = {'type': 'Feature', 'properties': {}, 'geometry': geom}
    assert to_feature(feat) == to_feature(geom)
    with pytest.raises(ValueError):
        assert to_feature({'type': 'foo'})
