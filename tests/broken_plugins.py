"""
We detect plugins that throw an exception on import, so just throw an exception
to mimic a problem.
"""


import click


@click.command()
def something(arg):
    click.echo('passed')


raise Exception('I am a broken plugin.  Send help.')


@click.command()
def after():
    pass
