from setuptools import setup

setup(name='ggtracker-client',
      version='0.1',
      description='API client for ggtracker.com',
      author='Travis Thieman',
      author_email='travis.thieman@gmail.com',
      license='BSD License',
      packages=['ggtracker'],
      zip_safe=False,
      install_requires=['requests'])
