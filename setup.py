from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name = 'taggable',
    version = '0.2.0',
    description = 'Taggable types for annotating data',
    long_description = readme(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Text Processing',
    ],
    keywords = 'tag annotate enrich text data NLP',
    url = 'https://github.com/ville-k/taggable',
    author = 'Ville Kallioniemi',
    author_email = 'ville.kallioniemi@gmail.com',
    license = 'MIT',
    packages = ['taggable'],
    tests_require = ['nose'],
    test_suite = 'nose.collector',
    include_package_data = True
)

