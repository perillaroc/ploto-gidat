import click

from ploto.scheduler.rabbitmq.consumer.consumer import (
    load_config,
    run_blocking_connection
)

@click.command()
@click.option("-c", "--config-file", help="config file path")
def cli(config_file):
    config = load_config(config_file)
    run_blocking_connection(config)


if __name__ == "__main__":
    cli()
