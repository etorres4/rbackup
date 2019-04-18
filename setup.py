import setuptools

# ========== Constants ==========
PACKAGES = ["rbackup", "rbackup.plugins", "rbackup.struct"]
SCRIPTS = ["bin/backup"]

# ========== Functions ==========
with open("README", "r") as fh:
    long_description = fh.read()

# ========== Package Setup ==========
setuptools.setup(
    name="rbackup",
    version="0.5",
    author="Eric Torres",
    author_email="erictorres4@protonmail.com",
    description="An rsync-based tool for creating backups",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="",
    packages=PACKAGES,
    scripts=SCRIPTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
