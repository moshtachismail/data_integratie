def csvreader(file):
    """
    Function reads PGPC csv files, returns dict with 
    column name key & column value.
    Input: File location string
    Returns: Dict column name - column value pairs
    """
    with open(file, "r") as file:
        for i, line in enumerate(file):
            line = line.replace('\n', '')
            if i == 0:
                columns = line.split(',')
            elif i == 1:
                values = line.split(',')
            elif not line.startswith("PGPC"):
                columns.extend(line.split(',')[1:])
            else: 
                values.extend(line.split(',')[1:])
        column_value_pair = dict(zip(columns, values))
    return column_value_pair

def get_data(column_value_pair):
    """
    Function uses Dict with column name - column value pairs
    to generate a string according to OMOP (?) format to insert 
    into a database.
    PARAM: Dict column_value_pair column name - column value
    RETURN: String according to OMOP (?) format to insert into a database.
    """

    # Participant, Birth year, birth month, MAKEN OP BASIS VAN SEX (8507M, 8532F), 
    # Sex, 4147507, 45532670, Ethnicity
    values = ["Participant", "Birth year", "Birth month"]
    returnstring = ""

    # For loop to get the first 3 standard values, rest is special
    for i in values:            
        if column_value_pair.get(i) != None:
            if i == "Participant":
                returnstring += column_value_pair.get(i).split("-")[1] + ",'" 
                + column_value_pair.get(i) + "',"
            else:
                returnstring += column_value_pair.get(i) + ","
        else:
            returnstring += ","

    if column_value_pair.get("Sex") != None:
        if "m" in column_value_pair.get("Sex").lower():
            gender_concept_id = "8507,'" + column_value_pair.get("Sex") + "',"
        else: 
            gender_concept_id = "8532,'" + column_value_pair.get("Sex") + "',"
        returnstring += gender_concept_id
    else:
        returnstring += ",,"

    if column_value_pair.get("Ethnicity") != None:
        returnstring += 2*("45532670,'" + column_value_pair.get("Ethnicity") + "',")
        returnstring = returnstring[:-1]
    else:
        returnstring += ','

    return returnstring

def main():
    files = ["PGPC-3.csv", "PGPC-25.csv", "PGPC-26.csv"]
    for i in files:   
        column_value_pair = csvreader(i)
        db_insert_string = get_data(column_value_pair)
        print(db_insert_string)


main()


