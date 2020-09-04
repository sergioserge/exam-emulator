import unittest
from sql_manager import SqlManager
from app_interface import AppInterface
from data_container import SettingVariables, Question


class TestUserInterface(unittest.TestCase):
    """Unittest class. With test variables as class variables."""
    test_table_name = "test_table"
    test_database_name = "test_table_db"
    test_results_name = "test_table"
    test_database_copy_name = "test_table_db_copy"

    @staticmethod
    def setUpDatabase(table_name):
        """Creates a new database table."""
        gui_w = AppInterface()
        gui_w.create_exam_database(table_name)

    @staticmethod
    def setUpResultsTables(table_name):
        """Creates a new results and a database_copy tables."""
        SettingVariables.selected_database = table_name + "_db"
        gui_w = AppInterface()
        gui_w.create_results_tables(table_name)

    @staticmethod
    def setUpDatabaseCopy(table_name):
        """Creates a new database_copy table only."""
        sql_m = SqlManager()
        sql_m.sql_create_database_copy(table_name)

    @staticmethod
    def setUpQueryCertainTable(object_position, item_position):
        # todo modify the tests, to use the setUpQueryResults() Function instead.
        """Queries all table names as a list of TableNames objects, transforms to a list ob tuples with table names
            and selects a certain tuple and position amid the tuple.
        """
        sql_m = SqlManager()
        all_tables = sql_m.sql_get_all_tables()
        all_tables = [tables.table_name for tables in all_tables]
        queried_tables = all_tables[object_position][item_position]

        return queried_tables

    @staticmethod
    def setUpQueryResults(table_name, object_position):
        """Queries a results table as list of Results objects and returns attribute values of a certain object.
            The object is dependent on the passed number of row(=object position) amid the list of all objects.
            """
        sql_m = SqlManager()
        results_list = sql_m.sql_get_results_content(table_name)
        r_obj = results_list[object_position]
        results = [r_obj.row_id, r_obj.question, r_obj.right_answers, r_obj.user_answers, r_obj.score, 0.0, r_obj.firsts]

        return results

    @staticmethod
    def setUpQueryQuestion(table_name, object_position):
        """Queries a database or database_copy table as list of Question objects and returns attribute values of certain
            object. The object is dependent on the passed number of row(=object position) amid the list of all objects.
        """
        sql_m = SqlManager()
        query_question_objects = sql_m.sql_get_database_content(table_name)
        q_obj = query_question_objects[object_position]
        query_real = [q_obj.row_id,
                      q_obj.question,
                      q_obj.answer1,
                      q_obj.answer2,
                      q_obj.answer3,
                      q_obj.answer4,
                      q_obj.answer5,
                      q_obj.right_answers,
                      q_obj.firsts]

        return query_real

    @staticmethod
    def setUpPopulateQuestions(row_id, database_name):
        """Insert values into a database or database_copy table."""
        question = "question"
        answer1 = "answer1"
        answer2 = "answer2"
        answer3 = "answer3"
        answer4 = "answer4"
        answer5 = "answer5"
        right_answers = [1, 0, 1, 0, 1]
        variables = Question(row_id, question, answer1, answer2, answer3, answer4, answer5, right_answers)
        variables = [variables]
        sql_m = SqlManager()
        sql_m.sql_insert_new_questions(variables, database_name)

    @staticmethod
    def setUpQuestionVariables():
        """Create a list of values which can be passed to a function which creates database or database_copy table."""
        question = "question"
        answer1 = "answer1"
        answer2 = "answer2"
        answer3 = "answer3"
        answer4 = "answer4"
        answer5 = "answer5"
        state_var1 = 1
        state_var2 = 0
        state_var3 = 1
        state_var4 = 0
        state_var5 = 1

        variables = [question, answer1, answer2, answer3, answer4, answer5, state_var1, state_var2, state_var3, state_var4, state_var5]

        return variables

    @staticmethod
    def tearDownTable(table_name):
        """Delete table with passed table name."""
        gui_w = AppInterface()
        gui_w.delete_table(table_name)

    def test_create_exam_database(self):
        """Create database table, query all tables and compare to the initial table name."""
        self.setUpDatabase(self.test_table_name)
        queried_last_table = self.setUpQueryCertainTable(-1, -1)

        self.assertEqual(self.test_database_name, queried_last_table)
        self.assertNotEqual(self.test_table_name, queried_last_table)

        self.tearDownTable(self.test_database_name)

    def test_create_results_tables(self):
        """Create results table, query all tables and compare to the initial table name."""
        self.setUpDatabase(self.test_table_name)
        self.setUpResultsTables(self.test_table_name)
        queried_last_table = self.setUpQueryCertainTable(-2, -1)
        queried_penultimate_table = self.setUpQueryCertainTable(-1, -1)

        self.assertEqual(self.test_table_name, queried_last_table)
        self.assertNotEqual(self.test_database_name, queried_last_table)
        self.assertNotEqual(self.test_database_copy_name, queried_last_table)
        self.assertEqual(self.test_database_copy_name, queried_penultimate_table)
        self.assertNotEqual(self.test_table_name, queried_penultimate_table)
        self.assertNotEqual(self.test_database_name, queried_penultimate_table)

        self.tearDownTable(self.test_table_name)
        self.tearDownTable(self.test_database_name)
        self.tearDownTable(self.test_database_copy_name)

    def test_show_all_tables(self):
        """Create some table, query all tables and compare to the initial table name."""
        gui_w = AppInterface()
        object_position = slice(0, None)
        item_position = slice(0, None)
        should_all_tables = self.setUpQueryCertainTable(object_position, item_position)
        queried_all_tables = gui_w.show_all_tables()
        self.assertEqual(should_all_tables, queried_all_tables)
        self.assertNotEqual(self.test_table_name, queried_all_tables)

    def test_set_up_settings(self):
        """Queries 3 kinds of tables: database, results, database_copy. Queries all_tables and separate them into
            same kinds. Compare each 2 lists if they are the same.
        """
        gui_w = AppInterface()
        database_list, results_list, database_copy_list = gui_w.set_up_settings()
        should_database_list = [database for database in database_list if "_db" in database and "_db_copy" not in database]
        should_results_list = [results for results in results_list if "_db" not in results]
        should_database_copy_list = [database_copy for database_copy in database_copy_list if "_db_copy" in database_copy]
        self.assertEqual(should_database_list, database_list)
        self.assertEqual(should_results_list, results_list)
        self.assertEqual(should_database_copy_list, database_copy_list)

    def test_save_selected_database(self):
        """Changes the SettingVariables class variable selected_database, queries it and compares to initial name. """
        gui_w = AppInterface()
        gui_w.save_selected_database(self.test_database_name)
        settings_obj = SettingVariables()
        self.assertEqual(self.test_database_name, settings_obj.selected_database)

        settings_obj = SettingVariables()
        settings_obj.selected_database = "some_name"
        self.assertNotEqual(self.test_database_name, settings_obj.selected_database)

    def test_save_selected_results_table(self):
        """Changes the SettingVariables class variable selected_results_table, queries it and compares to initial name.
        """
        gui_w = AppInterface()
        gui_w.save_selected_results_table(self.test_results_name)
        settings_obj = SettingVariables()
        self.assertEqual(self.test_results_name, settings_obj.selected_results_table)

        settings_obj = SettingVariables()
        settings_obj.selected_results_table = "some_name"
        self.assertNotEqual(self.test_results_name, settings_obj.selected_results_table)

    def test_save_selected_database_copy(self):
        """Changes the SettingVariables class variable selected_database_copy, queries it and compares to initial name.
        """
        gui_w = AppInterface()
        gui_w.save_selected_database_copy(self.test_database_copy_name)
        self.assertEqual(self.test_database_copy_name, SettingVariables().selected_database_copy)

        settings_obj = SettingVariables()
        settings_obj.selected_database_copy = "some_name"
        self.assertNotEqual(self.test_database_copy_name, settings_obj.selected_database_copy)

    def test_delete_table(self):
        """Creates some tables, queries the last table name, deletes it and queries the last table again.
            Compares both last tables.
        """
        self.setUpDatabase(self.test_table_name + self.test_table_name)
        self.setUpDatabase(self.test_table_name)
        last_before_delete = self.setUpQueryCertainTable(-1, 0)
        self.assertEqual(self.test_database_name, last_before_delete)

        gui_w = AppInterface()
        gui_w.delete_table(self.test_database_name)
        last_after_delete = self.setUpQueryCertainTable(-1, 0)
        self.assertNotEqual(self.test_database_name, last_after_delete)

        self.tearDownTable(self.test_table_name + self.test_database_name)

    def test_save_new_question(self):
        """Inserts two new questions with same content(except row_id since primary key) to database table."""
        self.setUpDatabase(self.test_table_name)
        SettingVariables.selected_database = self.test_database_name
        variables = self.setUpQuestionVariables()

        gui_w = AppInterface()
        gui_w.save_new_question(*variables)
        query_first_insert = self.setUpQueryQuestion(self.test_database_name, 0)
        gui_w.save_new_question(*variables)
        query_second_insert = self.setUpQueryQuestion(self.test_database_name, 1)

        # Exclude index=0 since row_id is generated automatically as Primary Key
        self.assertEqual(query_first_insert[1::], query_second_insert[1::])
        self.assertNotEqual(query_first_insert, query_second_insert)

        self.tearDownTable(self.test_database_name)

    def test_delete_row(self):
        """Delete certain row in some table."""
        self.setUpDatabase(self.test_table_name)
        SettingVariables().selected_database = self.test_database_name
        variables = self.setUpQuestionVariables()

        gui_w = AppInterface()
        gui_w.save_new_question(*variables)
        query_first_insert = self.setUpQueryQuestion(self.test_database_name, -1)
        gui_w.save_new_question(*variables)
        query_second_insert = self.setUpQueryQuestion(self.test_database_name, -1)
        gui_w.delete_row(self.test_database_name, 2)
        query_after_delete = self.setUpQueryQuestion(self.test_database_name, -1)

        self.assertEqual(query_first_insert, query_after_delete)
        self.assertNotEqual(query_second_insert, query_after_delete)

        self.tearDownTable(self.test_database_name)

    def test_start_testing(self):
        """Provides values for the testing gui."""
        self.setUpDatabase(self.test_table_name)
        self.setUpPopulateQuestions(1, self.test_database_name)
        self.setUpPopulateQuestions(2, self.test_database_name)
        self.setUpPopulateQuestions(3, self.test_database_name)
        self.setUpPopulateQuestions(4, self.test_database_name)
        self.setUpPopulateQuestions(5, self.test_database_name)
        self.setUpResultsTables(self.test_table_name)
        gui_w = AppInterface()
        random_seq, random_row_id, question_obj = gui_w.start_testing(self.test_database_copy_name)
        sql_m = SqlManager()
        q_obj = sql_m.sql_get_row(self.test_database_copy_name, random_row_id)
        q_obj = q_obj[0]
        answer_list = [q_obj.answer1, q_obj.answer2, q_obj.answer3, q_obj.answer4, q_obj.answer5]
        answer1 = answer_list[random_seq[0]]
        answer2 = answer_list[random_seq[1]]
        answer3 = answer_list[random_seq[2]]
        answer4 = answer_list[random_seq[3]]
        answer5 = answer_list[random_seq[4]]

        q_should = [question_obj.row_id,
                    question_obj.question,
                    question_obj.answer1,
                    question_obj.answer2,
                    question_obj.answer3,
                    question_obj.answer4,
                    question_obj.answer5,
                    question_obj.firsts]
        q_queried = [q_obj.row_id, q_obj.question, answer1, answer2, answer3, answer4, answer5, q_obj.firsts]
        self.assertEqual(q_should, q_queried)

        self.tearDownTable(self.test_database_name)
        self.tearDownTable(self.test_results_name)
        self.tearDownTable(self.test_database_copy_name)

    def test_next_question(self):
        """Inserts the user selection from the testing GUI into the selected_results table."""
        self.setUpDatabase(self.test_table_name)
        self.setUpPopulateQuestions(1, self.test_database_name)
        self.setUpPopulateQuestions(2, self.test_database_name)
        self.setUpPopulateQuestions(3, self.test_database_name)
        self.setUpPopulateQuestions(4, self.test_database_name)
        self.setUpPopulateQuestions(5, self.test_database_name)
        self.setUpResultsTables(self.test_table_name)
        SettingVariables().set_class_variables(self.test_database_name, self.test_results_name, self.test_database_copy_name)

        gui_w = AppInterface()
        gui_w.next_question(1, "question", "[1, 0, 1, 0, 1]", "[1, 0, 1, 0, 1]", 1.0, 2)
        r_queried = self.setUpQueryResults(self.test_results_name, 0)
        # r_queried = [r_obj.row_id, r_obj.question, r_obj.right_answers, r_obj.user_answers, r_obj.firsts]
        r_should = [1, "question", "[1, 0, 1, 0, 1]", "[1, 0, 1, 0, 1]", 1, 0.0, 2]
        # test the Insert into the Results table
        self.assertEqual(r_should, r_queried)
        # test the firsts -1 in database_copy if score = 1
        sql_m = SqlManager()
        firsts_change = sql_m.sql_get_row(self.test_database_copy_name, 1)[0].firsts
        self.assertNotEqual(2, firsts_change)
        # if score = 0
        gui_w.next_question(1, "question", "[1, 0, 1, 0, 1]", "[1, 0, 1, 0, 0]", 1.0, 2)
        firsts_no_change = sql_m.sql_get_row(self.test_database_copy_name, 1)[0].firsts
        self.assertEqual(2, firsts_no_change)

        SettingVariables().set_class_variables()
        self.tearDownTable(self.test_database_name)
        self.tearDownTable(self.test_results_name)
        self.tearDownTable(self.test_database_copy_name)
