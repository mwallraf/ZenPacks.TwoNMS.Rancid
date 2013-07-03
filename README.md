*   [Overview](#overview)
    *   [ZenPack Description](#shortdescription)
    *   [How does it work](#shorthow)
    *   [Screenshots](#screenshots)
*   [Installation](#installation)
    *   [Pre-Requisites](#prereqs)
    *   [Install](#install)
    *   [Upgrade](#upgrade)
    *   [Uninstall](#uninstall)
*   [Monitor Devices](#monitoring)
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

The community zenpack integrates RANCID into Zenoss. All configuration is managed inside the Zenoss interface and configs.
New device configs are being displayed as device components and can be viewed in the component details window.
RANCID uses SVN (Subversion) in the background to keep track of config changes.

<h3 id="shorthow">How does it work</h3>

A new "zenrancid" daemon is created which runs RANCID once a day, by default at 02:00 am.
The Rancid modeler checks the SVN database for config changes and displays each config version as a device component.

<h3 id="screenshots">Screenshots</h3>

Check the screenshots inside the project.


<h2 id="installation">Installation</h2>

This is a regular ZenPack so the standard installation will work if the pre-requisites are met. 
RANCID is being compiled (make & gcc) automatically during the installation so the ZenPack only works on Unix. 
Currently it has only been tested on CentOS.

<h3 id="prereqs">Pre-Requisites</h3>

The following unix packages have to be installed and available in the $PATH for the zenoss user:

   * expect
   * tar
   * gzip
   * make
   * gcc
   * subversion (CVS is currently not supported)

<h3 id="install">Install</h3>

It is recommended to install this package from commandline so that you can see if there were any pre-requisites missing and if the compilation of RANCID was succesful.

zenpack --link --install=<installdir>/ZenPacks.TwoNMS.Rancid

If there were no errors and the folder $ZENHOME/rancid exists then the installation went ok.

Make sure to restart zopectl and zenhub. If there are any issues while running RANCID the first time then restart zenoss completely.

Make sure that the new daemon "zenrancid" is started: zenrancid status

Please note that re-installing the zenpack will remove all files in the $ZENHOME/rancid folder !

<h3 id="upgrade">Upgrade</h3>

Upgrading the ZenPack is currently not specifically supported. If upgrading will not work then the old version has to be removed before installing the new version.
It is possible that upgrading will remove all old config files.

<h3 id="uninstall">Uninstall</h3>

Uninstalling the ZenPack can be done using the Zenoss web interface or via commandline:

zenpack --remove=ZenPacks.TwoNMS.Rancid

Please note that removing the zenpack will delete all files and folders in $ZENHOME/rancid !


<h2 id="monitoring">Monitor Devices</h2>

Devices can be added to the RANCID monitoring using the zenoss interface. There is no need to manually populate the RANCID "router.db" files.

<h3 id="firstuse">First Use</h3>

By default no devices will be added to the RANCID monitoring. In order to add a device you have to make sure the zRancid configuration properties are configured.
Enabling the zRancidIgnore property will add the device to the RANCID router.db file and the next time RANCID runs the device will be included.
If you want to see the different configurations then the Rancid modeler has to be added for the device as well.

It may take 2 runs of zenrancid before the configuration of the device will show up as a component. The first run just checks in the device into the Subversion repository and as of the second run the configuration will be stored.

<h3 id="zenrancidd">zenrancid daemon</h3>

<h3 id="modeler">rancid modeler</h3>

<h3 id="zproperties">zProperties</h3>


<h2 id="configuration">Configuration</h2>

<h3 id="configzenrancid">zenrancid daemon config</h3>

<h3 id="configrancid">rancid.conf</h3>

<h3 id="configcloginrc">cloginrc</h3>

<h3 id="configrouterdb">router.db</h3>

<h2 id="caveats">Caveats</h2>

<h2 id="todo">TODO</h2>

<h2 id="contact">Contact & Links</h2>
