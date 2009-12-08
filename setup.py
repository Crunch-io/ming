from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='Ming',
      version=version,
      description="Bringing order to Mongo since 2009",
      classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      long_description='''Database mapping layer for MongoDB on Python. Includes schema enforcement and some facilities for schema migration.
''',
      keywords='mongo, pymongo',
      author='Rick Copeland',
      author_email='rick@geek.net',
      url='http://merciless.sourceforge.net',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
        "mock >= 0.6.0",
        "FormEncode >= 1.2.2",
        "pymongo >= 1.1.2",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite='ming.tests',
      )
