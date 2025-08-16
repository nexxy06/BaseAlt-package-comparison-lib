import requests
from distutils.version import LooseVersion
import re


class AltLinuxAPI:

    def __init__(self, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout

    def get_binary_packages(self, branch: str):
        """Get binary packages for brach"""
        url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            packages = [
                {
                    "name": pkg["name"],
                    "version": pkg['version'],  # не учитываю epoch и release
                    "arch": pkg["arch"]
                }
                for pkg in data["packages"]
            ]
            return packages

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
            return LooseVersion(re.sub(r'[a-zA-Zа-яА-Я]', '', v1)) \
                   > LooseVersion(re.sub(r'[a-zA-Zа-яА-Я]', '', v2))

    def compare_branches(self, branch1: str, branch2: str):
        """Package comparison between two branches"""
        packages1 = self.get_binary_packages(branch1)
        packages2 = self.get_binary_packages(branch2)

        ver1 = {pkg["name"]: pkg["version"] for pkg in packages1}
        ver2 = {pkg["name"]: pkg["version"] for pkg in packages2}

        # Названия общих пакетов
        common_packages = set(ver1.keys()) & set(ver2.keys())

        newer_in_first = {
            name for name in common_packages
            if self.compare_loose_versions(ver1[name], ver2[name])
        }
        return {
            "unique_to_first": set(ver1.keys()) - set(ver2.keys()),
            "unique_to_second": set(ver2.keys()) - set(ver1.keys()),
            "newer_in_first": newer_in_first
        }


class AltLinuxAPIError(Exception):
    pass


# if __name__ == "__main__":
#     api = AltLinuxAPI()

    # packages = api.get_binary_packages("p11")
    # for pkg in packages[:5]:
    #     print(f"{pkg['name']} {pkg['version']}")

    # compare = api.compare_branches("p11", "p10")
    # print(compare)
