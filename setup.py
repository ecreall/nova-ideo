import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'dogpile.cache',
    'ecreall_dace',
    'ecreall_pontus',
    'ecreall_daceui',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_layout',
    'pyramid_mailer',
    'pyramid_tm',
    'requests',
    'deform',
    'substanced',
    'waitress',
    'gunicorn',
    'plone.event',
    'xlrd',
    'html_diff_wrapper',
    'Genshi',
    'beautifulsoup4',
    'pyramid_robot',
    'profilehooks',
    'metadata_parser'
    ]

setup(name='novaideo',
      version='1.0',
      description='The fusion of the best of the suggestion box and collaborative portal.',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        ],
      author='Amen Souissi',
      author_email='amensouissi@ecreall.com',
      url='https://nova-ideo.com',
      keywords='web pyramid substanced',
      license="GPLv3",
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

