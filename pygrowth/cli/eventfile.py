#!/usr/bin/env python

"""
CLI for eventfile module
"""

import click
import pygrowth.eventfile
import pygrowth.counthistory


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


@cli.command(help="Extract count history")
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("time_bin_sec", type=float)
@click.argument("output_file_path", type=click.Path())
@click.option("--time-axis", type=click.Choice(["absolute", "relative"]),
              help="Time axis mode (relative to the origin or absolute unix time")
@click.option("--time-origin", type=float, help="Time origin in unix time")
@click.option("--energy-range-kev", nargs=2, type=float, help="Lower and upper energy in keV")
@click.option("--time-range", nargs=2, type=float, help="Lower and upper unix time")
@click.option("--channel", type=int, help="Channel number to be extracted")
@click.option("--duration-before-origin-sec", type=float, help="Included duration before time origin in sec")
@click.option("--duration-after-origin-sec", type=float, help="Included duration before time origin in sec")
def extract_counthistory(
        file_path, time_bin_sec, output_file_path, time_axis="absolute", time_origin=None, energy_range_kev=None,
        time_range=None, channel=None, duration_before_origin_sec=None, duration_after_origin_sec=None):

    eventfile = pygrowth.eventfile.open(file_path)

    options = {
        "time_axis": time_axis,
        "time_origin": time_origin,
        "channel": channel,
        "energy_range_kev": energy_range_kev,
        "duration_before_origin_sec": duration_before_origin_sec,
        "duration_after_origin_sec": duration_after_origin_sec,
    }

    extractor = pygrowth.counthistory.CountHistoryExtractor()
    counthistory = extractor.extract(eventfile, time_bin_sec, options)
    counthistory.write(output_file_path)


def main():
    cli()


if __name__ == "__main__":
    main()
