# author: D. Hildebrand
def csvreader(file_iter):
    """Reads PGPC csv files, returns dict with column name key & column value.
    Args:
        file_iter (path): path to pgpc csv file.
    Returns:
        dict: column name - column value pairs
    """
    vallist = []
    with open(file_iter, "r") as file_iter:
        for i, line in enumerate(file_iter):
            line = line.replace('\n', '')
            # First two lines of file
            if i == 0:
                columns = line.split(',')
            elif i == 1:
                values = line.split(',')
            # If the line does not start with PGPC, it's a value
            # and gets added to 'columns' var
            elif not line.startswith("PGPC"):
                columns.extend(line.split(',')[1:])
                if vallist:
                    # List comprehension line
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
    """Uses dict with column name - column value pairs to generate
    a string according to OMOP format to insert into a database.
    Args:
        column_value_pair (dict): column name - column value
    Returns:
        str: str according to OMOP format to insert into the database
    """
    values = ["Participant", "Birth year", "Birth month"]
    returnstring = ""
    # For loop to get the first 3 values; they don't need special handling
    for i in values:
        if column_value_pair.get(i) != None and column_value_pair.get(i) != "":
            if column_value_pair.get(i).startswith("PGPC"):
                returnstring += f"'{column_value_pair.get(i).split('-')[1]}', "
                "'{column_value_pair.get(i)}', "
            else:
                returnstring += f"'{column_value_pair.get(i)}', "
        else:
            returnstring += "NULL,"
    # Determine 'sex'; if not M it's F. If empty, add NULL
    if column_value_pair.get("Sex") != None:
        if "m" in column_value_pair.get("Sex").lower():
            gender_concept_id = f"8507, '{column_value_pair.get('Sex')}', "
        else:
            gender_concept_id = f"8532, '{column_value_pair.get('Sex')}', "
        returnstring += gender_concept_id
    else:
        returnstring += ","+"NULL"+","
    # Determine the ethnicity. Return Athena ethnicity code for white
    # and if the colour isn't white, add 404 ethnicity unknown
    if column_value_pair.get("Ethnicity") != None and column_value_pair. \
            get("Ethnicity") != "":
        if column_value_pair.get("Ethnicity") == "White":
            returnstring += 2 * \
                ("45532670, '" + column_value_pair.get("Ethnicity") + "',")
            returnstring = returnstring[:-1]
        else:
            returnstring += 2 * \
                ("404, '" + column_value_pair.get("Ethnicity") + "',")
            # if 404 ethnicity unknown
            returnstring = returnstring[:-1]

    returnstring = "(" + returnstring + ")"
    return returnstring


def person_all(files):
    """Creates a command string to insert into the database. 
    Calls csvreader and get_data functions.
    Args:
        files (list): list containing paths to CSV PGPC files.
    Returns:
        list: list of command strings to insert into the database.
    """

    db_insert_strings = []
    for i in files:
        column_value_pair = csvreader(i)
        db_insert_strings.append(get_data(column_value_pair))
    return db_insert_strings
