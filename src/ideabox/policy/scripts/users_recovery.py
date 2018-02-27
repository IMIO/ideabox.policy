# encoding: utf-8
"""
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

import csv

import password_generator
from plone import api
from plone.i18n.normalizer import urlnormalizer
from transaction import commit
from zope.component.hooks import setSite


def add_user(author, mail):
    if len(author) < 3:
        author = urlnormalizer.normalize(mail[0:3].decode('utf8'), locale='fr')
    else:
        author = urlnormalizer.normalize(author.decode('utf8'), locale='fr')
    with api.env.adopt_user(username="admin"):
        if api.user.get(username=author) is None:
            pwd = password_generator.generate(length=12)
            api.user.create(
                username=author,
                email=mail,
                password=pwd,
            )


def data_recovery(filename):
    csv_file = open(filename, 'rb')
    reader = csv.reader(csv_file, delimiter=";")
    reader.next()
    for line in reader:
        author = line[3]
        author_mail = line[4]

        add_user(
            author,
            author_mail
        )


def main(app):
    import argparse
    from Zope2.App import startup

    startup.startup()

    parser = argparse.ArgumentParser()
    parser.add_argument('-c')
    parser.add_argument('csv', help='csv file')
    parser.add_argument('name', help='Name of plone site')
    args = parser.parse_args()

    setSite(app[args.name])

    if args.csv:
        data_recovery(args.csv)
        commit()


if "app" in locals():
    main(app)  # NOQA
