from setuptools import find_packages, setup

setup(
    name="Wendy-srv",
    version="0.1",
    packages=find_packages(),
    install_requires=["Flask==2.2.5", "flask_sqlalchemy", "shortuuid", "flask_cors"],
)
