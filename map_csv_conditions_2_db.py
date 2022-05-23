def csvreader(file_iter):
    """
    Function reads PGPC csv files, returns dict with 
    column name key & column value.
    Input: File location string
    Returns: Dict column name - column value pairs
    """
    vallist = []
    with open(file_iter, "r") as file_iter:
        for i, line in enumerate(file_iter):
            line = line.replace('\n', '')

            if i == 0:
                columns = line.split(',')

            elif i == 1:
                values = line.split(',')

            elif not line.startswith("PGPC"):
                columns.extend(line.split(',')[1:])
                if vallist:
                    vallist = [i for i in vallist if i]
                    values.extend(vallist)
                    vallist = []

            elif line.startswith("PGPC"):
                vallist.extend(line.split(',')[1:])

            else: 
                values.extend(vallist)

        column_value_pair = dict(zip(columns, values))
    return column_value_pair

def get_data(column_value_pair):
    """
    Function uses Dict with column name - column value pairs
    to generate a string according to OMOP (?) format to insert 
    into a database.
    PARAM: Dict column_value_pair column name - column value
    RETURN: String according to OMOP format to insert into a database.
    """
    values = ["Participant", "Birth year", "Birth month"]
    returnstring = ""

    # For loop to get the first 3 standard values, rest is special
    for i in values:            
        if column_value_pair.get(i) != None and column_value_pair.get(i) != "":
            if column_value_pair.get(i).startswith("PGPC"):
                returnstring += column_value_pair.get(i).split("-")[1] + "," + column_value_pair.get(i) + ","
            else:
                returnstring += column_value_pair.get(i) + ","
        else:
            returnstring += "NULL,"

    if column_value_pair.get("Sex") != None:
        if "m" in column_value_pair.get("Sex").lower():
            gender_concept_id = "8507," + column_value_pair.get("Sex") + ","
        else: 
            gender_concept_id = "8532" + column_value_pair.get("Sex") + ","
        returnstring += gender_concept_id
    else:
        returnstring += ","+"NULL"+","

    if column_value_pair.get("Ethnicity") != None and column_value_pair.get("Ethnicity") != "":
        if column_value_pair.get("Ethnicity") == "White":
            returnstring += 2*("45532670," + column_value_pair.get("Ethnicity") + ",")
            returnstring = returnstring[:-1]
        else:
            returnstring += 2*("404," + column_value_pair.get("Ethnicity") + ",")
            returnstring = returnstring[:-1]

    returnstring = "(" + returnstring + ")"
    return returnstring

def person_all(files):
    """
    Function to create DB insert strings. Calls csvreader and get_data functions.
    PARAM: List of PGPC CSV file locations.
    RETURN: List of DB insert strings.
    """
    db_insert_strings = []
    for i in files:   
        column_value_pair = csvreader(i)
        db_insert_strings.append(get_data(column_value_pair))
    return db_insert_strings
