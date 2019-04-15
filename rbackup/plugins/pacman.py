"""
.. moduleauthor:: Eric Torres
.. module:: rbackup.plugins.pacman
    :synopsis: Implementation class for the Pacman package manager.
"""
from rbackup.plugins.packagemanager import PackageManager


class Pacman(PackageManager):
    def __init__(self):
        super().__init__("/var/cache/pacman", "/var/lib/pacman", ("pacman", "-Qqe"))
