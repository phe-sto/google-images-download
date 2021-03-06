from codecs import open
from os import path

from setuptools import setup, find_packages

__version__ = '0.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='google_images_download',
    version=__version__,
    description="Python Script to download giant dataset of images from 'Google Images'. It is a ready-to-run code! ",
    long_description=long_description,
    url='https://github.com/phe-sto/google-images-download',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='google images dataset creator download save filter color image-search image-dataset image-scrapper image-gallery terminal command-line',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    license="NO LICENSE, FEEL FREE!",
    author='Christohe Brun',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='christophe.brun@papit.fr',
    entry_points={
        'console_scripts': [
            'google-images-download = google_images_download.google_images_download:main'
        ]},

)
