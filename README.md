# data_integratie
This is a workflow designed to anotate VCF files from data from patient (), and the health data from the patient pdf files are mapped to a OMOP common data model with the concepts using the OMOP vocabulary (Athena.org) .  

## Installation:
The workflow runs in a conda (miniconda) environment, and can be installed by the following command:
- conda env create -n data_integratie --file data_integratie.yaml

This will install the correct version of psycopg2 for the connection with the database. And the right dependencies will be installed for tabula to convert the pdf into csv files.

## Run the workflow
The following variables will need to be changed to the files from the user.
- pdf_to_csv([PGPC-1.pdf]) contains a list of the path pdf files it's converting to a CSV file
    - with the following output as name: PGPC-1.csv
- all_vcf variable has the following list struture:
[[file_1.flt.vcf, filter_chr21_PGPC_filter21_0001.vcf, filter_chr21_PGPC-0001_filter21_vep_0001.vcf, PGPC-1.csv], [file_2.flt.vcf, filter_chr21_PGPC_filter21_0002.vcf, filter_chr21_PGPC-0002_filter21_vep_0002.vcf, PGPC-2.csv]]
    - **It needs to have this order!** The first three files are required, the last file isn't required and is excepted in the code.
    - The first file needs to be a legit VCF file and the other files are only the names that are going to be used for the workflow.

