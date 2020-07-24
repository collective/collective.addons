Add A New Release To An Add-On Project
######################################

An owner of an add-on project could add a release to the own project. There is
a link at the top of an add-on project page whilst the owner is logged-in to the
Plone site. Once he clicked on this link he got an edit form to enter the
content of the new release.

.. image:: images/create_addon_release.png

The owner could make alternatively a mouse click on the menu entry 'Add new' in
the menu bar on the left side and choose from the opening sub menu the entry
'Add-On Release' (see the small red arrow in the screenshot above).

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

The Second Register 'Compatibility'
***********************************

This register contains a form field to choose the versions of the program the
release is compatible with. The list of program versions will be created by
the site admin within the 'Add-on Center'. It is possible to choose multiple
program versions for the release compatibility.

.. image:: images/addon_release_form02.png
   :width: 600



The Third Register 'Legal'
**************************

The third register shows the necessary fields for the legal statements about
the release. It starts with the license for the release. It is possible to
check more than one license for a release. This declaration need to be in
accordance with the license declaration inside the add-on release (if there
is one).

.. image:: images/addon_release_form03.png
   :width: 600

There is also a read-only form field which contains the text of the legal
disclaimer that has to be accepted by the add-on release owner. The text of
the legal disclaimer will be set by the site admin inside the 'Add-on Center'.

If the source code is not inside the add-on release (the drop down field is
set to 'No'), it is necessary to fill in the link to the source code in the form
field at the bottom of the register. If such a link will not be submitted the
release owner gets an error message.

The Fourth Register 'Fileupload'
********************************

This register is the place to upload the add-on release file and declare which
platform it is compatible with.

.. image:: images/addon_release_form04.png
   :width: 600

If there are versions of the add-on release for different platforms (e.g. one
for MS Windows and another one for Linux only) this further release files
could be uploaded using the following register.

The list of platforms in the listing below the the upload field will be created
by the site admin inside the 'Add-on Center'. She / he is able to expand this
list at any time if desired.
