import os
import time

from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

def search_packages(console=None) -> list:
    """ Searches PyPi for a list of available packages """
    # TODO: Switch everything over to QProcess (not subprocess.run)
    # TODO: Look to see if using ScraPy is faster than using BeautifulSoup (lxml)

    start_time = time.time()

    URL = "https://pypi.org/simple"

    try:
        source = urlopen(URL)
    except URLError as e:
        error = str(e)
        try:
            console.add_text(error)
        except:
            print(error)

        return []

    # lxml is faster than html.parser
    soup = BeautifulSoup(source, "lxml")

    packages = []

    package_links = soup.find_all('a')

    for package_link in package_links:
        packages.append(package_link.get_text())

    end_time = time.time()
    total_time = str(end_time - start_time)
    try:
        console.add_text("Package List Download Time: " + total_time)
    except:
        print("Package List Download Time: ", total_time)

    return packages


def save_pypi_package_list(console=None):
    """ Save the pypi packagae list locally to improve performance """

    with open("data/pip/pypipackages.txt", mode='w') as f:
        packages_string = ""

        if console:
            packages = search_packages(console)
        else:
            packages = search_packages()

        for package in packages:
            packages_string += package + ","

        f.write(packages_string)


def load_pypi_package_list() -> list:
    """ Loads the saved pypi package list """
    # TODO: Add support for slicing the list
    with open("data/pip/pypipackages.txt") as f:
        packages = f.read().split(",")

    # Use indexing to speed up testing
    # Remove it for the release
    # [120000:130000]
    return packages


def load_installed_package_list() -> list:
    # TODO: Use this method inside of the Uninstall dock
    installed_packages = []

    return installed_packages


def save_installed_package_list():
    pass


def install_package(package_name):
    """ Install a package using PIP

    :param package_name: The name of the package
    :type package_name: str """
    pass