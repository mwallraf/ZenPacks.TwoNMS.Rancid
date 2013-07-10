*   [Overview](#overview)
    *   [ZenPack Description](#shortdescription)
    *   [How does it work](#shorthow)
    *   [Screenshots](#screenshots)
*   [Installation](#installation)
    *   [Pre-Requisites](#prereqs)
    *   [Install](#install)
    *   [Upgrade](#upgrade)
    *   [Uninstall](#uninstall)
*   [Add Devices to Rancid](#monitoring)
    *   [First Use](#firstuse)
    *   [zenrancid daemon](zenrancidd)
    *   [rancid modeler](#modeler)
    *   [zProperties](#zproperties)
*   [Configuration](#configuration)
    *   [zenrancid daemon config](#configzenrancid)
    *   [rancid.conf](#configrancid)
    *   [cloginrc](#configcloginrc)
    *   [router.db](#configrouterdb)
*   [Caveats](#caveats)
*   [TODO](#todo)
*   [Contact & Links](#contact)


<h2 id="overview">Overview</h2>

<h3 id="shortdescription">ZenPack Description</h3>

This community zenpack integrates RANCID into Zenoss. All configuration is managed inside the Zenoss interface.
The device configurations are being displayed as device components and can be viewed in the component details window.
RANCID uses SVN (Subversion) in the background to keep track of config changes.

<h3 id="shorthow">How does it work</h3>

The new "zenrancid" daemon takes care of running RANCID once a day in the background, by default at 02:00 am.

The Rancid modeler checks the SVN database for config changes and displays each config version as a device component.

<h3 id="screenshots">Screenshots</h3>

Check the screenshots inside the project.


<h2 id="installation">Installation</h2>

This is a regular ZenPack so the standard installation will IF all the pre-requisites are installed. 
RANCID is being compiled (make & gcc) automatically during the installation so the ZenPack only works on Unix. 
Currently the ZenPack has only been tested on CentOS but it should work on all unix flavors capable of compiling Rancid.

<h3 id="prereqs">Pre-Requisites</h3>

The following packages have to be installed prior to installing the ZenPack and they have to be in the PATH of the zenoss user:

   * expect
   * tar
   * gzip
   * make
   * gcc
   * subversion (CVS is currently not supported)

<h3 id="install">Installing ZenPack</h3>

It is recommended to install this package from commandline so that you can see if there were any pre-requisites missing and if the compilation of RANCID was succesful.

   zenpack --link --install=<installdir>/ZenPacks.TwoNMS.Rancid

If there were no errors and the folder $ZENHOME/rancid exists then the installation went ok.

Make sure to restart zopectl and zenhub. If there are any issues while running RANCID the first time then restart zenoss completely.

Make sure that the new daemon "zenrancid" is started: 

   zenrancid status

**NOTE:** *re-installing the zenpack will remove all files in the $ZENHOME/rancid folder !*

<h3 id="upgrade">Upgrade</h3>

Upgrading the ZenPack is currently not specifically supported. If upgrading will not work then the old version has to be removed before installing the new version.
It is possible that upgrading will remove all old config files.

<h3 id="uninstall">Uninstall</h3>

Uninstalling the ZenPack can be done using the Zenoss web interface or via commandline:

   zenpack --remove=ZenPacks.TwoNMS.Rancid

**NOTE:** *re-installing the zenpack will remove all files in the $ZENHOME/rancid folder !*


<h2 id="monitoring">Add Devices to Rancid</h2>

Devices can be added to RANCID using the zenoss interface by changing the zRancid properties. 
There is no need to manually populate the RANCID "router.db" files.

<h3 id="firstuse">First Use</h3>

By default no devices will be added to the RANCID monitoring. 

In order to add a device you have to make sure the zRancid properties are set
Disabling the zRancidIgnore property will include the device to the RANCID router.db file and the next time RANCID runs the device will be included.

After a device has been enabled for Rancid via the zRancid properties the zenrancid daemon has to run.
You can run this manually or if the daemon is started you can wait until it's started automatically, by default once a day.
The modeler takes care of displaying the configs into zenoss, each config version is a device component called *Rancid Revision*.

**NOTE:** It may take 2 runs of zenrancid before the configuration of the device will show up as a component. 
The first run just checks in the device into the Subversion repository and as of the second run any configuration changes will be stored.

**NOTE:** The zenrancid daemon only runs once a day by default so if zenmodeler was started before zenrancid then any changes will be visible in Zenoss only after the next time zenmodeler is started.

<h3 id="zenrancidd">zenrancid daemon</h3>

The is the daemon that takes care of running RANCID so it calls "rancid-run" in the background.
It is possible to disable the daemon but then you have to schedule rancid-run manually as a cron job.

The daemon can be configured using the zenrancid.conf config file.
By default zenrancid will start at 02:00am every day but this can be changed in the zenrancid.conf file.

It is possible to run zenrancid via command-line for all devices or for a single device:

   zenrancid run --device=<my device>

<h3 id="modeler">Rancid modeler</h3>

The modeler will check if new config versions or SVN revisions are available. 
Each revision will be visible as a device os component called "Rancid Revision"

<h3 id="zproperties">zProperties</h3>

A few zRancid properties are created when the ZenPack is installed.
zRancid properties are used to define if a device will be added to Rancid, what Rancid device type it should be, what group is created and the username + password.

* zRancidGroup =
* zRancidType =
* zRancidUser =
* zRancidPassword =
* zRancidEnablePassword =
* zRancidViewer =
* zRancidSSH =

<h2 id="configuration">Configuration</h2>

Although this ZenPack runs "out of the box" and all configuration files are being overwritten each time zenrancid is started, it is possible to define your own custom Rancid settings.
All these configurations files are available in $ZENHOME/rancid/etc

<h3 id="configzenrancid">zenrancid daemon config</h3>

This is the default zenrancid daemon config file and is available in $ZENHOME/etc/zenrancid.conf
Usually you won't have to make any changes here except if you want to update the time and frequency when zenrancid should start.
It's a typical zenoss config, the most important rancid parameters are:

* rancid_starttime =
* rancid_cycletime =

<h3 id="configrancid">rancid.conf</h3>

This is the default configuration file used by Rancid. This file is auto-generated and over-written each time zenrancid runs!
If you want to make customized changes then create a new file called $ZENHOME/rancid/etc/rancid-custom.conf
All settings in this custom file will override the standard settings.

<h3 id="configcloginrc">cloginrc</h3>

<h3 id="configrouterdb">router.db</h3>

<h2 id="caveats">Caveats</h2>

* Special characters in passwords may need to be escaped (ex. *, ^, ..)

<h2 id="todo">TODO</h2>

<h2 id="contact">Contact & Links</h2>
