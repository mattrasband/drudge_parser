from distutils.core import setup


setup(name='drudge_parser',
      version='2.1',
      description='Naive parser for the Drudge Report',
      author='Matt Rasband',
      author_email='matt.rasband@gmail.com',
      maintainer='Matt Rasband',
      maintainer_email='matt.rasband@gmail.com',
      license='MIT',
      url='https://github.com/mrasband/drudge_parser',
      download_url='https://github.com/mrasband/drudge_parser/archive/v2.1.tar.gz',
      keywords=['parsing', 'webscraping', 'drudge', 'drudgereport'],
      py_modules=['drudge_parser'],
      classifiers=[
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Development Status :: 4 - Beta',
      ],
      install_requires=[])
