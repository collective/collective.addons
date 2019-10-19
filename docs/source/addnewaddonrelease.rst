Add A New Release To An Add-On Project
######################################

A owner of an add-on project could add a release to the own project. There is
a link at the top of a add-on project page whilst the owner is logged-in to the
Plone site. Once he clicked on this link he got an edit form to enter the
content of the new release.

.. image:: images/create_addon_release.png

The owner could make alternatively a mouse click on the menu entry 'Add new' in
the menu bar on the left side and choose from the opening sub menu the entry
'Add-On-Release' (see the small red arrow in the screenshot above).

The form dialog consists of several register. The form fields in the first register
asks for more general information about the release. It's possible to edit and change
the content of the fields later, if there is something missing or there are e.g.
typos, that should be fixed.

The First Register 'Default'
****************************

The new add-on release needs its own release number. This number (up to twelf
chars) will be part of the release title and its URL. The title will be created
from the add-on project title and the release number. This title has to be
unique inside the Plone site. If the release number is already in use, the
editor will get an error message about it.

.. image:: images/addon_release_form01.png
   :width: 600

A new release needs also a summary and could get a full release description with
details about its features. The latter one is optional (only form fields with
a red point behind the title are mandatory).

There is also an optional field to add changelog information, especially if
the add-on release adds some new features or fix some issues.

The field for the email address will be initialized with the email address from
the add-on project the release was added to.

