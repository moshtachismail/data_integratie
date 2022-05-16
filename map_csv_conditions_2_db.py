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
        print(column_value_pair)
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
    values = ["Conditions or Symptom"]
    returnstring = ""

    # For loop to get the first 3 standard values, rest is special
    for i in values:            
        if column_value_pair.get(i) != None:
            print(column_value_pair.get(i))
    # return returnstring

def main():
    # files = ["PGPC-3.csv", "PGPC-25.csv", "PGPC-26.csv"]
    files = ["PGPC-26.csv"]
    for i in files:   
        column_value_pair = csvreader(i)
        db_insert_string = get_data(column_value_pair)
        # print(db_insert_string)


main()


