# django-fritzconnection

[![tests](https://github.com/jedie/django-fritzconnection/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/django-fritzconnection/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/django_fritzconnection/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/django_fritzconnection)
[![django-fritzconnection @ PyPi](https://img.shields.io/pypi/v/django-fritzconnection?label=django-fritzconnection%20%40%20PyPi)](https://pypi.org/project/django-fritzconnection/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-fritzconnection)](https://github.com/jedie/django-fritzconnection/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/django-fritzconnection)](https://github.com/jedie/django-fritzconnection/blob/main/LICENSE)

Web based FritzBox management using Python/Django and the great [fritzconnection](https://github.com/kbr/fritzconnection) library.

The basic idea is to block/unblock Internet access to a group of devices as easily as possible.

Current state: **early development stage**

Existing features:

* actions:
  * Change WAN access of a host or for all host of a group
* models:
  * HostModel - A host/device that is/was connected to your FritzBox
    * "Static" storage for all `FritzHosts().get_hosts_info()` information
    * Update in Admin via change list tools link and manage command
  * HostGroupModel - Collect host/device into groups to manage "WAN access"
    * Every group are listed on the front page
    * Allow/Disallow "WAN access" for all hosts of a group with one click
* a few "test" views:
  * Host information
    * Get information about registered hosts
    * Get raw mesh topology
  * Diagnose
    * Test FritzBox connection
    * List all FritzBox services


[![Install django-fritzconnection with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=django-fritzconnection)

> [django-fritzconnection_ynh](https://github.com/YunoHost-Apps/django-fritzconnection_ynh) allows you to install django-fritzconnection quickly and simply on a YunoHost server. If you don't have YunoHost, please consult [the guide](https://yunohost.org/#/install) to learn how to install it.

Pull requests welcome ;)


## Screenshots

[more screenshots](https://github.com/jedie/jedie.github.io/tree/master/screenshots/django-fritzconnection)

----

![Group Management](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/django-fritzconnection/v0.1.0.rc1%20-%20Group%20Management.png)

----

![Host Change List](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/django-fritzconnection/v0.0.2%20-%20hosts%20change%20list.png)

----

[more screenshots](https://github.com/jedie/jedie.github.io/tree/master/screenshots/django-fritzconnection)


## Quick start for developers

```
~$ git clone https://github.com/jedie/django-fritzconnection.git
~$ cd django-fritzconnection
~/django-fritzconnection$ ./manage.py
```

## FritzBox Credentials

Some of the FritzBox API requests needs a login. Currently the only way to store FritzBox Credentials is to add them into the environment.

Error message if login credentials are missing is: `Unable to perform operation. 401 Unauthorized`

Shell script work-a-round for developing, e.g.:

```
#!/bin/bash

(
    set -ex
    export FRITZ_USERNAME="<username>"
    export FRITZ_PASSWORD="<password>"

    ./devshell.py run_dev_server
)
```
See also: [Issues #5](https://github.com/jedie/django-fritzconnection/issues/5)


## Make new release

We use [cli-base-utilities](https://github.com/jedie/cli-base-utilities#generate-project-history-base-on-git-commitstags) to generate the history in this README.


To make a new release, do this:

* Increase your project version number
* Run tests to update the README
* commit the changes
* Create release


## History

See also git tags: https://github.com/jedie/manageprojects/tags

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [v0.3.0rc2](https://github.com/jedie/django-fritzconnection/compare/v0.2.0...v0.3.0rc2)
  * 2023-11-28 - fix CI and activate PYTHONWARNINGS only for the tests
  * 2023-11-28 - fix tox config
  * 2023-11-28 - Revert deletion of AUTHORS and LICENSE and remove obsolete snapshot file
  * 2023-11-28 - Remove different Django version from test matrix: Just use the newest release
  * 2023-11-28 - Fix tests
  * 2023-11-28 - Skip fetching host information if there is no IP address
  * 2023-11-28 - Log any fritzconnection call action
  * 2023-11-28 - generate the history in README
  * 2023-11-28 - fix code style
  * 2023-11-28 - Run django-upgrade
  * 2023-11-28 - +"flake8-bugbear"
  * 2023-11-28 - Switch from drv-shell to manage_django_project
  * 2023-06-11 - Update requirements
  * 2022-09-21 - Setup Github PyPi Cache
  * 2022-09-21 - Replace DynamicViewMenu with `bx_django_utils.admin_extra_views`
  * 2022-09-21 - Use RunServerCommand from django-tools
  * 2022-08-12 - fix CI
  * 2022-08-12 - update CI
  * 2022-05-29 - Remove Django v2.2 from text matrix
  * 2022-05-29 - "python3 devshell.py" -> "./devshell.py"
  * 2022-05-29 - Update tox setup
* [v0.2.0](https://github.com/jedie/django-fritzconnection/compare/v0.1.0...v0.2.0)
  * 2022-05-15 - Release v0.2.0
  * 2022-05-15 - Add test for host changelist + unique name filter
  * 2022-05-15 - NEW: Hosts admin action to ping all IPs from selected hosts
  * 2022-05-11 - Add host change list filter "unique name"
  * 2022-04-30 - Update requirements
* [v0.1.0](https://github.com/jedie/django-fritzconnection/compare/v0.0.3...v0.1.0)
  * 2022-04-08 - Update README.md
  * 2022-04-08 - Skip hosts without IP in group management
  * 2022-04-08 - Handle updating not existing host
  * 2022-04-08 - Set v0.1.0.rc0
  * 2022-04-08 - Bugfix adding new hosts without a group
* [v0.0.3](https://github.com/jedie/django-fritzconnection/compare/v0.0.2...v0.0.3)
  * 2022-04-08 - NEW: 'Manage host WAN access via host-groups'
  * 2022-04-08 - NEW: Group host entries
  * 2022-04-08 - Add some info about username/password
  * 2022-04-08 - Update README.md
  * 2022-04-08 - Display FRITZ_USERNAME and FRITZ_PASSWORD on connection info page
  * 2022-04-08 - set v0.0.3.rc0
  * 2022-04-07 - NEW: 'List "last connect" information about hosts' view
  * 2022-04-07 - Fix typo in URL

<details><summary>Expand older history entries ...</summary>

* [v0.0.2](https://github.com/jedie/django-fritzconnection/compare/e9ef397...v0.0.2)
  * 2022-04-04 - Render tags under name in change list
  * 2022-04-04 - Reoder admin change list
  * 2022-04-02 - Update README.md
  * 2022-04-02 - Fix python version in github actions
  * 2022-04-02 - Support Python 3.7
  * 2022-04-02 - SUpport and test with Python 3.7 (for YunoHost)
  * 2022-04-01 - NEW First usable action: "Change WAN access of a host"
  * 2022-04-01 - Store "WAN access state" for every host
  * 2022-04-01 - Display the RAW mesh topology JSON data
  * 2022-04-01 - Store host IP v4 address from FritzBox
  * 2022-04-01 - Remove django "sites"
  * 2022-03-31 - Add translations
  * 2022-03-31 - Delete wrong translation files
  * 2022-03-31 - Add "HostModel" to store all "fh.get_hosts_info()" information
  * 2022-03-31 - Bugfix settings.BASE_PATH
  * 2022-03-31 - Raise traceback on manage command errors
  * 2022-03-31 - Add a view to list all registered hosts and change internet access for one host
  * 2022-03-31 - cleanup gitignore
  * 2022-03-31 - Add FritzBox connection information in admin header
  * 2022-03-31 - Catch and log FritzConnectionException
  * 2022-03-31 - Add django admin context to diagnose views
  * 2022-03-29 - Enhance 'List all FritzBox services'
  * 2022-03-29 - Add 'List all FritzBox services' view
  * 2022-03-29 - Add 'Test FritzBox connection' view to admin index
  * 2022-03-24 - fix version
  * 2022-03-24 - Bugfix "publish" command
  * 2022-03-24 - Update README
  * 2022-03-24 - fix tests
  * 2022-03-24 - Init project
  * 2022-03-24 - Initial commit

</details>


[comment]: <> (✂✂✂ auto generated history end ✂✂✂)
