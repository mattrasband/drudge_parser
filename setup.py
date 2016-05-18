from distutils.core import setup


setup(name='drudge_parser',
      version='1.0',
      description='Naive parser for the Drudge Report',
      author='Matt Rasband',
      author_email='matt.rasband@gmail.com',
      url='https://github.com/mrasband/drudge_parser',
      packages=['drudge_parser'],
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Development Status :: 3 - Alpha',
      ],
      install_requires=[
          'beautifulsoup4',
          'html5lib'
      ])
