import click

from app import crud
from app.api.deps import get_db


@click.group()
def cli():
    pass


@click.command()
def refresh_domain_salts():
    db = next(get_db())
    crud.domain.refresh_domain_salts(db)


cli.add_command(refresh_domain_salts)

if __name__ == "__main__":
    cli()
