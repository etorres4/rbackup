"""
.. author:: Eric Torres
.. module:: rbackup.package_managers.pacman
    :synopsis: Implementation class for the Pacman package manager.
"""
from rbackup.package_managers.packagemanager import PackageManager


class Pacman(PackageManager):
    def __init__(self):
        super().__init__("/var/cache/pacman", "/var/lib/pacman", ["pacman", "-Qqe"])
