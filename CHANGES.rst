Changelog
=========

2.7 (2021-09-25)
----------------

- Use Products.PrintingMailHost version 1.1.6 [Andreas Mantke]
- Add classifiers for Python 3.8. and 3.9 [Andreas Mantke]
- Update localization files [Andreas Mantke]


3.1 (2021-08-10)
----------------

- flake8 fixes [Andreas Mantke]
- Update localization files [Andreas Mantke]


3.0 (2021-08-10)
----------------

- Change the main release number to 3.x because this version
  breaks compatibility due to move to honeypot instead of
  captcha technology to protect mail forms. [Andreas Mantke]
- Update README with information about honeypot technology
  [Andreas Mantke]
- Add contactauthor and contactprojectowner module with
  honeypot technology to protect against robots, add
  collective.honeypot to the requirements. [Andreas Mantke]
- Add configuration for collective.honeypot to the
  buildout script. [Andreas Mantke]
- Remove mailtoauthor and mailtoprojectowner modules with
  hcaptcha technology and plone.formwidget.hcaptcha from
  the requirements. [Andreas Mantke]
- Add configuration for collective.honeypot to
  base.cfg [Andreas Mantke]


2.6 (2021-08-06)
----------------

- Add PrintingMailHost to the buildout script [Andreas Mantke]
- Update readme and add information about using hcaptcha
  instead of recaptcha [Andreas Mantke]


2.5 (2021-07-23)
----------------

- Add PloneHotfix20210518 to the buildout [Andreas Mantke]
- Migrate contact forms from recaptcha to hcaptcha [Andreas Mantke]
- Update localization files and German localization [Andreas Mantke]
- Remove plone.formwidget.recaptcha from the buildout and
  replace it with plone.formwidget.hcaptcha [Andreas Mantke]


2.4 (2020-11-11)
----------------

- Text fixes in addoncenter view template [Andreas Mantke]
- Add listing of the number of projects per category to the sidebar of the
  addoncenter view template [Andreas Mantke]
- Update localization files [Andreas Mantke]


2.3 (2020-09-19)
----------------

- Reordering view templates and move them to one new folder [Andreas Mantke]
- Update localization files [Andreas Mantke]


2.2 (2020-08-02)
----------------

- Add a file extension validator for linked add-on releases. [Andreas Mantke]


2.1 (2020-07-27)
----------------

- Use safe_unicode for unicode strings, make more labels translatable [Andreas Mantke]
- Update README.rst [Andreas Mantke]
- Update localization files and German localization [Andreas Mantke]


2.0 (2020-07-24)
----------------

- Add a controlpanel and move configuration entries from the addoncenter
  module to this panel, create new vocabulary and functions from this
  entries in the configuration registry instead of entries in the portal_catalog,
  register vocabularies as named utilities in the configure.zcml file, use the
  new functions (inside the common module) for the project and (linked) release
  creation / edit form and their views as well as for the search feature of
  the addon center module. [Andreas Mantke]
- Update localization files and German localization [Andreas Mantke]
- Adapt the user documentation to the new functions and structure of the
  add-on and create documentation in html and pdf file format [Andreas Mantke]


1.2 (2020-05-07)
----------------

- Fix a tal expression on the addon release view. [Andreas Mantke]
- Add new fields to choose, in username and /or e-mail address of a
  project owner / contact should be published and save the choice
  in the portal_catalog. [Andreas Mantke]
- Update localization files and add German localization for new
  strings [Andreas Mantke]


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
