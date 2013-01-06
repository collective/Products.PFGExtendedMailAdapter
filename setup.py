from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('src', 'Products', 'PFGExtendedMailAdapter', 'docs', 'README.rst') + "\n" +
    read('src', 'Products', 'PFGExtendedMailAdapter', 'docs', 'HISTORY.rst') + "\n" +
    read('src', 'Products', 'PFGExtendedMailAdapter', 'docs', 'CONTRIBUTORS.rst') + "\n" +
    read('src', 'Products', 'PFGExtendedMailAdapter', 'docs', 'CREDITS.rst'))

setup(
    name='Products.PFGExtendedMailAdapter',
    version='2.3',
    description="Adds extended mail adapter to Products.PloneFormGen.",
    long_description=long_description,
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='https://github.com/collective/Products.PFGExtendedMailAdapter',
    license='BSD',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.PloneFormGen',
        'hexagonit.testing',
        'setuptools'],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
