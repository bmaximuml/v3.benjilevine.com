from setuptools import setup, find_packages

setup(
    name='benjilevine.com',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'datetime',
        'Flask',
        'Flask-SQLAlchemy',
        'mysql-connector-python',
        'WTForms'
    ],
    author='Benji Levine',
    author_email='benji@benjilevine.com',
    url='https://github.com/benjilev08/v3.benjilevine.com'
)
