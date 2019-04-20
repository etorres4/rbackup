import setuptools
from sphinx.setup_command import BuildDoc

# ========== Constants ==========
PACKAGES = ["rbackup", "rbackup.plugins", "rbackup.struct"]
SCRIPTS = ["bin/backup"]
CMDCLASS = {"build_sphinx": BuildDoc}

# ========== Functions ==========
with open("README.rst", "r") as fh:
    long_description = fh.read()

# ========== Package Setup ==========
setuptools.setup(
    name="rbackup",
    version="0.5.2",
    cmdclass=CMDCLASS,
    author="Eric Torres",
    author_email="erictorres4@protonmail.com",
    description="An rsync-based tool for creating backups",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/etorres4/rbackup",
    packages=PACKAGES,
    scripts=SCRIPTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    command_options={
        "build_sphinx": {
            # "project": ("setup.py", name),
            "version": ("setup.py", "version"),
            "release": ("setup.py", "release"),
            # "source_dir": ("setup.py", "doc"),
        }
    },
)
