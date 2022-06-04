# author: Dominic, Lean
from datetime import datetime


def create_meta_file(file, sources):
    """Function that creates a file containing metadata, like last run, 
    authors, database_type, version workflow

    Args:
        file (path): string containing file name
        sources (list): list containing source data (1D or 2D)
    """
    sources = create_one_list_sourcefiles(sources)
    datenow = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    with open(file, "w") as fp:
        # remove existing content
        fp.seek(0)
        fp.truncate()
        # create new file content
        fp.write(f"date_lastrun,{datenow}\n")
        fp.write(f"data_source,{', '.join(sources)}\n")
        fp.write("workflow_creators,D.Hildebrand,L.Schoonveld,M.Ismail\n")
        fp.write("workflow_version, workflow v1.0.1")
        fp.write("database_type,Postgres\n")
        fp.write("database_version,PostgreSQL 14.3 on x86_64-pc-linux-gnu, "
                 "compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit\n")
        fp.write(f"database_last_attempt_update,{datenow}\n")


def create_one_list_sourcefiles(sources):
    """Makes from a 2d list (e.g. all_vcf from workflow) a 1d list
    to generate metadata for.
    Args:
        sources (list): [[][]] or []

    Returns:
        list: _description_
    """
    # if element a list not a 1D list, but a 2d list
    new_sourcefiles = []
    if isinstance(sources[0], list):
        for source in sources:
            for s in source:
                new_sourcefiles.append(s)
        return new_sourcefiles
    else:
        # is already a list
        return sources
