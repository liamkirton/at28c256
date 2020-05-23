from distutils.core import setup


setup(name='at28c256',
      version='1.0',
      description='AT28C256 Programmer',
      author='Liam Kirton',
      author_email='liam@int3.ws',
      packages=['at28c256'],
      install_requires=[
          'pyserial',
      ])
