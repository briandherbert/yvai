from setuptools import setup, find_packages

setup(
    name='yvai',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'Flask-Cors',
        'openai'
    ],
)