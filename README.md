# data_integratie
The following path needs to be changed to run the workflow:
- pdf_to_csv([PGPC-1.pdf]) contains a list of the path pdf files it's converting to a CSV file
    - with the following output as name: PGPC-1.csv
- all_vcf variable has the following list struture:
[[file_1.flt.vcf, filter_chr21_PGPC_filter21_0001.vcf, filter_chr21_PGPC-0001_filter21_vep_0001.vcf, PGPC-1.csv], [file_2.flt.vcf, filter_chr21_PGPC_filter21_0002.vcf, filter_chr21_PGPC-0002_filter21_vep_0002.vcf, PGPC-2.csv]]
    - It needs to have this order!, the first three files are required, the last file isn't an is excepted in the code

