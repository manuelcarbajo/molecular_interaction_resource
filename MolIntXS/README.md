# Molecular interaction REST API server
This repo hosts the code necessary to run the REST API server that manages the endpoints to query the Molecular interactions database resource from Ensembl.
The pipeline that populates the actual database (Map_interspecies_interactions) uses a separate repository hosted at https://github.com/Ensembl/ensembl-production-imported  

## Prerequisites
Pipelines are intended to be run inside the Ensembl production environment.
Please, make sure you have all the proper credential, keys, etc. set up.

### Getting this repo

```
git clone git@github.com:Ensembl/molecular_interaction_resource.git
```

### Configuration

#### Refresing environment

This project uses the Django restframework
It runs inside a virtual conda environment which itself lives inside a virtual machine

### Initialising and running the server

Log in to codon
Log in to a web-production network
Become one of the authorised virtual users
Log into the virtual machine
Activate the virtual conda environment
Open the screen "run server"
Set the server environment variables (MolIntXS_DBNAME, MolIntXS_msql_USER,MolIntXS_msql_PASSWORD, MolIntXS_msql_HOST, and MolIntXS_msql_PORT)


