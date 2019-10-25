from setuptools import setup

setup(
    name='benjilevine.com',
    version='0.0.1.dev',
    long_description=__doc__,
    packages=['benjilevine.com'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'datetime',
        'Flask'
    ]
)
