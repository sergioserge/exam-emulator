import unittest
import sqlite3
from sql_manager import SqlManager
from data_container import Question, Results


class TestVariables:
    """Class for various variables for unit testing purposes only."""

    def __init__(self):
        self.entry_field_content = "test_table"
        self.selected_results_table = "test_table"
        self.selected_database = "test_table_db"
        self.selected_database_copy = "test_table_db_copy"
        self.right_answers = "[1, 0, 1, 0, 1]"
        self.user_answers_right = "[1, 0, 1, 0, 1]"
        self.user_answers_wrong = "[0, 0, 1, 0, 1]"


class TestSqlManager(unittest.TestCase):
    """Unit Test Class."""

    @staticmethod
    def setUpDatabase():
        """Creates new database table."""
        test_obj = TestVariables()
        sql_m = SqlManager()
        sql_m.sql_create_exam_database(test_obj.entry_field_content)

    @staticmethod
    def setUpResultsTable():
        """Creates new results table."""
        test_obj = TestVariables()
        results_table = test_obj.selected_results_table
        sql_m = SqlManager()
        sql_m.sql_create_results_table(results_table)

    @staticmethod
    def setUpDatabaseCopy():
        """Creates new copy of the selected database table."""
        test_obj = TestVariables()
        selected_database = test_obj.selected_database
        sql_m = SqlManager()
        sql_m.sql_create_database_copy(selected_database)

    def setUpInsertRow(self, table_name):
        """Inserts a row into the passed table(can be database or database copy table)."""
        row_id = self.setUpRowID(table_name)
        new_question = Question(row_id, "q", "a1", "a2", "a3", "a4", "a5", [0, 1, 0, 1, 0], 2)
        new_question = [new_question]
        sql_m = SqlManager()
        sql_m.sql_insert_new_questions(new_question, table_name)
        query_should = [row_id, "q", "a1", "a2", "a3", "a4", "a5", "[0, 1, 0, 1, 0]", 2]
        query_question_objects = sql_m.sql_get_database_content(table_name)
        q_obj = query_question_objects[-1]
        query_real = [q_obj.row_id,
                      q_obj.question,
                      q_obj.answer1,
                      q_obj.answer2,
                      q_obj.answer3,
                      q_obj.answer4,
                      q_obj.answer5,
                      q_obj.right_answers,
                      q_obj.firsts]

        return query_real, query_should

    @staticmethod
    def setUpRowID(table_name):
        """Queries the last row_id from passed table and returns that value + 1 as an integer value."""
        try:
            sql_m = SqlManager()
            row_id = sql_m.sql_get_last_row_id(table_name) + 1
        except sqlite3.OperationalError:
            print("First row_id was set to 1")
            row_id = 1

        return row_id

    @staticmethod
    def setUpResultsObject(row_id, right_answers, user_answer, score, firsts=2):
        """Creates and returns an Results object with the passed values."""
        results_obj = Results(row_id, "question", right_answers, user_answer, score, "0.5", firsts)
        results_obj = [results_obj]

        return results_obj

    @staticmethod
    def tearDownTable(table_name):
        """Deletes a table with the passed name."""
        sql_m = SqlManager()
        sql_m.sql_delete_table(table_name)

    @staticmethod
    def tearDownInsertRow(table_name, row_id):
        """Deletes a row from the passed table with the passed row_id."""
        sql_m = SqlManager()
        sql_m.sql_delete_row(table_name, row_id)

    def test_create_exam_database(self):
        """Creates a database table with certain name, queries all tables
        and checks that the queried last table_name equals the initial name.
        """
        sql_m = SqlManager()
        test_obj = TestVariables()
        table_name = test_obj.entry_field_content
        sql_m.sql_create_exam_database(table_name)
        queried_table_name = sql_m.sql_get_all_tables()
        queried_table_name = [tables.table_name for tables in queried_table_name][-1][-1]
        self.assertEqual(table_name + "_db", queried_table_name)
        print("test_create_exam_database: successful")
        self.tearDownTable(table_name + "_db")

    def test_create_results_table(self):
        """Creates a results table with certain name, queries all tables
        and checks that the queried last table_name equals the initial name.
        """
        sql_m = SqlManager()
        test_obj = TestVariables()
        table_name = test_obj.entry_field_content
        sql_m.sql_create_results_table(table_name)
        queried_table_name = sql_m.sql_get_all_tables()
        queried_table_name = [tables.table_name for tables in queried_table_name][-1][-1]
        self.assertEqual(table_name, queried_table_name)
        print("test_create_results_table: successful")
        self.tearDownTable(table_name)

    def test_create_database_copy(self):
        """Creates a database copy table with certain name, queries all tables
        and checks that the queried last table_name equals the initial name.
        """
        test_obj = TestVariables()
        selected_database = test_obj.selected_database
        self.setUpDatabase()
        sql_m = SqlManager()
        sql_m.sql_create_database_copy(selected_database)
        queried_table_name = sql_m.sql_get_all_tables()
        queried_table_name = [tables.table_name for tables in queried_table_name][-1][-1]
        self.assertEqual(selected_database + "_copy", queried_table_name)
        print("test_create_database_copy: successful")
        self.tearDownTable(selected_database)
        self.tearDownTable(selected_database + "_copy")

    def test_sql_insert_new_questions(self):
        """Creates a database table, inserts a row into it, queries the last row
        and checks if it equals the arguments passed as values into the sql_insert_new_questions function.
        """
        self.setUpDatabase()
        test_obj = TestVariables()
        selected_database = test_obj.selected_database
        query_real, query_should = self.setUpInsertRow(selected_database)
        self.assertEqual(query_should, query_real)
        print("test_sql_insert_new_questions: successful")
        self.tearDownInsertRow(selected_database, query_real[0])
        self.tearDownTable(selected_database)

    def test_sql_insert_new_results(self):
        """Creates a database and results tables, inserts a row into the database table
        and creates a database copy of the database table. Queries last row_id + 1 and creates a Results object to
        pass it to the sql_insert_new_results. Then queries last row of the results table and compares it
        to the variables initially passed.
        """
        test_obj = TestVariables()
        selected_database = test_obj.selected_database
        selected_results_table = test_obj.selected_results_table
        selected_database_copy = test_obj.selected_database_copy
        self.setUpDatabase()
        self.setUpResultsTable()
        self.setUpInsertRow(selected_database)
        self.setUpDatabaseCopy()
        answers_right = test_obj.right_answers
        user_answers_right = test_obj.user_answers_right
        user_answers_wrong = test_obj.user_answers_wrong
        row_id = self.setUpRowID("database_table_db_db")
        results = self.setUpResultsObject(row_id, answers_right, user_answers_right, 1, firsts=2)
        sql_m = SqlManager()
        sql_m.sql_insert_new_results(results, selected_results_table)
        results_objects_list = sql_m.sql_get_results_content(selected_results_table)
        results_vars_list = results_objects_list[-1]
        results_vars_query = [results_vars_list.row_id,
                              results_vars_list.question,
                              results_vars_list.right_answers,
                              results_vars_list.user_answers,
                              results_vars_list.score,
                              results_vars_list.time_track,
                              results_vars_list.firsts]

        results_should_right = [row_id, "question", answers_right, user_answers_right, 1, 0.5, 2]
        results_should_wrong = [row_id, "question", answers_right, user_answers_wrong, 1, 0.5, 2]
        self.assertEqual(results_should_right, results_vars_query)
        self.assertNotEqual(results_should_wrong, results_vars_query)
        print("test_sql_insert_new_results: successful")
        self.tearDownTable(selected_database)
        self.tearDownTable(selected_results_table)
        self.tearDownTable(selected_database_copy)

    def test_sql_subtract_firsts(self):
        """Creates a database table, inserts a row into it and creates a database copy of the database table.
        Queries last row_id, adds 1 to it and creates a Results object to pass it to the sql_insert_new_results. The
        firsts variable is subtracted by one with the sql_subtract_firsts function.
        Then queries the row with that row_id and checks that firsts value is minus 1.
        """
        test_obj = TestVariables()
        selected_database = test_obj.selected_database
        selected_database_copy = test_obj.selected_database_copy
        self.setUpDatabase()
        self.setUpInsertRow(selected_database)
        self.setUpDatabaseCopy()
        row_id = self.setUpRowID(selected_database_copy) - 1
        sql_m = SqlManager()
        new_question_obj_list = sql_m.sql_get_database_content(selected_database_copy)
        new_question_obj = new_question_obj_list[-1]
        firsts_before_update = new_question_obj.firsts
        sql_m.sql_subtract_firsts(row_id, selected_database_copy)
        new_question_obj_list = sql_m.sql_get_database_content(selected_database_copy)
        new_question_obj = new_question_obj_list[-1]
        firsts_after_update = new_question_obj.firsts
        firsts_should_right = 1
        self.assertEqual(firsts_should_right, firsts_after_update)
        self.assertNotEqual(firsts_before_update, firsts_after_update)
        print("test_sql_subtract_firsts: successful")
        self.tearDownTable(selected_database)
        self.tearDownTable(selected_database_copy)

    def test_sql_add_firsts(self):
        """Creates a database table, inserts a row into it and creates a database copy of the database table.
        Queries last row_id, adds 1 to it and creates a Results object to pass it to the sql_insert_new_results.
        Adds 1 to the firsts variable with the sql_add_firsts function.
        Then queries the row with that row_id and checks that firsts value is plus 1.
        """
        test_obj = TestVariables()
        selected_database = test_obj.selected_database
        selected_database_copy = test_obj.selected_database_copy
        self.setUpDatabase()
        self.setUpInsertRow(selected_database)
        self.setUpDatabaseCopy()
        row_id = self.setUpRowID(selected_database_copy) - 1
        sql_m = SqlManager()
        new_question_obj_list = sql_m.sql_get_database_content(selected_database_copy)
        new_question_obj = new_question_obj_list[-1]
        firsts_before_update = new_question_obj.firsts
        sql_m.sql_add_firsts(row_id, selected_database_copy)
        new_question_obj_list = sql_m.sql_get_database_content(selected_database_copy)
        new_question_obj = new_question_obj_list[-1]
        firsts_after_update = new_question_obj.firsts
        firsts_should_right = 3
        self.assertEqual(firsts_should_right, firsts_after_update)
        self.assertNotEqual(firsts_before_update, firsts_after_update)
        print("test_sql_subtract_firsts: successful")
        self.tearDownTable(selected_database)
        self.tearDownTable(selected_database_copy)
