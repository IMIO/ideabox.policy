# -*- coding: utf-8 -*-
"""Installer for the ideabox.policy package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='ideabox.policy',
    version='1.0a1',
    description="IdeaBox",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Martin Peeters',
    author_email='martin.peeters@affinitic.be',
    url='https://pypi.python.org/pypi/ideabox.policy',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['ideabox'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'plone.api',
        'Products.GenericSetup>=1.8.2',
        'setuptools',
        'z3c.jbot',
        'plone.app.dexterity',
        'plone.app.referenceablebehavior',
        'plone.app.relationfield',
        'plone.app.lockingbehavior',
        'collective.z3cform.select2',
        'plone.api',
        'plone.dexterity',
        'plone.app.contenttypes',
        'password-generator',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
