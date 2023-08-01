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
# Design notes, spec sheets, diagrams, snippets, etc
See ./notes 
