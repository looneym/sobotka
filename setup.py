from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='sobotka',

    version='0.0.7',

    description='Manage development environments on AWS',

    url='https://github.com/looneym/sobotka',

    author='Micheal Looney',
    author_email='looneymicheal+sobotka@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='aws ec2 docker docker-compose devtools development environments',

    packages=find_packages(exclude=[ 'docs']),

    install_requires=[
        'python_hosts', 
        'watchdog', 
        'peewee', 
        'pytz', 
        'boto3', 
        'stormssh', 
        'Fabric', 
        'storm', 
        'PyYAML'
    ],

    entry_points={
        'console_scripts': [
            'sobotka = sobotka.cli:main',
        ],
    },
)
