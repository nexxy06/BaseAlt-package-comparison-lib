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

    Args:\n
        branch: Branch name (e.g. 'p11', 'p10', 'sisyphus')\n

    Returns:\n
        {\n
            'x86_64': {\n
                'bash': '5.1.16',\n
                'curl': '7.76.1'\n
            },\n
            'aarch64': {\n
                'bash': '5.1.16',\n
                'python3': '3.9.5'\n
            }\n
        }\n
    """
    api = AltLinuxAPI()
    try:
        packages = api.get_binary_packages("p11")
        for arch in packages.keys():
            click.echo(packages[arch])
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("branch1")
@click.argument("branch2")
def compare_branches(branch1, branch2):
    """
    Compares packages between two ALT Linux branches.

    Args:\n
        branch1: First branch name to compare\n
        branch2: Second branch name to compare

    Returns:\n
        Dictionary with comparison results by architecture:
        {\n
            'x86_64': {\n
                'unique_to_first': ['package1', 'package2'],\n
                'unique_to_second': ['package3'],\n
                'newer_in_first': ['bash', 'curl']\n
            },\n
            'aarch64': {
                ...\n
            }\n
        }\n
    """
    api = AltLinuxAPI()
    try:
        result = api.compare_branches(branch1, branch2)
        click.echo(result)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli()
