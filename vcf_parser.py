# Lean

def read_file(file):
    info = {}
    with open(file, "r") as f:
        for index, line in enumerate(f):
            # if index == 28:
            #     # print(line.strip().split("\n"))
            #     line_sp = line.split("\t")
            #     print(line_sp[7].split(";")[9])
            #     if line_sp[7].split(";")[9].endswith("|missense_variant"):
            #         info[index] = line_sp
            # print(line.strip().split("\n"))
            line_sp = line.split("\t")
            try:
                if line_sp[0] == "chr21":  # get chr21
                    info[index] = line
                # if line_sp[7].split(";")[9].endswith("|missense_variant"):
                #     info[index] = line
            except IndexError:
                pass
    return info

def write_file(file, info):
    # the standard info is written manually to the vcf file
    # header needs to be add manually
    with open(file, "w") as f:
        for line_info in info.values():
            f.write(f"{str(line_info)}")
    print(f"Filtered vcf file contains {len(info.values())} variants.")

# chr, positie, id (welk id? ref, alt, INFO(Medgen, clnsig))
                

def main():
    vcf = "/Users/lean/PGPC_0026_S1.flt.vcf"
    info = read_file(vcf)  # info is dict with variants that contains missense_variant
    write_file("filter_chr21_PGPC_0026.vcf", info)

main()
