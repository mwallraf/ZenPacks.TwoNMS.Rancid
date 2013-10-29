*[current version = 1.0.0]*

# Overview


## ZenPack Description

This community zenpack fully integrates [RANCID](http://www.shrubbery.net/rancid/) into Zenoss without any manual coniguration required.

Backup all your routers, switches, load balancers, etc. right from the Zenoss interface.


## How does it work

The new "zenrancid" daemon takes care of running RANCID once a day in the background, by default at 02:00 am.

The Rancid modeler checks the SVN database for config changes and displays each config version as a device component.

> **The zenoss device ID is used in the Rancid config files. so make sure that it can resolve to a valid IP address.**
> **Possibly you need to add the hosts to the local /etc/hosts file. Examples can be found in the Zenoss community to automate this.**

## Screenshots

Check the [screenshots here](https://github.com/mwallraf/ZenPacks.TwoNMS.Rancid/tree/master/screenshots).


# Installation

> **Check the pre-requisites before starting the installation**
> **Install the ZenPack from command line to make sure everything went ok**

During the installation the RANCID binaries are being compiled from source (make & gcc) so the ZenPack only works on Unix. 
Currently the ZenPack has only been tested on CentOS but it should work on all unix flavors capable of compiling Rancid.


## Pre-Requisites

Make sure your system meets these requirements, you might also check the requirements for Rancid on their [website](http://www.shrubbery.net/rancid/):

* Unix only
* expect
* tar
* gzip
* make
* gcc
* subversion (CVS is currently not supported)
* telnet (for Rancid)
* sendmail (for Rancid)


## Installing the ZenPack

It is recommended to install this package from commandline so that you can see if there were any pre-requisites missing and if the compilation of RANCID was succesful.

      zenpack --link --install=/<path to files>/ZenPacks.TwoNMS.Rancid
      zenoss restart

If there were no errors and the folder $ZENHOME/rancid exists then the installation went ok.

Make sure that the new daemon "zenrancid" is started: 

      zenrancid status

**NOTE:** *re-installing the zenpack will remove all files in the $ZENHOME/rancid folder !*


## Upgradig the ZenPack

Upgrading the ZenPack is currently not specifically supported. If upgrading will not work then the old version has to be removed before installing the new version.
It is possible that upgrading will remove all old config files.

## Uninstalling the ZenPack

Uninstalling the ZenPack can be done using the Zenoss web interface or via commandline:

      zenpack --remove=ZenPacks.TwoNMS.Rancid

> **NOTE:** *re-installing the zenpack will remove all files in the $ZENHOME/rancid folder !*


# Adding Devices to Rancid

Devices can be added to RANCID using the zenoss interface by changing the zRancid properties. 
There is no need to manually populate the RANCID "router.db" files.

# Add the zenrancid modeler to the devices

Don't forget to add the zenrancid modeler to the devices that you want to include in Rancid! The modeler takes care of integrating the configs in the Zenoss GUI. Withouth the modeler Rancid will take the backups but you will not see the results inside Zenoss.
The modeler to add is community.twonms.python.RancidMap


## First Use

By default no devices will be added to the RANCID monitoring. 

In order to add a device you have to make sure the zRancid properties are set correctly.
Disabling the zRancidIgnore property will include the device to the RANCID router.db file and the next time RANCID runs the device will be included.

After a device has been enabled for Rancid via the zRancid properties the zenrancid daemon has to run.
You can run this manually or if the daemon is started you can wait until it's started automatically, by default once a day.
The modeler takes care of displaying the configs into zenoss, each config version is a device component called *Rancid Revision*.

> *It may take 2 runs of zenrancid before the configuration of the device will show up as a component.* 
> *The first run just checks in the device into the Subversion repository and as of the second run any configuration changes will be stored.*
> *The zenrancid daemon only runs once a day by default so if zenmodeler was started before zenrancid then any changes will be visible in Zenoss only after the next time zenmodeler is started.*


## zenrancid daemon

The is the daemon that takes care of running RANCID so it calls "rancid-run" in the background.
It is possible to disable the daemon but then you have to schedule rancid-run manually as a cron job.

The daemon can be configured using the zenrancid.conf config file.
By default zenrancid will start at 02:00am every day but this can be changed in the zenrancid.conf file.

It is possible to run zenrancid via command-line for all devices or for a single device:

      zenrancid run --device=MYDEVICE
      
(MYDEVICE should exist in Zenoss)


## Rancid modeler

The modeler will check if new config versions or SVN revisions are available. 
Each revision will be visible as a device os component called "Rancid Revision"

To run the modeler for a single device, this could be useful after running zenrancid for a single device:

      zenmodeler run --device=MYDEVICE

(MYDEVICE should exist in Zenoss)


## Rancid zProperties

A few new zProperties are created when the ZenPack is installed.
zRancid properties are used to indicate if a device will be added to Rancid, what Rancid device type it should be, what group is created and the username + password.

* zRancidIgnore = Indicates if the device should be included in Rancid or not
* zRancidGroup = The Rancid group that the device belongs to, each group means a different directory in Rancid
* zRancidDeviceType = The Rancid device type (ex. cisco, f5, netscreen)
* zRancidUser = The default username used to login to a device
* zRancidPassword = The default password for the username
* zRancidEnablePassword = The enable password if needed
* zRancidViewerPath = if you have ane external SVN viewer installed (ex. ViewVC) then you can put a link to the URL here, this link will be used in the Rancid Revision device components. This path accepts the parameters: %device% %group% %id% %type%
* zRancidSSH = Indicates that SSH should be used as login method, otherwise telnet will be used


# Configuration files

This ZenPack runs "out of the box" so no configuration changes have to be made.
However it is possible to change to the default Rancid configuration files which are stored in $ZENHOME/rancid/etc


## zenrancid daemon config

This is the default zenrancid daemon config file and is available in $ZENHOME/etc/zenrancid.conf
Usually you won't have to make any changes here except if you want to update the time and frequency when zenrancid should start.

* starttime 02:00 = the time when the zenrancid daemon should start the first time, by default 02:00am
* cycletime 86400 = the frequency when the zenrancid daemon starts, by default every 24 hours


## rancid.conf

This is the default configuration file used by Rancid and can be found in $ZENHOME/rancid/etc.
This file is auto-generated and over-written each time zenrancid runs.
You can override the generated file by creating a new file called $ZENHOME/rancid/etc/rancid-custom.conf
All settings in this custom file will override the standard settings.


## .cloginrc

This is the default device authentication file used by Rancid and can be found in the zenoss user home folder.
This file is auto-generated and over-written each time zenrancid runs.
You can override the generated file by creating a new file called $ZENHOME/rancid/etc/cloginrc-custom
All settings in this custom file will override the standard settings.


## router.db

The router.db files contain a list of all the devices that should be included in Rancid. Each device group has its own router.db file.
These files are generated automatically from Zenoss by disabling the "zRancidIgnore" property and configuring the "zRancidGroup" property. This is done each time the zenrancid daemon runs.

If you want to include devices to Rancid which are not managed in Zenoss then you need to create your own router.db files using the same folder structure as Rancid uses.
This has to be done in the folder $ZENHOME/rancid/etc/customdb/

For example if you have a folder structure $ZENHOME/rancid/var/Switches/router.db then you'll need to create the following file : $ZENHOME/rancid/etc/customdb/Switches/router.db


# Caveats

   - Special characters in passwords may need to be escaped (ex. *, ^, ..)
   - the first time it may take two runs of "zenrancid" before you will start seeing configs, the first time only the SVN folder structure is built
   - you have to wait for the next run of "zenmodeler" before config revisions will be visible as component
   - In case the installation fails because of missing requirements for example it may be impossible to re-install or remove the Zenpack because of an issue with the zProperties. The workaround is to comment all zProperties in the **__init__.py** file, remove the zenpack, uncomment the zProperties and try again.
   - at this moment customized router.db files can only be used for groups which already exist in Zenoss, so at least 1 device in zenoss must be enabled in the rancid group. Should be fixed


# TODO

So many things to add, so little time :)

Check the [readme.txt](https://github.com/mwallraf/ZenPacks.TwoNMS.Rancid/blob/master/README.txt) file for the TODO list for the next release.


# Contact & Links

* Report issues [here](https://github.com/mwallraf/ZenPacks.TwoNMS.Rancid/issues)
* Link to [Zenoss](http://www.zenoss.org/)
* Link to [Zenoss ZenPacks](http://wiki.zenoss.org/Category:ZenPacks)
* Link to [Rancid](http://www.shrubbery.net/rancid/)
* Link to [ViewVC](http://www.viewvc.org/)

For Professional services contact us at [TwoNMS.com](http://2nms.github.io)
