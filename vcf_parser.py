# author: Lean
import uuid

def read_file(file):
    """Read lines VCF from a VCF file.
    Args:
        file (path): path to VCF file
    Returns:
        dict: lines from VCF file with ch
    """
    info = {}
    with open(file, "r") as f:
        for index, line in enumerate(f):
            line_sp = line.split("\t")
            try:
                if line_sp[0] == "chr21" or line.startswith("#"):  # get chr21
                    info[index] = line
            except IndexError:
                pass
    return info


def read_file_filter(filter_annotated_variants):
    """Gets 10 annotated gene variants (via  VEP) from a VCF file
    use the function multiple times for more files.
    Args:
        filter_annotated_variants (str): path to VCF file
    Returns:
        dict: gene, with gene_annotated_variants information
    """
    info = {}
    chosen_variants = 0
    # get person id from the VCF file name.
    for person in filter_annotated_variants.split("_"):
        if "PGPC" in person:  # e.g. PGPC-26
            person_id = person.split("-")[1]
    try:
        print(f"workflow: Generating data for measurement, patient {person_id}")
    except NameError:
        print("workflow: Something went wrong with person_id for the person.")
    with open(filter_annotated_variants, "r") as f:
        for index, line in enumerate(f):
            line_sp = line.strip().split("\t")
            try:
                if line.strip().startswith("## Output produced at"):
                    # expected date format 
                    # ## Output produced at 2022-04-25 09:52:30"
                    date = line.strip().split(" ")[4]
                if line_sp[3] != "-":  # 3 is gene, 4 is feature
                    if chosen_variants <= 10:
                        chosen_variants += 1
                        # print(line_sp)
                        if line_sp[3] != "Gene" or line_sp[4] != "Feature":
                            # so the first header is 
                            # PostgreSQL uses the yyyy-mm-dd
                            # measurement_type_concept_id: 5001 for all
                            person_id = person_id.replace("0", "")
                            info[index] = f"({int(str(uuid.uuid1().int)[-9:])}, {person_id}, '{date}', 4281995, '{line_sp[3]}', 4048365, '{line_sp[4]}', 5001)" 
                            # print(info[index], "test")
                        # UUID, person_id, date, measurement_concept_id, gene (measurement_source_value), value_as_concept_id (measurement_id athena) feature, measurement_type_concept_id
            except IndexError:
                pass
    return info

def write_file(file, info):
    """writes the filterd VCF data into a new file to get annotated.
    Args:
        file (path): path to the filtered VCF file
        info (dict): dict of information about the VCF file
    """
    # the standard info is written manually to the vcf file
    with open(file, "w") as f:
        for line_info in info.values():
            f.write(f"{str(line_info)}")
    print(f"workflow: {file} contains {len(info.values())} variants.")