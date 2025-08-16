import click
from alt_lib.client import AltLinuxAPI


@click.group()
def cli():
    pass


@cli.command()
@click.argument("branch")
def get_packages(branch):
    """Get binary packages list for brach"""
    api = AltLinuxAPI()
    try:
        packages = api.get_binary_packages(branch)
        click.echo(f"Packages in {branch}: {len(packages)}")
        for pkg in packages:
            click.echo(f"{pkg['name']}-{pkg['version']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("branch1")
@click.argument("branch2")
def compare_branches(branch1, branch2):
    """Compares two package versions using lenient parsing rules."""
    api = AltLinuxAPI()
    try:
        result = api.compare_branches(branch1, branch2)
        click.echo(result)
        click.echo(f"Comparison between {branch1} and {branch2}:")
        click.echo(f"Unique to {branch1}: {len(result['unique_to_first'])}")
        click.echo(f"Unique to {branch2}: {len(result['unique_to_second'])}")
        click.echo(f"The packages are newer in {branch1}: {len(result['newer_in_first'])}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli()
