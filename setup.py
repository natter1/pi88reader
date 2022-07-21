import pathlib
from setuptools import setup


# The directory containing this file
root_path = pathlib.Path(__file__).parent
long_description = (root_path / "README.rst").read_text()


setup(
    name='pi88reader',
    version='0.0.1a08',
    packages=['pi88reader'],
    url='https://github.com/natter1/pi88reader.git',
    license='MIT',
    author='Nathanael Jöhrmann',
    author_email='',
    description='Tool to read/process PI88 measurement files',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    install_requires=['matplotlib', 'numpy', 'scipy'],
)