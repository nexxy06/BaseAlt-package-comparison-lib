import click
from alt_lib.client import AltLinuxAPI


@click.group()
def cli():
    pass


@cli.command()
@click.argument("branch")
def get_packages(branch):
    """
    Retrieves binary packages list for specified ALT Linux branch.

    Args:
        branch: Branch name (e.g. 'p11', 'p10', 'sisyphus')

    Returns:
        List of package dictionaries with structure:
        [
            {
                'name': str,      # Package name (e.g. 'bash')
                'version': str,   # Version string (e.g. '5.1.16')
                'arch': str       # Architecture (e.g. 'x86_64')
            },
            ...
        ]
    """
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
    """
    Compares packages between two ALT Linux branches.

    Args:
        branch1: First branch name to compare
        branch2: Second branch name to compare

    Returns:
        Dictionary with comparison results:
        {
            'unique_to_first': set(),
            'unique_to_second': set(),
            'newer_in_first': set()     # Packages where version in branch1
                                        # is newer than in branch2
        }
    """
    api = AltLinuxAPI()
    try:
        result = api.compare_branches(branch1, branch2)
        click.echo(result)
        click.echo(f"Comparison between {branch1} and {branch2}:")
        click.echo(f"Unique to {branch1}: {len(result['unique_to_first'])}")
        click.echo(f"Unique to {branch2}: {len(result['unique_to_second'])}")
        click.echo(f"The packages are newer in {branch1}: \
                   {len(result['newer_in_first'])}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli()
