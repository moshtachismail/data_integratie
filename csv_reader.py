# Lean
import uuid
def read_csv_filter(file, data):
    """gets the condition occurences from a patient
    Args:
        file (path): path to PGPC csv file for file name
        data (list): list with the content of a csv file
    Returns:
        conditions: dict with conditions and symptoms
    """
    conditions = {}
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
    """Get the conditions from the dict conditions to retrieve the 
    conditions, it is hardcoded due to fact that we need to add a 
    specific condition_concept_id from athena.
    Args:
        conditions (dict): ('26', ['Bilateral retinal detachments 
        and cataracts', 'Osteoarthritis'])
    Returns:
        cc: dict with the format of the measurements to insert it in the
        postgres database without writing a new functin.
    """
    c = {}
    i = 0
    for patient, condition in conditions.items():
        cc = {}
        print(patient, condition, "ttest")
        for con in condition:
            c[patient] = []
            # its not clean to set the concept_id hardcoded here, but
            # we need a workflow, cleaner to get it by an api 
            if con == "Bilateral retinal detachments and cataracts":
                # condition startdate is not available in our patients
                # condition_type_concept_id = 2022-05-30 (yyyy-MM-dd)
                cc[i] = f"({int(str(uuid.uuid1().int)[-9:])}, {patient}, 4147507, '{con}', '2022-05-30', 32020)"
                i +=1
                # (condition_occurrence_id, person_id, condition_concept_id, condition_source_value, condition_start_date, condition_type_concept_id)
            if con == "Osteoarthritis":
                # con is the condition_occurrence of the patient
                cc[i] = f"({int(str(uuid.uuid1().int)[-9:])}, {patient}, 40320318, '{con}', '2022-05-30', 32020)"
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
        print(f"workflow: File not found {file}, try another file.")
        exit(1)