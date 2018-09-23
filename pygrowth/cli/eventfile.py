#!/usr/bin/env python

"""
CLI for eventfile module
"""

import click
import pygrowth.common.eventfile


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


@cli.command(help="Dump header attributes of an event file")
@click.argument("file_path", type=click.Path(exists=True))
def show(file_path):
    eventfile = pygrowth.common.eventfile.open(file_path)
    click.echo(eventfile)


def main():
    cli()


if __name__ == "__main__":
    main()
