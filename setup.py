from setuptools import setup, find_packages

setup(
    name="chronicler",
    version="1.0.0",
    description="Game tracker for Warmachine",
    url="http://github.com/elwinar/chronicler",
    author="Romain Baugue",
    author_email="romain.baugue@elwinar.com",
    license="The Unlicense",
    zip_safe=False,
    install_requires=[
        'docopt>=0.6',
        'hjson>=1.5',
        'jsonschema>=2.5',
        'tabulate>=0.7',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ssc = chronicler.__main__:main',
        ],
    },
)
