# Lean
import uuid
def read_csv_filter(file, data):
    """gets the condition occurences from a patient
    Args:
        file (_type_): _description_
    """
    conditions = {}
    # with open(f"{file[:-4]}_filtered.csv", "w") as ff: # write the 
    # filtered content
    
    for index, data_l in enumerate(data):
        for d in data_l[0].split(","):
            # if d == "Blood type":  # is only present in blood type
                # ff.write(f"{data_l[0]}\n{data[index + 1][0]}\n")
            if d == "Conditions or Symptom":
                conditions[file[:-4].split('/')[-1].split('_')[0].split("-")[1]] = []
                # expected file format
                # /Users/lean/Library/CloudStorage/OneDrive-Persoonlijk/
                # School/Han - Bio informatica/BI10 Data Science en 
                # onderzoeksproject/Data_integratie/data_integratie_git
                # /data_integratie/PGPC-26.csv

                for i in range(len(data)):
                    try:
                        if data[index + i + 1][0].\
                        startswith(f"{file[:-4].split('/')[-1].split('_')[0]}"): # indicates a row
                            # ff.write(f"{data[index + i + 1][0]}\n")
                            conditions[file[:-4].split('/')[-1].split('_')[0].split("-")[1]].append(data[index + i + 1][0].split(",")[1])

                        else:
                            break
                    except IndexError:
                        pass
    return conditions


def set_conditions(conditions):
    c = {}
    i = 0
    for patient, condition in conditions.items():
        cc = {}
        for con in condition:
            c[patient] = []
            # its not clean to set the concept_id hardcoded here, but
            # we need a workflow, cleaner to get it by an api 
            # print(patient, condition)
            # print(conditions)/
            if con == "Bilateral retinal detachments and cataracts":
                cc[i] = f"{uuid.uuid1().int}, {patient}, 4147507, {con}, NULL", "NULL"
                i +=1
                # cc += str(t)
                # (condition_occurrence_id, person_id, condition_concept_id, condition_source_value, condition_start_date, condition_type_concept_id)
            if con == "Osteoarthritis":
                cc[i] = f"{uuid.uuid1().int}, {patient}, 40320318, {con}, NULL", "NULL"
                i+=1
        
        return cc



def read_csv(file):
    """Read a PDF file and write the results to a csv file in list
    Args:
        file (_type_): _description_
    """
    data = []
    # write temp file to csv, can be removed.
    try:
        with open(file, "r") as f:
            for linef in f:
                data.append([linef.strip()])
        
        return set_conditions(read_csv_filter(file, data))
    except FileNotFoundError:
        print(f"File not found {file}, try another file.")
        exit(1)


def main():
    files = ["/Users/lean/Library/CloudStorage/OneDrive-Persoonlijk/School/Han - Bio informatica/BI10 Data Science en onderzoeksproject/Data_integratie/data_integratie_git/data_integratie/PGPC-3.csv", "/Users/lean/Library/CloudStorage/OneDrive-Persoonlijk/School/Han - Bio informatica/BI10 Data Science en onderzoeksproject/Data_integratie/data_integratie_git/data_integratie/PGPC-26_filtered.csv"]
    files = ["/Users/lean/Library/CloudStorage/OneDrive-Persoonlijk/School/Han - Bio informatica/BI10 Data Science en onderzoeksproject/Data_integratie/data_integratie_git/data_integratie/PGPC-3.csv", "/Users/lean/Library/CloudStorage/OneDrive-Persoonlijk/School/Han - Bio informatica/BI10 Data Science en onderzoeksproject/Data_integratie/data_integratie_git/data_integratie/PGPC-26.csv"]
    # print(read_csv(files[1]))




main()