import unittest
from data_container import TableNames, DatabaseTables, ResultsTables, DatabaseCopyTables


class TestVariables:
    """Testvariables used for the unitests only."""

    def __init__(self):
        self.all_tables = [("test1",), ("test1_db",), ("test1_db_copy",), ("test2_db",), ("test2_db_copy",), ("test2",)]
        self.database_list = ["test1_db", "test2_db"]
        self.results_list = ["test1", "test2"]
        self.database_copy_list = ["test1_db_copy", "test2_db_copy"]


test_obj = TestVariables()


class TestAppInterface(unittest.TestCase):
    """Unittest class."""

    @staticmethod
    def setUpTableNames(all_tables):
        """Queries all saved tables and returns a list of TableNames objects."""
        all_tables_list = []
        for table_name in all_tables:
            all_tables_list.append(TableNames(table_name))

        return all_tables_list

    def test_get_settings_variables(self):
        """Tests the 3 functions which are separating all tables in
            database, results and database copy tables into 3 different lists."""
        all_tables_list = self.setUpTableNames(test_obj.all_tables)

        database_list = DatabaseTables().get_settings_variables(all_tables_list)
        database_list = [database.database_name for database in database_list]
        self.assertEqual(test_obj.database_list, database_list)

        results_list = ResultsTables().get_settings_variables(all_tables_list)
        results_list = [results.results_name for results in results_list]
        self.assertEqual(test_obj.results_list, results_list)

        database_copy_list = DatabaseCopyTables().get_settings_variables(all_tables_list)
        database_copy_list = [database_copy.database_copy_name for database_copy in database_copy_list]
        self.assertEqual(test_obj.database_copy_list, database_copy_list)
