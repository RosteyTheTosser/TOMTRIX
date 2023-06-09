"""This module implements the command line interface for tomtrix."""

import asyncio
import logging
import os
import sys
from enum import Enum
from typing import Optional

import typer
from dotenv import load_dotenv
from rich import console, traceback
from rich.logging import RichHandler
from tomtrix import __version__
from verlat import latest_release

load_dotenv( ".env" )

FAKE = bool( os.getenv( "FAKE" ) )
app = typer.Typer( add_completion=False )

con = console.Console()


def topper() :
    print( "tomtrix" )
    version_check()
    print( "\n" )


class Mode( str, Enum ) :
    """tomtrix works in two modes."""

    PAST = "past"
    LIVE = "live"


def verbosity_callback(value: bool) :
    """Set logging level."""
    traceback.install()
    if value :
        level = logging.INFO
    else :
        level = logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                markup=True,
            )
        ],
    )
    topper()
    logging.info( "Verbosity turned on! This is suitable for debugging" )


def version_callback(value: bool) :
    """Show current version and exit."""

    if value :
        con.print( __version__ )
        raise typer.Exit()


def version_check() :
    latver = latest_release( "tomtrix" ).version
    if __version__ != latver :
        con.print(
            f"tomtrix has a newer release {latver} availaible!\
            \nVisit http://https://github.com/RosteyTheTosser/TOMTRIX",
            style="bold yellow",
        )
    else :
        con.print( f"Running latest tomtrix version {__version__}", style="bold green" )


@app.command()
def main(
        mode: Mode = typer.Argument(
            ..., help="Choose the mode in which you want to run tomtrix.", envvar="tomtrix_MODE"
        ),
        verbose: Optional[bool] = typer.Option(  # pylint: disable=unused-argument
            None,
            "--loud",
            "-l",
            callback=verbosity_callback,
            envvar="LOUD",
            help="Increase output verbosity.",
        ),
        version: Optional[bool] = typer.Option(  # pylint: disable=unused-argument
            None,
            "--version",
            "-v",
            callback=version_callback,
            help="Show version and exit.",
        ),
) :
    """
    For updates join telegram channel @rosteythetossers_code

    To run web interface run `tomtrix-web` command.
    """
    if FAKE :
        logging.critical( f"You are running fake with {mode} mode" )
        sys.exit( 1 )

    if mode == Mode.PAST :
        from tomtrix.past import forward_job  # pylint: disable=import-outside-toplevel

        asyncio.run( forward_job() )
    else :
        from tomtrix.live import start_sync  # pylint: disable=import-outside-toplevel

        asyncio.run( start_sync() )

# rosteythetosser 2023
