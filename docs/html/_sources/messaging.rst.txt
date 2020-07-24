Messaging
#########

The collective.addons Plone add-on use some of the Plone messaging
implementations to create messages to the site admin, reviewers and the
owner / creator of add-ons.

Messages To The Site-Admininstrator / Administrator
***************************************************

- The site-administrator / admiinstrator get an e-mail once a new add-on
  project have been added to the add-on center.
- If the project owner submit her / his project for publication, the
  site-administrator / administrator get an e-mail about this event.
- Once the text of a published project change the site-administrator /
  administrator will get an e-mail with the complete text of the project
  summary and its description. Thus he get an information, if the text
  of the project changes into a direction that has not been reviewed.

If the form field 'contactForCenter' in the add-on center contains an
e-mail address the above messages will be send to this address. Otherwise
the e-mail goes to the e-mail address of the Plone site.



Messages To The Project Owner
*****************************

- Once a workflow status of his project(s) change the project owner will get an
  message (e-mail) which inform her / him about this new status.
- The project owner will get an e-mail once an add-on release or a linked
  add-on release have been added to her / his project(s).
- Once the site-administrator / administrator of the Plone site adds a new
  product version to the form field 'Available Versions' the owner of a
  project will get an e-mail to inform her / him about this event. The message
  ask the owner to update the versions list of the (linked) releases of his
  project(s).


Messages To A Possible Information Hub Of Add-on Releases
*********************************************************

It is possible to create a hub outside of the Plone site, that drives the
add-ons center, which could get an e-mail for every new published add-on
(linked) release. This e-mail could be parsed and used to inform the user
of the product about new (linked) releases from inside the product.




