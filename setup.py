from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='tekquota',
      version='0.1.0',
      description='Script for checking TekSavvy Quota',
      long_description=readme(),
      url='https://github.com/mikeodr/TekSavvyQuota',
      author="Mike O'Driscoll",
      license='GPL2',
      packages=['tekquota'],
      scripts=['bin/tekquota'],
      install_requires=[
              "configobj",
      ],
      zip_safe=False)
