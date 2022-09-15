from setuptools import setup, find_packages

setup(
    name='Telegram (un)subscriber',
    version='0.0.1',
    packages=find_packages(include=['tg_subscriber', 'tg_subscriber.*'])
)
