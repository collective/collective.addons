.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://travis-ci.org/collective/collective.addons.svg?branch=master
    :target: https://travis-ci.org/collective/collective.addons

=================
collective.addons
=================

Features
--------


- A add-on center with listing and display of template projects respectively to their rating,
  a search form and a listing of the latest projects.
- The add-on center edit form contains fields to set the title of the center and the name of
  the add-ons, add a description of the center, set a choice of categories, platforms, lizenses
  and versions of the product (for which the add-ons are used). There are also fields to set the
  allowed file extensions of the add-on files and the image files (e.g. screenshots, logos).
- Inside the add-on center contributors could create add-on projects. The edit form of the
  project contains fields to choose the categories.
- The contributor could add releases and linked releases to the add-on project.
- The release contains fields to upload files.
- The linked release provide fields for links to the release files.
- Both, release and linked release, contains fields to choose the product version, platform
  and licenses.
- The add-on send message once a new project was added. It push a message too, once a project
  was submitted for publication. It send an email to the project contact address for every
  change in the workflow status of the project.
- The add-on informs the contributor via email about new releases or linked releases,
  once they were added to his project(s).
- The user could send a message to the author of an add-on via a mail. The mail form uses a
  recaptcha widget. The contact data of the author of the aa-on will not be made public.
- The file extensions of the uploaded add-ons will be checked. It is possible to set the
  allowed file extensions distinct for the specific use case of the add-on center. They
  could be dynamically changed at any time.
- The add-on sends messages to the project contact email on every edit of the add-on
  center's product versions field (thus the contributors could potentially add this new
  product version to their release / linked release).



Examples
--------

This add-on can be seen in action at the following sites:


Documentation
-------------

Full documentation for end users is available in the "docs" folder

Translations
------------

This product has been translated into

- German (Andreas Mantke)


Installation
------------

Install collective.addons by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.addons


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.addons/issues
- Source Code: https://github.com/collective/collective.addons


Support
-------

If you are having issues, please let us know.
Please create an issue in the project issue tracker (see above).


License
-------

The project is licensed under the GPLv2.
