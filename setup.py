from setuptools import setup, find_packages

setup(
    name="Wendy-srv",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Flask==2.2.5",
        "flask_sqlalchemy"
    ],
)
