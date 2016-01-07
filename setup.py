import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'dogpile.cache',
    'dace',
    'pontus',
    'daceui',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_layout',
    'pyramid_mailer',
    'pyramid_tm',
    'deform',
    'substanced',
    'waitress',
    'gunicorn',
    'xlrd',
    'diff-match-patch',
    'Genshi',
    'html5lib',
    'html2text',
    'beautifulsoup4',
    'pyramid_robot',
    'profilehooks'
    ]

setup(name='novaideo',
      version='0.0',
      description='novaideo',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons substanced',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="novaideo",
      message_extractors={
          'novaideo': [
              ('**.py', 'python', None), # babel extractor supports plurals
              ('**.pt', 'chameleon', None),
          ],
      },
      extras_require = dict(
          test=['pyramid_robot'],
      ),
      entry_points="""\
      [paste.app_factory]
      main = novaideo:main
      """,
      )

