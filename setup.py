from setuptools import setup, find_packages

setup(
    name='benjilevine.com',
    version='0.1.dev',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'datetime',
        'Flask'
    ]
)
