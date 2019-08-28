# -*- coding: utf-8 -*-
from collective.addons.addoncenter import IAddonCenter
from plone import api


def notifiyAboutNewVersion(addonproject, event):
    if hasattr(event, 'descriptions') and event.descriptions:
        for d in event.descriptions:
            if hasattr(d, 'interface') and d.interface is IEUpCenter and \
                'available_versions' in d.attributes:
                users = api.user.get_users()
                message = 'We added a new version of the product to the ' \
                          'list.\n Please add this version to your ' \
                          'template project(s), if it is (they ' \
                          'are) compatible with this version.\n\n' \
                          'You could do this on your project(s). Go to ' \
                          'your project and choose the command ' \
                          "'edit' from the menu bar. Go to the section " \
                          "'compatible with versions of the product' " \
                          'and mark the checkbox for the new version of ' \
                          'the product.\n\n' \
                          'Kind regards,\n\n' \
                          'Administration Team'
                for f in users:
                    mailaddress = f.getProperty('email')
                    api.portal.send_email(
                        recipient=mailaddress,
                        sender=api.portal.get_registry_record(
                            'plone.email_from_address'),
                        subject='New Version of the Product Added',
                        body=message,
                    )
