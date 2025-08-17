import requests
from distutils.version import LooseVersion
import re
import json


class AltLinuxAPI:

    def __init__(self, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout

    def get_binary_packages(self, branch: str):
        """
        Retrieves binary packages list for specified ALT Linux branch.

        Args:
            branch: Branch name (e.g. 'p11', 'p10', 'sisyphus')

        Returns:
            {
                'x86_64': {
                    'bash': '5.1.16',
                    'curl': '7.76.1'
                },
                'aarch64': {
                    'bash': '5.1.16',
                    'python3': '3.9.5'
                }
            }
        """
        BASE_URL = "https://rdb.altlinux.org/api/"
        url = f"{BASE_URL}export/branch_binary_packages/{branch}"

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            arch_packages = {}
            for pkg in data["packages"]:
                arch = pkg["arch"]
                if arch not in arch_packages:
                    arch_packages[arch] = {}
                arch_packages[arch][pkg["name"]] = pkg["version"]

            return arch_packages

        except requests.RequestException as e:
            raise AltLinuxAPIError(f"API request failed: {e}")
        except (KeyError, ValueError) as e:
            raise AltLinuxAPIError(f"Invalid API response format: {e}")

    def compare_loose_versions(self, v1: str, v2: str):
        """Compares two package versions using lenient parsing rules.

        Returns:
            True if v1 is considered greater than v2, False otherwise

        Note:
            Uses LooseVersion comparison which handles common version formats
            Falls back to numeric-only comparison if standard comparison fails
        """
        try:
            return LooseVersion(v1) > LooseVersion(v2)
        except Exception:
            return LooseVersion(re.sub(r"[a-zA-Zа-яА-Я]", "", v1)) > \
                LooseVersion(re.sub(r"[a-zA-Zа-яА-Я]", "", v2))

    def compare_branches(self, branch1: str, branch2: str):
        """
        Compares packages between two ALT Linux branches.

        Args:
            branch1: First branch name to compare
            branch2: Second branch name to compare

        Returns:
            Dictionary with comparison results by architecture:
            {
                'x86_64': {
                    'unique_to_first': ['package1', 'package2'],
                    'unique_to_second': ['package3'],
                    'newer_in_first': ['bash', 'curl']
                },
                'aarch64': {
                    ...
                }
            }
        """
        pkgs1 = self.get_binary_packages(branch1)
        pkgs2 = self.get_binary_packages(branch2)

        all_archs = set(pkgs1.keys()) | set(pkgs2.keys())

        result = {}

        for arch in all_archs:
            # Receive packages for the current arch from both branches
            arch_pkgs1 = pkgs1.get(arch, {})
            arch_pkgs2 = pkgs2.get(arch, {})

            unique_first = set(arch_pkgs1.keys()) - set(arch_pkgs2.keys())
            unique_second = set(arch_pkgs2.keys()) - set(arch_pkgs1.keys())

            newer_in_first = []
            for pkg in set(arch_pkgs1.keys()) & set(arch_pkgs2.keys()):
                if self.compare_loose_versions(arch_pkgs1[pkg],
                                               arch_pkgs2[pkg]):
                    newer_in_first.append(pkg)

            result[arch] = {
                "unique_to_first": sorted(unique_first),
                "unique_to_second": sorted(unique_second),
                "newer_in_first": newer_in_first,
            }

        return json.dumps(result, indent=2, ensure_ascii=False)


class AltLinuxAPIError(Exception):
    pass


# if __name__ == "__main__":
#     api = AltLinuxAPI()

#     packages = api.get_binary_packages("p11")
#     for arch in packages.keys():
#         print(packages[arch])

#     compare = api.compare_branches("p11", "p10")
#     print(compare)
