import setuptools

setuptools.setup(
    name='furniture-analyze',
    version='0.0.0',
    description='Example package for a CLI',
    author='You',
    author_email='you@example.com',
    packages=['furniture_analyze'],
    entry_points={
        'console_scripts': ['furniture-analyze=furniture_analyze.cli:main'],
    },
    install_requires=[
        'requests',
    ],
)