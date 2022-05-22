# Lean
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
    print(f"workflow: Generating data for measurement, patient {person_id}")
    with open(filter_annotated_variants, "r") as f:
        for index, line in enumerate(f):
            line_sp = line.strip().split("\t")
            try:
                if line.strip().startswith("## Output produced at"):
                    date = line.strip()
                if line_sp[3] != "-":  # 3 is gene, 4 is feature
                    if chosen_variants <= 10:
                        chosen_variants += 1
                        # print(line_sp)
                        if line_sp[3] != "Gene" or line_sp[4] != "Feature":
                            # so the first header is 
                            info[index] = f"({uuid.uuid1().int}, {person_id}, '{date}', 4281995, '{line_sp[3]}', 4048365, '{line_sp[4]}', NULL)" 
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
    # header needs to be add manually
    with open(file, "w") as f:
        for line_info in info.values():
            f.write(f"{str(line_info)}")
    print(f"workflow: {file} contains {len(info.values())} variants.")

# chr, positie, id (welk id? ref, alt, INFO(Medgen, clnsig))
                

# def main():
    # vcf = "/Users/lean/PGPC_0026_S1.flt.vcf"
    # # info = read_file(vcf) # info is dict with variants that contains missense_variant
    # vcfs = ["/Users/lean/data_integratie/Filtered_chr21_PGPC-3_annotated.vcf", "/Users/lean/data_integratie/Filtered_chr21_PGPC-26_annotated.vcf"]
    # for vcf in vcfs:
    #     info = read_file_filter(vcf)
    # write_file("filter_chr21_PGPC_0026.vcf", info)

# main()
