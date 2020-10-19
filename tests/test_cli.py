import os
import os.path
import sys

import click
import pytest

import cligj


def test_files_in(runner):
    @click.command()
    @cligj.files_in_arg
    def cmd(files):
        for f in files:
            click.echo(f)

    result = runner.invoke(cmd, ['1.tif', '2.tif'])
    assert not result.exception
    assert result.output.splitlines() == [
        os.path.join(os.getcwd(), '1.tif'),
        os.path.join(os.getcwd(), '2.tif'),
    ]


def test_files_inout(runner):
    @click.command()
    @cligj.files_inout_arg
    def cmd(files):
        for f in files:
            click.echo(f)

    result = runner.invoke(cmd, ['1.tif', '2.tif'])
    assert not result.exception
    assert result.output.splitlines() == [
        os.path.join(os.getcwd(), '1.tif'),
        os.path.join(os.getcwd(), '2.tif'),
    ]


def test_verbose(runner):
    @click.command()
    @cligj.verbose_opt
    def cmd(verbose):
        click.echo("%s" % verbose)

    result = runner.invoke(cmd, ['-vv'])
    assert not result.exception
    assert result.output.splitlines() == ['2']


def test_quiet(runner):
    @click.command()
    @cligj.quiet_opt
    def cmd(quiet):
        click.echo("%s" % quiet)

    result = runner.invoke(cmd, ['-qq'])
    assert not result.exception
    assert result.output.splitlines() == ['2']


def test_format(runner):
    @click.command()
    @cligj.format_opt
    def cmd(driver):
        click.echo("%s" % driver)

    result = runner.invoke(cmd, ['--driver', 'lol'])
    assert not result.exception
    assert result.output.splitlines() == ['lol']

    result = runner.invoke(cmd, ['--format', 'lol'])
    assert not result.exception
    assert result.output.splitlines() == ['lol']

    result = runner.invoke(cmd, ['-f', 'lol'])
    assert not result.exception
    assert result.output.splitlines() == ['lol']

    result = runner.invoke(cmd)
    assert not result.exception
    assert result.output.splitlines() == ['GTiff']


def test_indent(runner):
    @click.command()
    @cligj.indent_opt
    def cmd(indent):
        click.echo("%s" % indent)

    result = runner.invoke(cmd, ['--indent', '2'])
    assert not result.exception
    assert result.output.splitlines() == ['2']

    result = runner.invoke(cmd)
    assert not result.exception
    assert result.output.splitlines() == ['None']


def test_compact(runner):
    @click.command()
    @cligj.compact_opt
    def cmd(compact):
        click.echo("%s" % compact)

    result = runner.invoke(cmd, ['--compact'])
    assert not result.exception
    assert result.output.splitlines() == ['True']

    result = runner.invoke(cmd, ['--not-compact'])
    assert not result.exception
    assert result.output.splitlines() == ['False']

    result = runner.invoke(cmd)
    assert not result.exception
    assert result.output.splitlines() == ['False']


def test_precision(runner):
    @click.command()
    @cligj.precision_opt
    def cmd(precision):
        click.echo("%s" % precision)

    result = runner.invoke(cmd, ['--precision', '2'])
    assert not result.exception
    assert result.output.splitlines() == ['2']

    result = runner.invoke(cmd)
    assert not result.exception
    assert result.output.splitlines() == ['-1']


def test_projection(runner):
    @click.command()
    @cligj.projection_geographic_opt
    @cligj.projection_projected_opt
    @cligj.projection_mercator_opt
    def cmd(projection):
        click.echo("%s" % projection)

    result = runner.invoke(cmd, ['--geographic'])
    assert not result.exception
    assert result.output.splitlines() == ['geographic']

    result = runner.invoke(cmd, ['--projected'])
    assert not result.exception
    assert result.output.splitlines() == ['projected']

    result = runner.invoke(cmd, ['--mercator'])
    assert not result.exception
    assert result.output.splitlines() == ['mercator']

    result = runner.invoke(cmd)
    assert not result.exception
    assert result.output.splitlines() == ['geographic']


@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize(
    ("opt", "val"),
    [
        ("--sequence", True),
        ("--no-sequence", False),
        (None, cligj.__version__.startswith("1.0")),
    ],
)
def test_sequence(runner, opt, val):
    """True becomes the default in 1.0"""
    @click.command()
    @cligj.sequence_opt
    def cmd(sequence):
        click.echo(str(sequence))

    result = runner.invoke(cmd, [opt] if opt is not None else [])
    assert not result.exception
    assert result.output.splitlines() == [str(val)]


@pytest.mark.skipif(sys.version_info < (3,), reason="Requires Python 3")
@pytest.mark.xfail(cligj.__version__.startswith("1.0"), reason="No warning in 1.0")
def test_sequence_warns(runner):
    """Warn about --sequence until 1.0"""
    @click.command()
    @cligj.sequence_opt
    def cmd(sequence):
        click.echo(str(sequence))

    with pytest.warns(FutureWarning):
        result = runner.invoke(cmd, ["--sequence"])


@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize(("opt", "val"), [("--rs", True), (None, False)])
def test_sequence_rs(runner, opt, val):
    @click.command()
    @cligj.sequence_opt
    @cligj.use_rs_opt
    def cmd(sequence, use_rs):
        click.echo(str(sequence))
        click.echo(str(use_rs))

    result = runner.invoke(cmd, ["--sequence"] + ([opt] if opt is not None else []))
    assert not result.exception
    assert result.output.splitlines() == ["True", str(val)]


@pytest.mark.parametrize(
    ("opt", "val"),
    [("--collection", "collection"), ("--feature", "feature"), ("--bbox", "bbox")],
)
def test_geojson_type(runner, opt, val):
    @click.command()
    @cligj.geojson_type_collection_opt(True)
    @cligj.geojson_type_feature_opt(False)
    @cligj.geojson_type_bbox_opt(False)
    def cmd(geojson_type):
        click.echo(str(geojson_type))

    result = runner.invoke(cmd, [opt])
    assert not result.exception
    assert result.output.splitlines() == [val]
