# laad de elementen in de database week 3/4

import psycopg2
import vcf_parser
import os

# pip install psycopg2  # don't forget to install

def connection(user, password):
    """_summary_
    Connect to a postgres database
    Args:
        user (_type_): _description_
        password (_type_): _description_

    Returns:
        _type_: _description_
    """
    return psycopg2.connect(database="onderwijs", user=user, password=password, host="postgres.biocentre.nl", options="-c search_path=di_groep_6")


def get_command(command_base, data):
    """_summary_
    Creattes a command to insert into a postgres database
    Args:
        person (list): list with all person information
    """
    for index, p in enumerate(data):
        if index == len(data) -1:
            command_base = command_base + p + ";"
            break
        else:
            command_base = command_base + p + ", "
    return command_base


def write_filter_vcf_to_annotate(s_vcf):
    """read and write VCF files with to cotain only genes from chr21
    Args:
        s_vcf (list): list with VCF files [stander_vcf, filter_vcf, vep_vcf]
    """
    for vcf in s_vcf:  # standard vcf file
        try:
            info = vcf_parser.read_file(vcf[0])
            vcf_parser.write_file(vcf[1], info)
        except FileNotFoundError as e:
            print(f"workflow: File not found try changing the path {e}")


def annotate_using_vep(filter_vcf, annotated_vcf):
    """annotates the filterd VCF files using VEP (docker is required).
    Install VEP using the following installation guide:
    https://www.ensembl.org/info/docs/tools/vep/script/vep_download.html#docker
    Args:
        filter_vcf (path): path to filterd VCF file
    """
    # os.system("docker run -i -t -v $HOME/vep_data:/opt/vep/.vep -v {filter_vcf}:/opt/vep/.vep/{annotated_vcf} ensemblorg/ensembl-vep")
    

    # INSERT INTO onderwijs.di_groep_6.person(person_id, person_source_value, year_of_birth, month_of_birth, gender_concept_id, gender_source_value, race_concept_id, race_source_value, ethnicity_concept_id, ethnicity_source_value) VALUES (3,'PGPC-3',1959, 'NULL',8507,'M',45532670,'White',45532670,'White'),(25,'PGPC-25',1944,12,8507,'M',45532670,'White',45532670,'White'),(26,'PGPC-26',1933,8,8507,'M',45532670,'White',45532670,'White');(26,'PGPC-26',1933,8,8507,'M',45532670,'White',45532670,'White'),
def main():
    filter_annotated_vcf =["/Users/lean/data_integratie/Filtered_chr21_"
    "PGPC-3_annotated.vcf", "/Users/lean/data_integratie/Filtered_chr21_"
    "PGPC-26_annotated.vcf"]

    # connection failed:
    # conn = connection("DI_groep_6", "blaat1234")  
    # cursor = conn.cursor()
    
    # cursor.execute("select version()")
    # "INSERT INTO onderwijs.di_groep_6.person(person_id, person_source_value, year_of_birth, month_of_birth, gender_concept_id, gender_source_value, race_concept_id, race_source_value, ethnicity_concept_id, ethnicity_source_value) VALUES (3,'PGPC-3',1959, 'NULL',8507,'M',45532670,'White',45532670,'White'),(25,'PGPC-25',1944,12,8507,'M',45532670,'White',45532670,'White'),(26,'PGPC-26',1933,8,8507,'M',45532670,'White',45532670,'White');(26,'PGPC-26',1933,8,8507,'M',45532670,'White',45532670,'White'),"
    command_p = "INSERT INTO onderwijs.di_groep_6.person(person_id, "\
    "person_source_value, year_of_birth, month_of_birth, gender_concept_id, "\
    "gender_source_value, race_concept_id, race_source_value, "\
    "ethnicity_concept_id, ethnicity_source_value) VALUES "
    person = ["(3,'PGPC-3',1959, NULL,8507,'M',45532670,'White',45532670,'White')", "(25,'PGPC-25',1944,12,8507,'M',45532670,'White',45532670,'White')", "(26,'PGPC-26',1933,8,8507,'M',45532670,'White',45532670,'White')"]
    command_p = get_command(command_p, person) # set the person table correct
    print(command_p)
    # cursor.execute(command)



    # measurements = vcf_parser.read_file_filter(filter_annotated_vcf)
    # print(measurements)
    command_m = "INSERT INTO onderwijs.di_groep_6.measurement(measurement_id,"\
        " person_id, measurement_date, measurement_concept_id, measurement_"\
        "source_value, value_as_concept_id, value_source_value, measurement_"\
        "type_concept_id) VALUES "

    # cursor.execute(command_m)
    # Fetch a single row using fetchone() method.
    # data = cursor.fetchone()
    # print("Connection established to: ",data)
    # conn.commit()
    # conn.close()


    # new order needs to be changed to the correct steps
    all_vcf = [["/Users/lean/data_integratie/PGPC_0003_S1.flt.vcf", 
    "/Users/lean/data_integratie/filter_chr21_PGPC_filter21_0003.vcf", 
    "/Users/lean/data_integratie/filter_chr21_PGPC-0003_filter21_vep_0003.vcf"], 
    ["/Users/lean/data_integratie/PGPC_0026_S1.flt.vcf",
    "/Users/lean/data_integratie/filter_chr21_PGPC_filter21_0026.vcf", 
    "/Users/lean/data_integratie/filter_chr21_PGPC-0026_filter21_vep_0026.vcf"]]

    write_filter_vcf_to_annotate(all_vcf)

    # annotate vcf files and set command for measurement table
    for vcf in all_vcf:
        annotate_using_vep(vcf[1], vcf[2])

        # get genes 10 from the annotated vcf file into the
        # measuremnt table in the database
        measurements = vcf_parser.read_file_filter(vcf[2])
        command_m = get_command(command_m, measurements.values())
    print(command_m)
    # for file in filter_annotated_vcf:
    #     measurements = vcf_parser.read_file_filter(file)
    #     command_m = get_command(command_m, measurements.values())
    #     print(command_m, "test")
    
main()
