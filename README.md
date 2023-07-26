# NASA-cFS-Bifrost
Bifrost Configuration for the NASA cFS 

# Influx Historical Telemetry Query Screenshot
![image](https://github.com/Mejiro-McQueen/Bifrost-NASA-cFS/assets/96747634/e4fea083-8538-437b-a1d4-d010e6dcbfc1)

# OpenMCT Live Telemetry Display Screenshot
![image](https://github.com/Mejiro-McQueen/Bifrost-NASA-cFS/assets/96747634/c00f8668-ded5-449e-bb57-005109ab7eac)

# Installation 

## Make artifacts directory
``
	sudo mkdir /gds
	sudo chown $USER:2001 /gds
	sudo chmod 775 /gds
``

## Installation
``
	git clone git@github.com:Mejiro-McQueen/Bifrost-NASA-cFS.git 
	cd bifrost
	make
``

# Extra Notes Below

# Table of Contents

1.  [Bifrost Deployment](#orge084a28)
2.  [Host Dependencies](#org322984f)
    1.  [Filesystem](#org0d5e535)
3.  [Repositories](#orge0fe812)
    1.  [About stability](#org30f7ac4)
    2.  [About Project Adaptation Repostories](#orgf884d73)
4.  [Configuration](#org4002976)
    1.  [Docker Layer](#org3fa4ba9)
        1.  [Bifrost](#org1a42cf8)
        2.  [NATS](#orgf8aed80)
        3.  [Influx](#org1d8efd6)
        4.  [NATS-CLI](#orgd883aaf)
        5.  [OpenMCT](#org226af61)
    2.  [docker.env layer](#org686190a)
    3.  [config templates](#org015eb04)
        1.  [tlm.yaml](#org0aa14f0)
        2.  [cmd.yaml](#orga7c859f)
        3.  [config.tmpl.yaml](#orge3de3c3)
        4.  [alarms.yaml](#orga9b908f)
        5.  [services.tmpl.yaml](#org3332e3e)
5.  [Web Services](#org516ecb4)
    1.  [NATS Network](#orgea00c74)
    2.  [InfluxDB](#org1bd9a12)
    3.  [Gjallarhorn](#orga61e132)
    4.  [OpenMCT](#org8dab0da)
    5.  [TCP Service](#orgee19dc6)
6.  [Adaptations](#orgb50d27b)
    1.  [Frame Processors](#orge77f7d5)
    2.  [Dictionaries](#orgc2d9438)
    3.  [Post Processing](#org09adb6c)


<a id="orge084a28"></a>

# Bifrost Deployment

Bifrost can be quickly deployed by using the NASA cFS Bifrost Expansion and docker:
<https://github.com/Mejiro-McQueen/Bifrost-NASA-cFS>

This sets up bifrost, its dependencies, etc&#x2026; for use with the NASA cFS FSS.


<a id="org322984f"></a>

# Host Dependencies


<a id="org0d5e535"></a>

## Filesystem

If using the default artifact directory /gds:

    sudo mkdir /gds
    sudo chown $USER:2001 /gds
    sudo chmod 775 /gds

The groupid 2001 is the hardcoded groupid for the user *bifrost* in the docker containers.
The docker containers are rootless and run as bifrost.

-   make
-   git
-   docker
    1.  docker is used to build, configure, and deploy:
        -   OpenMCT
        -   InfluxDB
        -   NATS
        -   NATS-CLI
    2.  Bifrost uses *make* for convenience scripts.
    3.  git is used for version control and to manage the project specific adaptations.


<a id="orge0fe812"></a>

# Repositories

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Repository</th>
<th scope="col" class="org-left">Note</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left"><https://github.com/Mejiro-McQueen/Bifrost-NASA-cFS></td>
<td class="org-left">Unstable NASA cFS Bifrost Expansion</td>
</tr>


<tr>
<td class="org-left"><https://github.com/Mejiro-McQueen/Bifrost></td>
<td class="org-left">Unstable Bifrost</td>
</tr>
</tbody>

<tbody>
<tr>
<td class="org-left"><https://github.com/14LAB/Bifrost-NASA-cFS></td>
<td class="org-left">Stable NASA cFS Bifrost Expansion</td>
</tr>


<tr>
<td class="org-left"><https://github.com/14LAB/Bifrost></td>
<td class="org-left">Stable Bifrost</td>
</tr>
</tbody>

<tbody>
<tr>
<td class="org-left"><https://github.com/14LAB/ait></td>
<td class="org-left">Hacked AIT dictionary and DSN capabilities.</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">Will remain frozen in order to motivate</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">building something new.</td>
</tr>
</tbody>
</table>


<a id="org30f7ac4"></a>

## About stability

The repos on Mejiro-McQueen are where I develop and experiment.
The repos on 14LAB are synced with Mejiro-McQueen whenever I have new stable features and have had a chance to test against cFS.


<a id="orgf884d73"></a>

## About Project Adaptation Repostories

-   I intend for projects to fork and own the stable NASA cFS Bifrost Expansion.
-   This repostitory contains the minimum configuration to integrate with the NASA cFS.
-   It contains Bifrost as a submodule (projects should switch to subtree and cherry pick commits from the upstream).
-   The project will customize the templates and add additional mission specific services.
-   This repostiory is designed to be self contained, i.e. is readily deployable and contains all tools needed for demo and evalutation:
    -   Bifrost
    -   Project Adaptations
    -   Influx
    -   OpenMCT
    -   NATS
    -   NATS CLI


<a id="org4002976"></a>

# Configuration


<a id="org3fa4ba9"></a>

## Docker Layer

The primary deployment method is through docker-compose. 
The NASA cFS Expansion contains contains defaults that make it usable out of the box.
Within the compose layer:


<a id="org1a42cf8"></a>

### Bifrost

-   Web Service Port
-   Flight Software Simulator host
-   Filesystem volume for storing GDS artifacts (downlinked files, service artifacts, telemetry dumps)
-   environment file (next layer of customization and configuration)
-   Additional environment variables can be set here to configure Bifrost options if it is convenient.


<a id="orgf8aed80"></a>

### NATS

The defaults for NATS have not been well explored, since the defaults have proven to be sufficient so far.

-   server name


<a id="org1d8efd6"></a>

### Influx

Bifrost will automatically setup and configure Influx buckets for storing telemetry.

-   Root login
-   Admin Token
-   Organization
-   Filesystem volume for storing Influx database and artifacts


<a id="orgd883aaf"></a>

### NATS-CLI

Used for debugging purposes, currently no configuration or customization is needed.


<a id="org226af61"></a>

### OpenMCT

Currently no configuration or customization is needed at this layer.


<a id="org686190a"></a>

## docker.env layer

This file contains various environment variable values used to configure Bifrost and its services.
Bifrost will substitute these variables when loading configuration template files (next customization layer)


<a id="org015eb04"></a>

## config templates

The *config* directory contains various configuration files and AIT dictionaries.


<a id="org0aa14f0"></a>

### tlm.yaml

This is an AIT telemetry dictionary.

-   Does not support templating.
-   Has support for variable array sizes.
-   See AIT documentation.


<a id="orga7c859f"></a>

### cmd.yaml

This is an AIT command dictionary.

-   Does not support templating.
-   Has support for variable array sizes.
-   See AIT documentation.
-   Configuration services does not known that this exists.


<a id="orge3de3c3"></a>

### config.tmpl.yaml

Template for additional AIT settings (DSN interface, KMC)

-   See AIT documentation.
-   Configuration service does not know that this exists.


<a id="orga9b908f"></a>

### alarms.yaml

Alarm definitions. Telemetry is evaluated against alarm conditions, 
and is assigned a color enum (default is green) and threshold flag. This metadata is transmitted through the
rest of the system.

-   Does not support templating.
-   Documentation coming soon.


<a id="org3332e3e"></a>

### services.tmpl.yaml

This defines and configures Bifrost services and the NATS network.
As the project progresses, they will not need to modify this file as often and
can rely on the templating capability for configuring the system for a specific venue or purpose.

-   Supports templating
-   Pipe data through the network by setting the appropriate streams and topics.
-   Disable services.
-   Modify the downlink or uplink pipeline by modifying stream inputs and outputs.

1.  Configuration Service

    -   Configuration service will automatically reconfigure services if their configuration changes.
    -   Configuration service will publish a service's configuration details over NATS on startup.
    -   Configuration service will publish a service's configuration details over NATS on request.
    -   Enable or disable a service's features by removing topics and streams.
    -   Set a local key/value store used to manage mission and pass specific data:
        Bifrost services can request the value of a key at any time.
        -   Pass ID
        -   AWS configuration
        -   Space Vehicle name
        -   SCID
        -   Custom values

2.  Task Manager

    The configuration and extension of Task Manager is the most complex and will be expained in further detail elsewhere.
    This service executes a task template whenever conditions are met (i.e. decompress a file downlink and upload the contents to S3 if they are text files and match the regular expression filter, then enter their contents into Influx).

3.  0158 Station Monitor

    -   Not shown in NASA cFS Expansion
    -   Not sure if the dictionary is distributable.
    -   Not supported in OpenMCT (dictionary incompatability, requires OpenMCT work)
    -   Supported in InfluxDB

4.  TCP Service

    Projects will configure specialized blocks in order to interact with external hosts (e.g. FSS).


<a id="org516ecb4"></a>

# Web Services


<a id="orgea00c74"></a>

## NATS Network

Other services can join this network in order to publish and receive streams/data from other services.
(e.g. a service that subscribes to EVRs in order to display them onto a GUI, another to send emails and text messages)


<a id="org1bd9a12"></a>

## InfluxDB

<http://localhost:8086>
View and plot telemetry, alarms, notebooks, backups, many other features.
All telemetry is dumped into this database.


<a id="orga61e132"></a>

## Gjallarhorn

<http://localhost:8000/>
Minimal working example of web UI 
Connects to Bifrost through web service.
Provides websockets to act as a gateway into the NATS network whenever a service can not use the NATS network.
(e.g. OpenMCT requests dictionaries through a websocket: <http://localhost:8000/dict/tlm>)


<a id="org8dab0da"></a>

## OpenMCT

<http://localhost:8081>
Used for telemetry visualization.
SunRISE has developed plugins to perform commanding, alarms, file uplink, etc&#x2026; from here.
This is the only GDS software that the MOS during operations.
Requires additional work.


<a id="orgee19dc6"></a>

## TCP Service

Used to interact with external software or hardware that can not use websocket or NATS client.

-   Receives TCP from other servers or clients (i.e. NASA cFS FSS) and publishes into a NATS stream or topic.
-   Transmits NATS stream or topic data to other servers or clients (i.e. NASA cFS FSS)


<a id="orgb50d27b"></a>

# Adaptations


<a id="orge77f7d5"></a>

## Frame Processors

Projects will need to copy and possibly modify a frame processor for each VCID.


<a id="orgc2d9438"></a>

## Dictionaries

Projects will need to define AIT telemetry and command dictionaries.


<a id="org09adb6c"></a>

## Post Processing

Projects may need to create post processors to perform special handling of particular packets.
