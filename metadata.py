from datetime import datetime

def create_meta_file(file, sources):
    """
    Function creates metadata file
    PARAMS: Str metadatafilename: string containing file name
            List sources: list containing source data
    RETURN: File containing metadata
    """
    datenow = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    with open(file, "w") as fp:
        # remove existing content
        fp.seek(0)
        fp.truncate()
        # create new file content
        fp.write(f"date_lastrun,{datenow}\n")
        fp.write(f"data_source,{sources}\n")
        fp.write("workflow_creators,D.Hildebrand,L.Schoonveld,M.Ismail\n")
        fp.write("database_type,Postgres\n")
        fp.write("database_version,PostgreSQL 14.3 on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit\n")
        fp.write(f"database_last_updated,{datenow}\n")

