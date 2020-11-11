# -*- coding: utf-8 -*-
"""Installer for the collective.addons package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.addons',
    version='2.4',
    description="Plone add-on to host add-ons / extensions of a software",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Andreas Mantke',
    author_email='maand@gmx.de',
    url='https://github.com/collective/collective.addons',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.addons',
        'Source': 'https://github.com/collective/collective.addons',
        'Tracker': 'https://github.com/collective/collective.addons/issues',
        # 'Documentation':
        # 'https://collective.addons.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7, >=3.6",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'z3c.jbot',
        'plone.api>=1.8.4',
        'plone.restapi',
        'plone.app.dexterity',
        'cioppino.twothumbs',
        'collective.dexteritytextindexer',
        'Products.validation',
        'plone.formwidget.recaptcha',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
            'collective.dexteritytextindexer',
            'Products.validation',
            'cioppino.twothumbs',
            'plone.formwidget.recaptcha',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.addons.locales.update:update_locale
    """,
)
