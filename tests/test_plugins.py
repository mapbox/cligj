"""Unittests for ``cligj.plugins``."""


from pkg_resources import EntryPoint
from pkg_resources import iter_entry_points
from pkg_resources import working_set

import click

import cligj.plugins


# Create a few CLI commands for testing
@click.command()
@click.argument('arg')
def printer(arg):

    """
    Printit!
    """

    click.echo('passed')

@click.command()
@click.argument('arg')
def square(arg):

    """
    Square it!
    """

    click.echo('passed')


# Manually register plugins in an entry point and put broken plugins in a
# different entry point.

# The `DistStub()` class gets around an exception that is raised when
# `entry_point.load()` is called.  By default `load()` has `requires=True`
# which calls `dist.requires()` and the `cligj.plugins.group()` decorator
# doesn't allow us to change this.  Because we are manually registering these
# plugins the `dist` attribute is `None` so we can just create a stub that
# always returns an empty list since we don't have any requirements.
class DistStub(object):
    def requires(self, *args):
        return []

working_set.by_key['cligj']._ep_map = {
    'cligj.test_plugins': {
        'printer': EntryPoint.parse(
            'printer=tests.test_plugins:printer', dist=DistStub()),
        'square': EntryPoint.parse(
            'square=tests.test_plugins:square', dist=DistStub())
    },
    'cligj.broken_plugins': {
        'before': EntryPoint.parse(
            'before=tests.broken_plugins:before', dist=DistStub()),
        'after': EntryPoint.parse(
            'after=tests.broken_plugins:after', dist=DistStub()),
        'do_not_exist': EntryPoint.parse(
            'do_not_exist=tests.broken_plugins:do_not_exist', dist=DistStub())
    }
}


def test_register_and_run(runner):

    @cligj.plugins.group(plugins=iter_entry_points('cligj.test_plugins'))
    def cli():
        pass

    # Execute without any calling a sub-command to get the help message
    result = runner.invoke(cli)
    assert result.exit_code is 0

    # Execute each subcommand
    for ep in iter_entry_points('cligj.test_plugins'):
        cmd_result = runner.invoke(cli, [ep.name, 'something'])
        assert cmd_result.exit_code is 0
        assert cmd_result.output.strip() == 'passed'
