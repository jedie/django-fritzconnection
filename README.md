# django-fritzconnection

![django-fritzconnection @ PyPi](https://img.shields.io/pypi/v/django-fritzconnection?label=django-fritzconnection%20%40%20PyPi)
![Python Versions](https://img.shields.io/pypi/pyversions/django-fritzconnection)
![License GPL V3+](https://img.shields.io/pypi/l/django-fritzconnection)

Web based FritzBox management using Python/Django.

Current state: **early development stage**

Features:

* actions:
  * Change WAN access of a host
* models:
  * HostModel
    * "Static" storage for all `FritzHosts().get_hosts_info()` information
    * Update in Admin via change list tools link and manage command
* a few "test" views:
  * Host information
    * Get information about registered hosts
    * Get raw mesh topology
  * Diagnose
    * Test FritzBox connection
    * List all FritzBox services


[![Install django-fritzconnection with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=django-fritzconnection)

> *This package allows you to install django-fritzconnection quickly and simply on a YunoHost server.
If you don't have YunoHost, please consult [the guide](https://yunohost.org/#/install) to learn how to install it.*

Pull requests welcome ;)


## Quick start for developers

```
~$ git clone https://github.com/jedie/django-fritzconnection.git
~$ cd django-fritzconnection
~/django-fritzconnection$ ./devshell.py
...
Developer shell - djfritz - v0.0.2.rc0
...

(djfritz) run_testserver
```

## versions

* [*dev*](https://github.com/jedie/django-fritzconnection/compare/v0.0.2.rc0...main)
  * TBC
* [v0.0.2.rc0 - 02.04.2022](https://github.com/jedie/django-fritzconnection/compare/v0.0.1-alpha...v0.0.2.rc0)
  * Store Host information
  * Possible to set WAN access for one host
* v0.0.1-alpha - 24.03.2022
  * init the project
