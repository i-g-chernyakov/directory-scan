# -*- coding: utf-8 -*-

# import asyncio
# import logging
# import typing

# import anyconfig
import click


@click.command()
@click.option('-p', '--period',
              type=int,
              default=60,
              help='Period of scanning')
@click.option('-d', '--depth',
              type=int,
              help='Recursive depth to scan')
@click.option('-i', '--ignored',
              type=str,
              help='Ignored file extensions')
@click.option('-l', '--log-level',
              type=str,
              help='Log level')
@click.option('-u', '--database-url',
              type=str,
              help='Database url')
@click.option('-c', '--config',
              type=click.Path(exists=True),
              help='Configuration file')
@click.argument('directory',
                type=click.Path(exists=True))
def cli(period: int = 60,
        depth: int = None,
        ignored: str = None,
        log_level: str = 'INFO',
        database_url: str = None,
        config: str = None,
        directory: str = "") -> None:
    """ The directory scanner

    Scan periodically directory and get changes.
    """

    pass


if __name__ == "__main__":
    cli()
