# data_integratie
This is a workflow designed to anotate VCF files from data from patient (https://personalgenomes.ca/), and the health data from the patient pdf files are mapped to a OMOP common data model with the concepts using the OMOP vocabulary (Athena.org).  

## Installation:
The workflow runs in a conda (miniconda) environment, and can be installed by the following command:
- conda env create -n data_integratie --file data_integratie.yaml

This will install the correct version of psycopg2 for the connection with the database. And the right dependencies will be installed for tabula to convert the pdf into csv files.

To use ensembl VEP it needs to be installed via docker. The following link will show how to correctly configure docker for ensembl VEP.
- https://www.ensembl.org/info/docs/tools/vep/script/vep_download.html#docker
- The output will be placed in the output directory created for the docker vep.

Please make sure that while running the workflow that you're connected with the EDUROAM network, currently the postgres database isn't available outside the network.

## Run the workflow:
The following variables will need to be changed to the files from the user. Make sure that in all variables the different patients are in the same order.
- pdf_to_csv([../data_integratie/example_data/PGPC-1.pdf]) contains a list of the path pdf files it's converting to a CSV file
    - with the following output as name: PGPC-1.csv, so the path in all_vcf becomes for the .csv: "../data_integratie/example_data/PGPC-1.csv"
- all_vcf variable has the following list struture:
[[file_1.flt.vcf, filter_chr21_PGPC_filter21_0001.vcf, filter_chr21_PGPC-0001_filter21_vep_0001.vcf, PGPC-1.csv], [file_2.flt.vcf, filter_chr21_PGPC_filter21_0002.vcf, filter_chr21_PGPC-0002_filter21_vep_0002.vcf, PGPC-2.csv]]
    - **It needs to have this order!** The first three files are required, the last file isn't required and is excepted in the code.
    - The first file needs to be a legit VCF file and the other files are only the names that are going to be used for the workflow.

The PGPC_filtered.sv files are not used, but they can be usefull to quickly see patient important info that gets into the database.

