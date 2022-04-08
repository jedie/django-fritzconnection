# django-fritzconnection

![django-fritzconnection @ PyPi](https://img.shields.io/pypi/v/django-fritzconnection?label=django-fritzconnection%20%40%20PyPi)
![Python Versions](https://img.shields.io/pypi/pyversions/django-fritzconnection)
![License GPL V3+](https://img.shields.io/pypi/l/django-fritzconnection)

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


## Quick start for developers

```
~$ git clone https://github.com/jedie/django-fritzconnection.git
~$ cd django-fritzconnection
~/django-fritzconnection$ ./devshell.py
...
Developer shell - djfritz - v0.0.3
...

(djfritz) run_testserver
```

# FritzBox Credentials

Some of the FritzBox API requests needs a login. Currently the only way to store FritzBox Credentials is to add them into the environment.

Error message if login credentials are missing is: `Unable to perform operation. 401 Unauthorized`

Shell script work-a-round for developing, e.g.:

```
#!/bin/bash

(
    set -ex
    export FRITZ_USERNAME="<username>"
    export FRITZ_PASSWORD="<password>"

    ./devshell.py run_testserver
)
```
See also: [Issues #5](https://github.com/jedie/django-fritzconnection/issues/5)

## versions

* [*dev*](https://github.com/jedie/django-fritzconnection/compare/v0.0.3...main)
  * TBC
* [v0.0.3 - 08.04.2022](https://github.com/jedie/django-fritzconnection/compare/v0.0.2...v0.0.3)
  * NEW: 'Manage host WAN access via host-groups'
  * NEW: Add "host group" model to collect hosts into groups
  * NEW: 'List "last connect" information about hosts' view
  * Display `FRITZ_USERNAME` and `FRITZ_PASSWORD` (anonymized) on connection info page
* [v0.0.2 - 04.04.2022](https://github.com/jedie/django-fritzconnection/compare/v0.0.1-alpha...v0.0.2)
  * Store Host information
  * Possible to set WAN access for one host
* v0.0.1-alpha - 24.03.2022
  * init the project
