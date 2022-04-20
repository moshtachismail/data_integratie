"""Parse a pdf file from PGPC to a pdf file with filtered content.
PDF files are from:
    https://personalgenomes.ca/data
"""
# Lean
import tabula


def write_csv(file, data):
    """write the perseons profile and Contions or Symptoms to a CSV file
    Args:
        file (_type_): _description_
    """
    with open(f"{file[:-4]}_filtered.csv", "w") as ff: # write the 
    # filtered content
        for index, data_l in enumerate(data):
            for d in data_l[0].split(","):
                if d == "Blood type":  # is only present in blood type
                    ff.write(f"{data_l[0]}\n{data[index + 1][0]}\n")
                if d == "Conditions or Symptom":
                    ff.write(f"{data_l[0]}\n")
                    for i in range(len(data)):
                        if data[index + i + 1][0].\
                        startswith(f"{file[:-4]}"): # indicates a row
                            ff.write(f"{data[index + i + 1][0]}\n")
                        else:
                            break


def read_pdf(file):
    """Read a PDF file and write the results to a csv file in list
    Args:
        file (_type_): _description_
    """
    # convert PDF into CSV
    try:
        tabula.convert_into(file, f"{file[:-4]}.csv", output_format="csv", 
            pages='all')
    except FileNotFoundError:
        print(f"File not found {file}, try another file.")
        exit(1)

    data = []
    # write temp file to csv, can be removed.
    try:
        with open(f"{file[:-4]}.csv", "r") as f:
            for linef in f:
                data.append([linef.strip()])
        write_csv(file, data)
    except FileNotFoundError:
        print(f"File not found {file}, try another file.")
        exit(1)

                        
def main():
    files = ["PGPC-3.pdf", "PGPC-25.pdf", "PGPC-26.pdf"]
    for file in files:
        read_pdf(file)


main()
