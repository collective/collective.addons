Changelog
=========

1.1 (2020-03-28)
----------------

- Fix formating and text issues in the users docomentation, add
  information about buildout entries and update documentation in
  HTML and PDF file format. [Andreas Mantke]
- Include documentation txt-files into the the
  MANIFEST.in [Andreas Mantke]
- Add versions to test_plone52.cfg [Andreas Mantke]
- Fix travis.yml [Andreas Mantke]
- Add a new module for a contact with the project owner, add a link to
  the mail forms from addon project respective the addon center
  view. [Andreas Mantke]
- Fix two URLs in own_projects.pt [Andreas Mantke]
- Add a subscriber for messaging about new project added [Andreas Mantke]
- Update localization files [Andreas Mantke]



1.0 (2019-11-16)
----------------

- Complete user documentation [Andreas Mantke]
- Flake8 fixes [Andreas Mantke]
- Add a custom.css for creating documentation in HTML file
  format [Andresa Mantke]


1.0b2 (2019-11-03)
------------------

- Add user documentation [Andreas Mantke]
- Add further directories to .gitignore [Andreas Mantke]


1.0b0 (2019-09-11)
------------------

- Made additions to travis.yml to get the robot test running
  successfully [Andreas Mantke]
- Update the Readme and add more features of the add-on [Andreas Mantke]
- Change the name of the field for the add-on project contact
  address [Andreas Mantke]
- Flake8 fixes [Andreas Mantke]


1.0a4 (2019-09-03)
------------------

- Pep8 and other code fixes [Andreas Mantke]
- Move from api.portal.get_tool to api.content.find for portal_catalog
  searches [Andreas Mantke]
- Move from checkpermission to api.user.has_permission [Andreas Mantke]
- Fix the message to sender in the mailtoauthor form [Andreas Mantke]
- Add further dependencies to the install_requirements section
  of the setup.py script [Andreas Mantke]
- Add include dependencies of the package to configure.zcml [Andreas Mantke]
- Remove test for Plone 4.3 from travis.yml [Andreas Mantke]
- Update localization files [Andreas Mantke]


1.0a3 (2019-08-23)
------------------

- Pep8, isort and code-analysis fixes. [Andreas Mantke]



1.0b1 (2019-08-23)
------------------

- Add notifications module [Andreas Mantke]
- Fix css-class names in addonrelease and addonlinkedrelease
  view [Andreas Mantke]
- Move a css inline style to the style sheet file [Andreas Mantke]
- Pep8 fixes [Andreas Mantke]
- Update localization template file and localization files,
  update German translation. [Andreas Mantke



1.0a2 (2019-08-16)
------------------

- Fix regular expressions for file extension validation [Andreas Mantke]
- Add import for Invalid to the addoncenter module [Andreas Mantke]
- Add necessary imports for virus scanning with
  collective.clamaav [Andreas Mantke]
- Fix title strings and field namings [Andreas Mantke]
- Update localization template file and localization files and
  add the missing German localization strings [Andreas Mantke]



1.0a1 (2019-08-13)
------------------

- Initial release.
  [andreasma]
