from setuptools import setup

setup(
    name="macDetec",
    version="0.0.1",
    author="Matthias Niedermaier, Thomas Hanka, Sven Plaga, Alexander von Bodisco, Dominik Merli",
    author_email="mattias.niedermaier@hs-augsburg.de, andreas.seiler@hs-augsburg.de, thomas.hanka@hs-augsburg.de, dominik.merli@hs-augsburg.de",
    description=(
        "Efficient Passiv Network Monitoring Tool for MAC Based Detection and Classification"),
    license="Linux",
    keywords="network monitoring, mac address",
    url="https://www.hs-augsburg.de",
    packages=['tests'],
    install_requires=[
        'Click',
        'requests',
        'dpkt',
        'pcapy',
        'coloredlogs'
    ],
    entry_points='''
        [console_scripts]
        macDetec=macDetec:cli
    ''',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: GPL GPLv3",
    ],
)

