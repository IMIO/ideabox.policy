# encoding: utf-8
"""
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

import csv
import os

from plone import api
from plone.i18n.normalizer import idnormalizer
from transaction import commit
from zope.component.hooks import setSite
from ideabox.policy.utils import token_type_recorevery, token_category_recorvery
from cioppino.twothumbs import rate


def add_project(portal,
                project_id,
                title,
                project_type,
                category,
                project_body,
                image_source,
                project_author,
                project_like,
                project_unlike):
    if 'projects' in portal:
        container = portal['projects']
        with api.env.adopt_user(username='admin'):
            api.user.grant_roles(username=project_author,
                                 roles=['Contributor', ]
                                 )
            with api.env.adopt_user(username=project_author):
                project = api.content.create(
                    type='Project',
                    title=title,
                    project_type=project_type,
                    category=category,
                    body=u'<br>'.join(project_body.decode('utf8').splitlines()),
                    container=container,
                )
                file_path = os.path.join(image_source, project_id + '.jpg')
                if os.path.isfile(file_path):
                    add_image_from_file(project, project_id + '.jpg', image_source)

        rate.setupAnnotations(project)
        if project_like:
            for x in range(0, int(project_like)):
                rate.loveIt(project, 'userimportp' + str(x))
        if project_unlike:
            for x in range(0, int(project_unlike)):
                rate.hateIt(project, 'userimportn' + str(x))

        with api.env.adopt_user(username='admin'):
            api.user.revoke_roles(username=project_author,
                                  roles=['Contributor', ]
                                  )


def add_image_from_file(container, file_name, source):
    file_path = os.path.join(source, file_name)
    if not container.hasObject(file_name):
        # with deterity image
        from plone.namedfile.file import NamedBlobImage
        named_blob_image = NamedBlobImage(
            data=open(file_path, 'r').read(),
            filename=unicode(file_name)
        )
        image = api.content.create(type='Image',
                                   title=file_name,
                                   image=named_blob_image,
                                   container=container,
                                   language='fr')
        image.setTitle(file_name)
        image.reindexObject()


def data_recovery(filename, image, portal):
    csv_file = open(filename, 'rb')
    reader = csv.reader(csv_file, delimiter=";")
    reader.next()
    for line in reader:
        project_id = line[0]
        project_title = line[2]
        project_type = line[1]
        project_body = line[18]
        project_category = line[5]
        project_author = line[3]
        project_mail = line[4]
        project_like = line[15]
        project_unlike = line[16]

        project_categorys = project_category.decode('utf8').split(";")[:-1]

        token_type = token_type_recorevery(project_type)
        token_categorys = token_category_recorvery(project_categorys)

        if len(project_author) < 3:
            project_author = idnormalizer.normalize(project_mail[0:3].decode('utf8'))
        else:
            project_author = idnormalizer.normalize(project_author.decode('utf8'))

        add_project(
            portal,
            project_id,
            project_title,
            token_type,
            token_categorys,
            project_body,
            image,
            project_author,
            project_like,
            project_unlike
        )
        print project_title


def main(app):
    import argparse
    from Zope2.App import startup

    startup.startup()

    parser = argparse.ArgumentParser()
    parser.add_argument('-c')
    parser.add_argument('csv', help='csv file')
    parser.add_argument('img', help='localisation of pictures')
    parser.add_argument('name', help='Name of plone site')
    args = parser.parse_args()

    setSite(app[args.name])
    portal = app[args.name]

    if args.csv and args.img:
        data_recovery(args.csv, args.img, portal)
        commit()


if "app" in locals():
    main(app)  # NOQA
