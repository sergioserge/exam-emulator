import tkinter
import time

"""
Following classes used as data containers for specific data structure.
"""


class TableNames:
    """Data container for table name information.

    Attributes:
        table_name(str): name of a table.
    """

    def __init__(self, table_name):
        self.table_name = table_name


class SettingVariables:
    """Default values to setup by the user.

    Attributes(class):
        selected_database(str): database name currently used for insertion of new questions and to make a copy.
        selected_results_table(str): results table name used for insertion of exam results.
        selected_database_copy(str): copy of database which is currently used for querying questions.
                                    The variable 'firsts' is subtracted by 1 if user answer was correct and 1 is added
                                    if it wasn't correct. If firsts = 0, the question is going to be deleted.
    """
    selected_database = "example_exam_database_db"
    selected_results_table = "example_exam_results"
    selected_database_copy = "example_exam_database_db_copy"

    @classmethod
    def set_class_variables(cls, selected_database="example_exam_database_db",
                            selected_results_table="example_exam_results",
                            selected_database_copy="example_exam_database_db_copy"):
        """[Optional]Changes all three SettingsVariables class variables to the passed arguments or to default values."""
        cls.selected_database = selected_database
        cls.selected_results_table = selected_results_table
        cls.selected_database_copy = selected_database_copy


class DatabaseTables:
    """Data container for database tables only - those tables which include the questions to copy from.

    Attributes:
        database_name(str): name of a database table.
    """

    def __init__(self, database_name=None):
        self.database_name = database_name

    @staticmethod
    def get_settings_variables(all_tables):
        """Returns a list of objects include only the database table names."""
        tables_list = [tables.table_name for tables in all_tables]

        database_list = []
        for tables in tables_list:
            for table in tables:
                if "_db" in table and "_db_copy" not in table:
                    database_list.append(DatabaseTables(table))

        return database_list


class ResultsTables:
    """Data container for results tables tables only - those tables which include the testing results.

    Attributes:
        results_name(str): name of a results table.
    """

    def __init__(self, results_name=None):
        self.results_name = results_name

    @staticmethod
    def get_settings_variables(all_tables):
        """Returns a list of objects include only the result table names."""
        tables_list = [tables.table_name for tables in all_tables]

        results_list = []
        for tables in tables_list:
            for table in tables:
                if "_db" not in table:
                    results_list.append(ResultsTables(table))

        return results_list


class DatabaseCopyTables:
    """Data container for database_copy tables only -
        those tables which include copied questions from the database tables.

    Attributes:
        database_copy_name(str): name of copy of a database table.
        """

    def __init__(self, database_copy_name=None):
        self.database_copy_name = database_copy_name

    @staticmethod
    def get_settings_variables(all_tables):
        """Returns a list of objects include only the database copy table names."""
        tables_list = [tables.table_name for tables in all_tables]

        database_copy_list = []
        for tables in tables_list:
            for table in tables:
                if "_db_copy" in table:
                    database_copy_list.append(DatabaseCopyTables(table))

        return database_copy_list


class Question:
    """Data container which includes all variables/ columns of the database/database copy tables.

    Attributes:
        row_id(int): Primary Key variable.
        question(str): an exam question.
        answer1(str): possible answer to the question.
        answer2(str): possible answer to the question.
        answer3(str): possible answer to the question.
        answer4(str): possible answer to the question.
        answer5(str): possible answer to the question.
        right_answers(list): list of 5 integer values. The sequence of the values corresponds to answer1 till answer5,
            so first value in the sequence stands for answer1, the second for answer2 etc.. 1 means right, 0 means wrong.
            firsts(int): integer value corresponds to how many tries are needed until question is going to be deleted,
            so wouldn't appear in exam testing any more.
    """

    def __init__(self, row_id, question, answer1, answer2, answer3, answer4, answer5, right_answers, firsts=2):
        self.row_id = row_id
        self.question = question
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer4 = answer4
        self.answer5 = answer5
        self.right_answers = right_answers
        self.firsts = firsts

    def to_dict(self):
        """Transform and return a list of question objects in a way that these can be passed to a pandas dataframe."""
        return {
            "Row_ID": self.row_id,
            "Question": self.question,
            "answer1": self.answer1,
            "answer2": self.answer2,
            "answer3": self.answer3,
            "answer4": self.answer4,
            "answer5": self.answer5,
            "Right Answers": self.right_answers,
            "Hitpoints": self.firsts
        }


class Results:
    """Data container which includes all variables/ columns of the results tables.

    Attributes:
        row_id(int): Primary Key variable.
        question(str): an exam question.
        right_answers(list): list of 5 integer values. The sequence of the values corresponds to answer1 till answer5,
            so first value in the sequence stands for answer1, the second for answer2 etc.. 1 means right, 0 means
            wrong.
        user_answers(list): same as right answers, but specified by the user. Represents users estimation if the
            possible answers are right or wrong.
        score(int): can be 1 - right_answers equals to user answers - or wrong - both variables aren't equal.
        time_track(float): represents the time user needed to answer the question and proceed to the next one.
        firsts(int): integer value corresponds to how many tries are needed until question is going to be deleted, so
            wouldn't appear in exam testing any more.
    """

    def __init__(self, row_id, question, right_answers, user_answers, score, time_track, firsts):
        self.row_id = row_id
        self.question = question
        self.right_answers = right_answers
        self.user_answers = user_answers
        self.score = score
        self.time_track = time_track
        self.firsts = firsts

    def to_dict(self):
        """Transform and return a list of results objects in a way that these can be passed to a pandas dataframe."""
        return {
            "Row_ID": self.row_id,
            "Question": self.question,
            "Right Answer Seq": self.right_answers,
            "User Answer Seq": self.user_answers,
            "Score": self.score,
            "Time Needed": self.time_track,
            "Hitpoints": self.firsts
        }


# Clock class from https://gist.github.com/ian-weisser/9993210
class Clock(tkinter.Label):
    """ Class that contains the clock widget and clock refresh """

    def __init__(self, parent=None, seconds=True, colon=False):
        """
        Create and place the clock widget into the parent element.
        It's an ordinary Label element with two additional features.
        """
        tkinter.Label.__init__(self, parent)

        self.display_seconds = seconds
        if self.display_seconds:
            self.time = time.strftime('%H:%M:%S')
        else:
            self.time = time.strftime('%I:%M %p').lstrip('0')
        self.display_time = self.time
        self.configure(text=self.display_time)

        if colon:
            self.blink_colon()

        self.after(200, self.tick)

    def tick(self):
        """ Updates the display clock every 200 milliseconds."""
        if self.display_seconds:
            new_time = time.strftime('%H:%M:%S')
        else:
            new_time = time.strftime('%I:%M %p').lstrip('0')
        if new_time != self.time:
            self.time = new_time
            self.display_time = self.time
            self.config(text=self.display_time)
        self.after(200, self.tick)

    def blink_colon(self):
        """ Blink the colon every second."""
        if ':' in self.display_time:
            self.display_time = self.display_time.replace(':', ' ')
        else:
            self.display_time = self.display_time.replace(' ', ':', 1)
        self.config(text=self.display_time)
        self.after(1000, self.blink_colon)
