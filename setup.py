from setuptools import setup, find_packages


setup(
    name='amigo-invisible',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['jinja2'],
)
