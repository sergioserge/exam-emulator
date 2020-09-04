import sqlite3
from data_container import TableNames, Question, Results


class SqlManager:
    """Class to query and manipulate data in the sqlite3 database.

    Attributes:
        table_names(list): a list of table names.

    """

    def __init__(self):
        self.table_names = []

    @staticmethod
    def sql_query(query_str):
        """Connects, initializes a transaction and closes connection after that.
        The exact query depends on the query_str variable passed by other functions.
        """
        connection = sqlite3.connect("Exam_Emulator.db")
        cursor = connection.cursor()
        cursor.execute(query_str)
        connection.commit()
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    @staticmethod
    def sql_query_with_values(query_str, value):
        """Similar to sql_query but with a more complex sql transaction."""
        connection = sqlite3.connect("Exam_Emulator.db")
        cursor = connection.cursor()
        cursor.execute(query_str, value)
        connection.commit()
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    def sql_get_row(self, table_name, row_id):
        """Queries from certain database or database copy table certain row and passes as list of one Question object."""
        query_str = "SELECT * FROM " + str(table_name) + " WHERE row_id = " + str(row_id)

        query_str = str(query_str)
        table_content = self.sql_query(query_str)
        table_content_list = []
        for row in table_content:
            table_content_list.append(Question(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        return table_content_list

    def sql_get_all_tables(self):
        """Queries from the main sqlite3 database the names of all tables and passes as list of TableNames objects."""
        query_str = "SELECT tbl_name FROM sqlite_master"
        query_str = str(query_str)
        all_tables = self.sql_query(query_str)
        all_tables_list = []
        for table_name in all_tables:
            all_tables_list.append(TableNames(table_name))

        return all_tables_list

    def sql_create_exam_database(self, table_name):
        """Creates new table with needed columns to save a question and possible answers(=question set)."""
        query_str = "CREATE TABLE " + str(table_name) + "_db" + \
                    """
                    (row_id INTEGER PRIMARY KEY,
                    question TEXT,
                    answer_1 TEXT,
                    answer_2 TEXT,
                    answer_3 TEXT,
                    answer_4 TEXT,
                    answer_5 TEXT,
                    answer_states TEXT,
                    firsts INTEGER)
                    """
        query_str = str(query_str)
        self.sql_query(query_str)

    def sql_create_results_table(self, table_name):
        """Creates new table with needed columns to save exam results."""
        query_str = "CREATE TABLE " + str(table_name) + \
                    """
                    (row_id INTEGER,
                    question TEXT,
                    right_answer_seq TEXT,
                    user_answer_seq TEXT,
                    score INTEGER,
                    time_track REAL,
                    firsts INTEGER)
                    """
        query_str = str(query_str)
        self.sql_query(query_str)

    def sql_create_database_copy(self, selected_database):
        """Creates a copy of database table currently selected by the user.
            Variable firsts (default = 2) is going to be -1 if answered correctly.
            The question is going to be deleted finally if firsts = 0.
            """
        selected_database = selected_database
        # Create a copy of the selected database to delete the right answered questions from it
        query_str = "CREATE TABLE " + str(selected_database) + "_copy" + " AS SELECT * FROM " + str(selected_database)
        query_str = str(query_str)
        self.sql_query(query_str)

    def sql_get_last_row_id(self, table_name):
        """Queries the last row in certain table and returns an integer value."""
        query_str = "SELECT row_id FROM " + str(table_name)
        query_str = str(query_str)
        query = self.sql_query(query_str)
        if len(query) > 0:
            last_row_id = self.sql_query(query_str)[-1][0]
        else:
            last_row_id = 0

        return last_row_id

    def sql_delete_table(self, table_name):
        """Deletes the whole table with certain name."""
        query_str = "DROP TABLE " + str(table_name)
        query_str = str(query_str)
        self.sql_query(query_str)

    def sql_insert_new_questions(self, variables, selected_database):
        """Inserts new question set into the user selected database table."""
        variables = variables[0]
        selected_database = selected_database
        query_str = "INSERT INTO " + str(selected_database) + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

        insert_content = (int(variables.row_id),
                          str(variables.question),
                          str(variables.answer1),
                          str(variables.answer2),
                          str(variables.answer3),
                          str(variables.answer4),
                          str(variables.answer5),
                          str(variables.right_answers),
                          int(variables.firsts))

        query_str = str(query_str)
        self.sql_query_with_values(query_str, insert_content)

    def sql_insert_new_results(self, results, selected_results_table):
        """Inserts the results of the last exam question into the user selected results table."""
        results = results[0]
        query_str = "INSERT INTO " + str(selected_results_table) + " VALUES (?, ?, ?, ?, ?, ?, ?)"

        insert_content = (int(results.row_id),
                          str(results.question),
                          str(results.right_answers),
                          str(results.user_answers),
                          int(results.score),
                          float(results.time_track),
                          int(results.firsts))

        query_str = str(query_str)
        self.sql_query_with_values(query_str, insert_content)

    def sql_delete_row(self, table_name, row_id):
        """Deletes certain row from certain table."""
        query_str = "DELETE FROM " + str(table_name) + " WHERE row_id = " + str(row_id)
        query_str = str(query_str)
        self.sql_query(query_str)

    def sql_get_database_content(self, table_name):
        """Queries from certain database or database copy table all rows and passes as list of Question objects."""
        query_str = "SELECT * FROM " + str(table_name)

        query_str = str(query_str)
        table_content = self.sql_query(query_str)
        table_content_list = []
        for row in table_content:
            table_content_list.append(Question(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        return table_content_list

    def sql_get_results_content(self, table_name):
        """Queries from certain results table all rows and passes as list of Results objects."""
        query_str = "SELECT * FROM " + str(table_name)

        query_str = str(query_str)
        table_content = self.sql_query(query_str)
        table_content_list = []
        for row in table_content:
            table_content_list.append(Results(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        return table_content_list

    def sql_subtract_firsts(self, row_id, selected_database_copy):
        """Subtracts '1' from the firsts variable."""
        query_str = "Update " + str(selected_database_copy) + " SET firsts = firsts - 1 WHERE row_id = " + str(row_id)
        query_str = str(query_str)
        self.sql_query(query_str)

    def sql_add_firsts(self, row_id, selected_database_copy):
        """Adds '1' to the firsts variable."""
        query_str = "Update " + str(selected_database_copy) + " SET firsts = firsts + 1 WHERE row_id = " + str(row_id)
        query_str = str(query_str)
        self.sql_query(query_str)
