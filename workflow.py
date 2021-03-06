# WORKFLOW DATA_INTEGRATIE
# authors: D.Hildebrand,L.Schoonveld,M.Ismail
from sqlite3 import IntegrityError
import psycopg2
import os
# custom imports
import vcf_parser
import csv_reader
import map_csv_conditions_2_db as person_table
import pdf_parser
import metadata

# pip install psycopg2  # don't forget to install


def connection(user, password):
    """Connect to a postgres database only available on an eduroam network
    Args:
        user (str): username
        password (str): password
    Returns:
        connection: database connection to postgres database
    """
    return psycopg2.connect(database="onderwijs", user=user,
                            password=password, host="postgres.biocentre.nl",
                            options="-c search_path=di_groep_6")


def get_command(command_base, data):
    """Creates a command to insert into a postgres database
    Args:
        person (list): list with all person information
    """
    for index, p in enumerate(data):
        if index == len(data) - 1:
            command_base = command_base + str(p) + ";"
            break
        else:
            command_base = command_base + str(p) + ", "
    # print(command_base)  # check command_base
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

    """annotates the filterd VCF files using VEP (docker is required).
    Install VEP using the following installation guide:
    https://www.ensembl.org/info/docs/tools/vep/script/vep_download.html#docker
    Args:
        filter_vcf (path): path to filterd VCF file
    """


def annotate_using_vep(filter_vcf, annotated_vcf):
    """annotates the filterd VCF files using VEP (docker is required).
    Install VEP using the following installation guide:
    https://www.ensembl.org/info/docs/tools/vep/script/vep_download.html#docker
    Args:
        filter_vcf (path): filtered VCF file (chr21) to annotate
        annotated_vcf (path): file name of annotated VCF file (chr21), 
        is going to be created using ensembl VEP.
    """
    os.system(
        f"docker run -i -t -v $HOME/vep_data:/opt/vep/.vep -v {filter_vcf}"
        f":/opt/vep/.vep/{annotated_vcf.split('/')[-1]} ensemblorg/ensem"
        f"bl-vep ./vep --cache -i /opt/vep/.vep/{filter_vcf.split('/')[-1]}"
        f" -o /opt/vep/.vep/output/{annotated_vcf.split('/')[-1]}")
    if os.stat(annotated_vcf).st_size > 0:
        print("workflow: Docker VEP file contains information, "
              "workflow continues...")
    else:
        print("workflow: Docker Failed VEP file doesn't cotain data")
        exit(1)


def csv_files(file, conditions_all_csv, person_all):
    """Reads CSV to check for conditions or symptoms
    Args:
        file (path): path to CSV file
        conditions_all_csv (dict): dict with conditions data for db
        person_all (list): list to add data for the person table in db
    Returns:
        conditions_all_csv, person_all: data to insert into db
    """
    con = csv_reader.read_csv(file)
    if con is None:
        print(f"No Symptoms or Condintions for {file}")
    else:
        # conditions_all_csv.append(csv_reader.read_csv(vcf[3].values()))
        conditions_all_csv |= con
    person_all.append(person_table.person_all([file])[0])
    return conditions_all_csv, person_all
    # example: database insert into person
    # INSERT INTO onderwijs.di_groep_6.person(person_id, person_source_value,
    #  year_of_birth, month_of_birth, gender_concept_id, gender_source_value,
    # race_concept_id, race_source_value, ethnicity_concept_id,
    # ethnicity_source_value) VALUES (3,'PGPC-3',1959, 'NULL',8507,'M',
    # 45532670,'White',45532670,'White'),(25,'PGPC-25',1944,12,8507,'M',
    # 45532670,'White',45532670,'White'),(26,'PGPC-26',1933,8,8507,'M',
    # 45532670,'White',45532670,'White');(26,'PGPC-26',1933,8,8507,'M',
    # 45532670,'White',45532670,'White'),


def pdf_to_csv(files):
    """PGPC files from pdf to csv format, files is a list with all files
    {file[:-4]}.csv will be the csv name, and {file[:-4]}_filtered.csv
    for the filterd files, but those won't be used.
    Args:
        files (list): path to pdf files
    """
    for file in files:
        pdf_parser.read_pdf(file)


def set_db_data_commands(all_vcf):
    """Get all the data for all the tables (person, measurement, 
    condition_occurrence) to later create a single command to insert
    into the database.
    Args:
        all_vcf (list): list containing all the data for all the files
        [[file_1.flt.vcf, filter_chr21_PGPC_filter21_0001.vcf, 
        filter_chr21_PGPC-0001_filter21_vep_0001.vcf, PGPC-1.csv], 
        [file_2.flt.vcf, filter_chr21_PGPC_filter21_0002.vcf, 
        filter_chr21_PGPC-0002_filter21_vep_0002.vcf, PGPC-2.csv]]
    Returns:
        return measurement, conditions, person: all the data
    """
    try:
        write_filter_vcf_to_annotate(all_vcf[:2])
    except IndexError:
        print("workflow: There is something wrong with lists of all file, "
              "check all_vcf")
    # annotate vcf files and set command for measurement table
    measurements_all_vcf = {}
    conditions_all_csv = {}
    person_all = []
    try:
        for index, vcf in enumerate(all_vcf):
            if index != 2:  # no vcf reading
                annotate_using_vep(vcf[1], vcf[2])
                measurements_all_vcf |= vcf_parser.read_file_filter(vcf[2])
                conditions_all_csv, person_all = csv_files(
                    vcf[3], conditions_all_csv, person_all)
            else:
                conditions_all_csv, person_all = csv_files(
                    vcf[0], conditions_all_csv, person_all)
        return measurements_all_vcf, conditions_all_csv, person_all
    except FileNotFoundError:
        print(f"workflow: Something went wrong with the files, "
              "please read the manual for the rigth configuration.")


def cursor_execute_db(cursor, command):
    """Execute a command in the database
    Args:
        cursor (cursor): cursor for postgres database
        command (str): command to execute into the database
    """
    print(f"workflow: Inserting the following into the database {command}")
    cursor.execute(command)


def close_con_cursor(cursor, conn, error):
    """Close the connection to the database
    Args:
        cursor (cursor): cursor from the database
        conn (connection): connection to the database
    """
    if conn:
        conn.close()
        cursor.close()
    if error:
        print("workflow: Closed connection to database.")
    else:
        print("workflow: Completed successfully and inserted into "
              "the database")


def main():
    # # the db is down/ unavailable
    try:
        conn = connection("DI_groep_6", "blaat1234")
        cursor = conn.cursor()
        print("workflow: Created cursor.")
    except psycopg2.OperationalError:
        print("workflow: Database connection failed, stopping workflow.")
        exit(1)
    # # stop comment

    # the standard insert commands are hardcoded
    command_p = "INSERT INTO onderwijs.di_groep_6.person(person_id, "\
        "person_source_value, year_of_birth, month_of_birth, gender_concept_id, "\
        "gender_source_value, race_concept_id, race_source_value, "\
        "ethnicity_concept_id, ethnicity_source_value) VALUES "
    command_m = "INSERT INTO onderwijs.di_groep_6.measurement(measurement_id,"\
        " person_id, measurement_date, measurement_concept_id, measurement_"\
        "source_value, value_as_concept_id, value_source_value, measurement_"\
        "type_concept_id) VALUES "

    command_c = "INSERT INTO onderwijs.di_groep_6.condition_occurrence(condit"\
        "ion_occurrence_id, person_id, condition_concept_id, condition_source_v"\
        "alue, condition_start_date, condition_type_concept_id) VALUES "

    # CHANGE TO NEW FILE LOCATION
    # PATH TO PATIENT PDF FILE (PGPC-26)
    list_csv_files = ["../data_integratie/example_data/PGPC-3.pdf",
                      "../data_integratie/example_data/PGPC-25.pdf",
                      "../data_integratie/example_data/PGPC-26.pdf"]

    # function loops over the list by itself.
    pdf_to_csv(list_csv_files)

    # CHANGE THE FILE
    # new order needs to be changed to the correct steps
    all_vcf = [["/Users/lean/data_integratie/PGPC_0003_S1.flt.vcf",
                "/Users/lean/data_integratie/filter_chr21_PGPC_filter21_0"
                "003.vcf", "/Users/lean/data_integratie/filter_chr21_PGPC"
                "-0003_filter21_vep_0003.vcf", 
                "../data_integratie/example_data/PGPC-3.csv"],
               ["/Users/lean/data_integratie/PGPC_0026_S1.flt.vcf",
                "/Users/lean/data_integratie/filter_chr21_PGPC_filter21"
                "_0026.vcf", "/Users/lean/data_integratie/filter_chr21_"
                "PGPC-0026_filter21_vep_0026.vcf", 
                "../data_integratie/example_data/PGPC-26.csv"],
               ["../data_integratie/example_data/PGPC-25.csv"]]
    # change
    measurements_all_vcf, conditions_all_csv, person_all = \
        set_db_data_commands(all_vcf)

    # check to see command for db if db is down/ unavailable
    # get_command(command_m, measurements_all_vcf.values())
    # get_command(command_c, conditions_all_csv.values())
    # get_command(command_p, person_all)

    # # comment to close_con_cursor(cursor, conn, False) to use script
    # # if the db is down/ unavailable
    try:
        cursor_execute_db(cursor, get_command(
            command_m, measurements_all_vcf.values()))
        cursor_execute_db(cursor, get_command(
            command_c, conditions_all_csv.values()))
        cursor_execute_db(cursor, get_command(command_p, person_all))
    except (Exception, psycopg2.Error) as e:
        print("workflow: Something went wrong inserting into the database, "
              f"is the data already inserted in the database? ({e}).")
        close_con_cursor(cursor, conn, True)
        exit(1)
    conn.commit()
    close_con_cursor(cursor, conn, False)
    # # stop comment
    metadata.create_meta_file("metadata.csv", all_vcf)


main()
