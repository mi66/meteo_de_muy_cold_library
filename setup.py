from setuptools import setup, find_packages

setup(
    name='meteo_de_muy_cold',
    version='0.1',
    packages=find_packages(),
    description='pull meteo data',
    long_description='from the antarctic',
    author='mi66',
    author_email='mi66@none.none',
    url='n/a',
    install_requires=[
        'requests>=2.32.2',
        'pytz>=2024.1',
    ],
    include_package_data=True,
    package_data={
        # Include any .yaml files found within any package under the "meteo" package.
        'meteo_de_muy_cold': ['configurable_params/*.yaml'],
    },
)