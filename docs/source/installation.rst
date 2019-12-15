Installation
############


You can install the Plone add-on collective.addons using zc.buildout
and the plone.recipe.zope2instance. Thus you could add it to the list of
eggs to install, e.g.:

.. code-block:: Python

    [buildout]
        ...
        eggs =
            ...
            collective.addons

Once you have added the add-on re-run buildout, e.g. with:

.. code-block:: Bash

    $ ./bin/buildout


Once your buildout finished you had to create a new Plone site and then
install and activate the Plone add-on inside this new Plone site.
Therefor you had to go to the Plone 'Site Setup' adminstration area. If
you got administration permissions you find a link to it in the menu
entry with your name (or 'admin'). You could reach it directly by
adding '/@@overview-controlpanel' to the URL of your Plone site.

In the 'Site Setup' page click on 'Add-ons' and you get a list of the Plone add-ons which
are available in your Plone site.


.. image:: images/install_collective_addon.png
   :width: 600

You will get a list like in the above screenshot. Click on the 'install' button next to
the 'collective.addons' list entry and the add-on will be installed in your Plone site.


Navigation configuration
************************

Next you need to go to the 'Navigation' configuration inside the 'Site Setup'. Thus click on
the corresponding button and you get to the configuration menu in the screenshot below.


.. image:: images/navigation_add_addon_center.png
   :width: 600

Tick the checkbox in fron of the entry 'Add-on_Center' and save your changes. The necessary steps
are done to go to the homepage of your Plone site (or a subdirectory of the site, where you want to
create a new add-on center.
