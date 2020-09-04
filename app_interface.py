from tkinter import *
import sqlite3
from pandastable import Table
import pandas as pd
from data_container import SettingVariables, DatabaseTables, ResultsTables, DatabaseCopyTables, Results, \
    Clock
from data_container import Question
from sql_manager import SqlManager
import random
import time


# ===== GUI Menus =====
class AppInterface:
    """This class includes both UI elements and Interface elements(general functionality)

    Attributes:
        master(Tkinter): Tkinter object. Needed to start and end the interface.
        insert_top(Toplevel)[optional]: Toplevel object, to open a new window.
        testing_top(Toplevel)[optional]: Toplevel object, to open a new window.
    """
    # todo separate UI and Interface

    def __init__(self, *args):
        self.master = args
        self.insert_top = None
        self.testing_top = None

    def gui_main_menu(self, master):
        """Widgets of the main GUI Menu."""
        entry_field = Entry(master, width=29, borderwidth=6)
        entry_field.grid(row=11, column=0, columnspan=2, sticky=W, padx=(5, 0))

        settings_button = Button(master, text="Select Working Tables", command=self.set_up_settings, width=25)
        testing_button = Button(master, text="Start Testing", command=lambda: self.start_testing(), width=25)
        exit_button = Button(master, text="Exit Application", command=self.exit_app, width=15)

        create_exam_db_button = Button(master,
                                       text="Create New Questions Database",
                                       command=lambda: self.create_exam_database(entry_field.get(),
                                                                                 entry_field.delete(0, END)),
                                       width=25)
        create_results_table_button = Button(master,
                                             text="Create Testing Session",
                                             command=lambda: self.create_results_tables(entry_field.get(),
                                                                                        entry_field.delete(0, END)),
                                             width=25)
        insert_questions_button = Button(master,
                                         text="Insert New Questions Manually",
                                         command=self.insert_new_questions,
                                         width=25)
        insert_from_file_button = Button(master,
                                         text="Insert New Questions From File",
                                         command=self.questions_from_file,
                                         width=25)

        delete_table_button = Button(master,
                                     text="Delete Table",
                                     command=lambda: self.delete_table(entry_field.get(),
                                                                       entry_field.delete(0, END)),
                                     width=25)
        delete_row_button = Button(master, text="Delete Question", command=self.gui_delete_row, width=25)

        show_all_tables_button = Button(master, text="Show All Tables", command=self.show_all_tables, width=25)
        testing_results_button = Button(master,
                                        text="Show Testing Results",
                                        command=self.show_testing_results,
                                        width=25)
        remaining_questions_button = Button(master,
                                            text="Show Current Questions",
                                            command=self.show_remaining_questions,
                                            width=25)
        database_content_button = Button(master, text="Show Database", command=self.show_database_content, width=25)

        settings_button.grid(row=1, column=0, sticky=W, padx=(5, 0), pady=(5, 0))
        testing_button.grid(row=1, column=1, sticky=W, padx=(5, 0), pady=(5, 0))
        exit_button.grid(row=1, column=3, sticky=E, padx=(5, 0))

        create_exam_db_button.grid(row=3, column=0, sticky=W, padx=(5, 0))
        create_results_table_button.grid(row=3, column=1, sticky=W, padx=(5, 0))
        insert_questions_button.grid(row=4, column=0, sticky=W, padx=(5, 0))
        insert_from_file_button.grid(row=4, column=1, sticky=W, padx=(5, 0))

        delete_table_button.grid(row=6, column=0, sticky=W, padx=(5, 0))
        delete_row_button.grid(row=6, column=1, sticky=W, padx=(5, 0))

        show_all_tables_button.grid(row=8, column=0, sticky=W, padx=(5, 0))
        testing_results_button.grid(row=8, column=1, sticky=W, padx=(5, 0))
        remaining_questions_button.grid(row=9, column=0, sticky=W, padx=(5, 0))
        database_content_button.grid(row=9, column=1, sticky=W, padx=(5, 0))

    def gui_setting_menu(self, database_list, results_list, database_copy_list):
        """
            The Menu to set up the default tables by the user:

            database: questions and possible answers are saved here only.
            results: exam results(right or wrong) as well as the time which user spent on the answer.
            database copy: an exact copy of the database table is created automatically on the creation of results table.
                A question is going to be deleted if user answered it a certain amount of time(default 2, but increase by one
                on every wrong answer of that same question).
            """
        set_up_top = Toplevel()
        set_up_top.attributes("-topmost", True)
        set_up_top.title("Interactive Table Overview")

        column1_title = "Database-Tables"
        column2_title = "Results-Tables"
        column3_title = "Copied Database-Tables"
        database_list = database_list
        results_list = results_list
        database_copy_list = database_copy_list

        # todo labels, which shows the current selected default tables
        database_label = Label(set_up_top, text=column1_title)
        results_label = Label(set_up_top, text=column2_title)
        database_copy_label = Label(set_up_top, text=column3_title)

        database_label.grid(row=1, column=0)
        results_label.grid(row=1, column=1)
        database_copy_label.grid(row=1, column=2)
        row_results = 2
        row_database_copy = 2
        row_database = 2

        database_var = StringVar()
        results_var = StringVar()
        database_copy_var = StringVar()

        for database in database_list:
            Radiobutton(set_up_top,
                        text=database,
                        variable=database_var,
                        value=database,
                        command=lambda: self.save_selected_database(database_var.get()),
                        anchor=W,
                        width=25).grid(row=row_database, column=0)
            row_database += 1

        for results in results_list:
            Radiobutton(set_up_top,
                        text=results,
                        variable=results_var,
                        value=results,
                        command=lambda: self.save_selected_results_table(results_var.get()),
                        anchor=W,
                        width=25).grid(row=row_results, column=1)
            row_results += 1

        for database_copy in database_copy_list:
            Radiobutton(set_up_top,
                        text=database_copy,
                        variable=database_copy_var,
                        value=database_copy,
                        command=lambda: self.save_selected_database_copy(database_copy_var.get()),
                        anchor=W,
                        width=25).grid(row=row_database_copy, column=2)
            row_database_copy += 1

        save_set_up_button = Button(set_up_top, text="Close Settings Menu", command=set_up_top.destroy)
        save_set_up_button.grid(row=1, column=3)

    def gui_insert_menu(self):
        """Gui for manual input of new questions."""
        self.insert_top = Toplevel()
        self.insert_top.geometry("1366x768")
        insert_database_label = Label(self.insert_top, text="The questions are going to be inserted into: {}".format(SettingVariables.selected_database))
        insert_database_label.grid(row=0, column=1, padx=(0, 25), pady=10, sticky=W)

        question_text = StringVar()
        answer_text1 = StringVar()
        answer_text2 = StringVar()
        answer_text3 = StringVar()
        answer_text4 = StringVar()
        answer_text5 = StringVar()
        state_var1 = IntVar()
        state_var2 = IntVar()
        state_var3 = IntVar()
        state_var4 = IntVar()
        state_var5 = IntVar()

        question_text = Text(self.insert_top, height=4, width=90)
        answer_text1 = Text(self.insert_top, height=4, width=90)
        answer_text2 = Text(self.insert_top, height=4, width=90)
        answer_text3 = Text(self.insert_top, height=4, width=90)
        answer_text4 = Text(self.insert_top, height=4, width=90)
        answer_text5 = Text(self.insert_top, height=4, width=90)
        question_text.grid(row=1, column=1, columnspan=3)
        answer_text1.grid(row=2, column=1, columnspan=3)
        answer_text2.grid(row=3, column=1, columnspan=3)
        answer_text3.grid(row=4, column=1, columnspan=3)
        answer_text4.grid(row=5, column=1, columnspan=3)
        answer_text5.grid(row=6, column=1, columnspan=3)

        answer_state1 = Checkbutton(self.insert_top, variable=state_var1)
        answer_state2 = Checkbutton(self.insert_top, variable=state_var2)
        answer_state3 = Checkbutton(self.insert_top, variable=state_var3)
        answer_state4 = Checkbutton(self.insert_top, variable=state_var4)
        answer_state5 = Checkbutton(self.insert_top, variable=state_var5)
        answer_state1.grid(row=2, column=0)
        answer_state2.grid(row=3, column=0)
        answer_state3.grid(row=4, column=0)
        answer_state4.grid(row=5, column=0)
        answer_state5.grid(row=6, column=0)

        save_button = Button(self.insert_top,
                             text="Save",
                             command=lambda: self.save_new_question(question_text.get(1.0, END),
                                                                    answer_text1.get(1.0, END),
                                                                    answer_text2.get(1.0, END),
                                                                    answer_text3.get(1.0, END),
                                                                    answer_text4.get(1.0, END),
                                                                    answer_text5.get(1.0, END),
                                                                    state_var1.get(),
                                                                    state_var2.get(),
                                                                    state_var3.get(),
                                                                    state_var4.get(),
                                                                    state_var5.get()))
        save_button.grid(row=0, column=4, sticky=W, padx=(5, 0))

    def gui_delete_row(self):
        """GUI window for the deletion of a certain row. User has to type in table name + row_id."""
        delete_top = Toplevel()
        delete_top.geometry("500x300")
        delete_top.title("Delete Row Menu")

        delete_menu_label = Label(delete_top, text="Please type in the table and the row id you want to delete")
        delete_menu_label.grid(row=1, column=0, columnspan=2)

        table_input_label = Label(delete_top, text="Table Name")
        row_input_label = Label(delete_top, text="Row Id")
        table_input_label.grid(row=2, column=0)
        row_input_label.grid(row=2, column=1)

        table_name_entry = Entry(delete_top, width=29, borderwidth=6)
        row_id_entry = Entry(delete_top, width=29, borderwidth=6)
        table_name_entry.grid(row=3, column=0)
        row_id_entry.grid(row=3, column=1)

        delete_button = Button(delete_top,
                               text="Delete Selected Row",
                               command=lambda:
                               self.delete_row(table_name_entry.get(),
                                               row_id_entry.get(),
                                               table_name_entry.delete(0, END),
                                               row_id_entry.delete(0, END)))
        delete_button.grid(row=3, column=3)

    def gui_testing_menu(self, question_obj):
        """GUI for the exam itself - multiple choice questions."""
        self.testing_top = Toplevel()
        self.testing_top.geometry("1366x768")

        info_frame = Frame(self.testing_top, width=768, height=100)
        info_frame.grid(row=1, column=0, sticky=W)
        testing_frame = Frame(self.testing_top, width=768, height=1260)
        testing_frame.grid(row=2, column=0, sticky=W)

        self.results_overview(info_frame)
        info_label = Label(info_frame, text="Brief Results Overview")
        info_label.grid(row=1, column=0)
        correct_answer_label = Label(testing_frame, text="Check the correct answer", anchor=W)
        correct_answer_label.grid(row=1, column=0)

        row_id = question_obj.row_id
        right_answers = question_obj.right_answers
        start_time = time.time()
        firsts = question_obj.firsts

        question = question_obj.question
        answer_list = [question_obj.answer1, question_obj.answer2, question_obj.answer3, question_obj.answer4, question_obj.answer5]
        choice1 = IntVar()
        choice2 = IntVar()
        choice3 = IntVar()
        choice4 = IntVar()
        choice5 = IntVar()
        user_choice_list = [choice1, choice2, choice3, choice4, choice5]
        row_answer = 5
        row_user_choice = 5

        question_label = Label(testing_frame, text=question, anchor=W, justify=LEFT)
        question_label.grid(row=2, column=1)

        for answer in answer_list:
            Label(testing_frame, text=answer).grid(row=row_answer, column=1, sticky=W)
            row_answer += 1

        for choice in user_choice_list:
            Checkbutton(testing_frame, variable=choice).grid(row=row_user_choice, column=0)
            row_user_choice += 1

        next_question_button = Button(testing_frame,
                                      text="Next Question",
                                      command=lambda: self.next_question(row_id,
                                                                         question,
                                                                         right_answers,
                                                                         [choice1.get(), choice2.get(), choice3.get(), choice4.get(), choice5.get()],
                                                                         start_time,
                                                                         firsts))
        next_question_button.grid(row=10, column=0, sticky=W)

    @staticmethod
    def gui_show_all_tables(tables_list):
        """GUI shows all tables saved in sqlite3 database."""
        display_all_tables_top = Toplevel()
        display_all_tables_top.title("Interactive Table Overview")

        tables_list = pd.DataFrame(tables_list)
        tables_list.rename(columns={0: "Tablename"}, inplace=True)

        my_frame = Frame(display_all_tables_top)
        my_frame.grid(row=5, column=0, columnspan=10)

        display_table = Table(parent=my_frame, dataframe=tables_list, showtoolbar=True)
        display_table.show()

    @staticmethod
    def gui_show_testing_results(results_obj):
        """GUI shows the exam results, so contents of the set up results table (=selected_results_table)."""
        display_top = Toplevel()
        display_top.title("Results Statistics")

        tables_list = pd.DataFrame(r.to_dict() for r in results_obj)
        tables_list.rename(columns={0: "Row ID",
                                    1: "Question",
                                    2: "Correct Answers",
                                    3: "User Answers",
                                    4: "Your Score",
                                    5: "Timetrack",
                                    6: "Frequency"},
                           inplace=True)

        my_frame = Frame(display_top)
        my_frame.grid(row=5, column=0, columnspan=10)

        display_table = Table(parent=my_frame, dataframe=tables_list, showtoolbar=True)
        display_table.show()

    @staticmethod
    def gui_show_remaining_questions(database_obj):
        """GUI shows the remaining questions in selected_database_copy."""
        display_top = Toplevel()
        display_top.title("Remaining Questions in Database Copy")

        tables_list = pd.DataFrame(r.to_dict() for r in database_obj)
        tables_list.rename(columns={0: "ID",
                                    1: "Question",
                                    2: "Answer1",
                                    3: "Answer2",
                                    4: "Answer3",
                                    5: "Answer4",
                                    6: "Answer5",
                                    7: "1 if Correct",
                                    8: "1 if Correct",
                                    9: "1 if Correct",
                                    10: "1 if Correct",
                                    11: "1 if Correct"},
                           inplace=True)

        my_frame = Frame(display_top)
        my_frame.grid(row=5, column=0, columnspan=10)

        display_table = Table(parent=my_frame, dataframe=tables_list, showtoolbar=True)
        display_table.show()

    @staticmethod
    def gui_show_database_content(database_obj):
        """GUI shows the remaining questions in selected_database."""
        display_top = Toplevel()
        display_top.title("All questions in Database")

        tables_list = pd.DataFrame(r.to_dict() for r in database_obj)
        tables_list.rename(columns={0: "ID",
                                    1: "Question",
                                    2: "Answer1",
                                    3: "Answer2",
                                    4: "Answer3",
                                    5: "Answer4",
                                    6: "Answer5",
                                    7: "1 if Correct",
                                    8: "1 if Correct",
                                    9: "1 if Correct",
                                    10: "1 if Correct",
                                    11: "1 if Correct"},
                           inplace=True)

        my_frame = Frame(display_top)
        my_frame.grid(row=5, column=0, columnspan=10)

        display_table = Table(parent=my_frame, dataframe=tables_list, showtoolbar=True)
        display_table.show()

    @staticmethod
    def gui_results_overview(top, average_score, last_score):
        """GUI shows the answered questions and exam information (like right or wrong) saved in selected_database_copy.
        """
        Label(top, text="The Average Score").grid(row=2, column=0, sticky=W)
        Label(top, text=average_score).grid(row=3, column=0, sticky=W)
        Label(top, text="The Last Score").grid(row=2, column=1, sticky=W)
        Label(top, text=last_score).grid(row=3, column=1, sticky=W)
        Label(top, text="Clock").grid(row=2, column=2, sticky=W)

        clock1 = Clock(top)
        clock1.grid(row=3, column=5, sticky=W)
        clock1.configure(font=("helvetica", 16))

    def gui_questions_from_file(self):
        """Instead of inserting new questions manually you can insert multiple question from file at once.
            Please make sure to take the specifications of that file into account.
        """
        import_file_top = Toplevel()
        import_file_top.geometry("600x600")
        import_file_top.title("Please READ the explanation before you click on the button on the right ")

        import_button = Button(import_file_top,
                               text="Import Questions",
                               command=lambda: self.insert_new_questions_from_file(import_file_top.destroy()),
                               width=25)

        import_info_label = Label(import_file_top, justify=LEFT,
                                  text="Please make sure that the external file "
                                       "is compliant with the following conditions: "
                                       "\n- it is a Textfile which is called 'import_questions' (.txt)"
                                       "\n - that file is in same folder as the 'Exam_Emulator' "
                                       "executable(.exe)"
                                       "\n- every new question starts with the word 'Exercise' "
                                       "followed by a blank space"
                                       "\n - it is followed by the question text in the next line"
                                       "\n - next '*' for the right and '_' for the wrong answers(exactly 5 symbols)"
                                       "\n - followed by the answer options(exactly 5, "
                                       "use some kind of symbol as placeholder if less than 5)"
                                       "\n - every element is separated by a blank line"
                                       "\n - just in case, example file is attached"
                                       "\n")
        import_example_label = Label(import_file_top, justify=LEFT,
                                     text="EXAMPLE:"
                                          "\n"
                                          "\nExercise Script page 202-204"
                                          "\nWhat is the name of our planet?"
                                          "\n"
                                          "\n*____"
                                          "\n"
                                          "\nEarth"
                                          "\n"
                                          "\nMars"
                                          "\n"
                                          "\nVenus"
                                          "\n"
                                          "\nPluto"
                                          "\n"
                                          "\nUrAnus"
                                          "\n"
                                          "\nExercise...")

        import_info_label.grid(row=1, column=0, sticky=W, padx=(5, 0))
        import_example_label.grid(row=2, column=0, sticky=W, padx=(5, 0))
        import_button.grid(row=3, column=0, sticky=W, padx=(5, 0))

    @staticmethod
    def create_exam_database(table_name, *args):
        """Creates a database table with the passed table name.
            *args: only needed to delete the gui entry_field after passing of data
        """
        sql_m = SqlManager()
        sql_m.sql_create_exam_database(table_name)

    @staticmethod
    def create_results_tables(table_name, *args):
        """Creates a results table with the passed table name. *args is used only in the button widget to delete input
            inside the entry widget.
            *args: only needed to delete the gui entry_field after passing of data
        """
        try:
            # creates 2 tables: 1. for saving results and 2. a copy of the selected database
            settings_obj = SettingVariables()
            selected_database = settings_obj.selected_database
            sql_m = SqlManager()
            sql_m.sql_create_results_table(table_name)
            sql_m.sql_create_database_copy(selected_database)
        except sqlite3.OperationalError as oe:
            print("Exception occurred in create_results_tables: " + str(oe))

    def show_all_tables(self):
        """Function passes the order to SqlManager to query all table names in database."""
        sql_m = SqlManager()
        all_tables = sql_m.sql_get_all_tables()
        tables_list = [tables.table_name for tables in all_tables]
        self.gui_show_all_tables(tables_list)

        return tables_list

    def set_up_settings(self):
        """Function selects each one of the three table types: database, results, database_copy."""
        sql_m = SqlManager()
        all_tables = sql_m.sql_get_all_tables()
        database_list = DatabaseTables().get_settings_variables(all_tables)
        results_list = ResultsTables().get_settings_variables(all_tables)
        database_copy_list = DatabaseCopyTables().get_settings_variables(all_tables)

        database_list = [database.database_name for database in database_list]
        results_list = [results.results_name for results in results_list]
        database_copy_list = [database_copy.database_copy_name for database_copy in database_copy_list]

        self.gui_setting_menu(database_list, results_list, database_copy_list)

        return database_list, results_list, database_copy_list

    @staticmethod
    def save_selected_database(selected_database):
        """Changes SettingVariables class variable selected_database to the passed table name."""
        SettingVariables.selected_database = selected_database

    @staticmethod
    def save_selected_results_table(selected_results_table):
        """Changes SettingVariables class variable results_table to the passed table name."""
        SettingVariables.selected_results_table = selected_results_table

    @staticmethod
    def save_selected_database_copy(selected_database_copy):
        """Changes SettingVariables class variable selected_database_copy to the passed table name."""
        SettingVariables.selected_database_copy = selected_database_copy

    @staticmethod
    def delete_table(table_name, *args):
        """Deletes a whole table with the passed table name. *args is used only in the button widget to delete input
            inside the entry widget.
            *args: only needed to delete the gui entry_field after passing of data
        """
        sql_m = SqlManager()
        sql_m.sql_delete_table(table_name)

    def save_new_question(self, *args):
        """Passes the user information input (Question object) from GUI to SqlManager to save data
            in selected_database table.
        """
        question, answer1, answer2, answer3, answer4, answer5, state_var1, state_var2, state_var3, state_var4, state_var5 = args
        right_answers_list = [state_var1, state_var2, state_var3, state_var4, state_var5]
        settings_obj = SettingVariables()
        selected_database = settings_obj.selected_database
        row_id = SqlManager().sql_get_last_row_id(selected_database) + 1
        new_question = Question(row_id,
                                question.replace("\n", "."),
                                answer1.replace("\n", "."),
                                answer2.replace("\n", "."),
                                answer3.replace("\n", "."),
                                answer4.replace("\n", "."),
                                answer5.replace("\n", "."),
                                right_answers_list,
                                2)
        new_question_list = [new_question]
        sql_m = SqlManager()
        sql_m.sql_insert_new_questions(new_question_list, selected_database)

        try:
            self.insert_top.destroy()
        except AttributeError as ae:
            print("Exception occurred in save_new_question - due to " + str(ae))
        finally:
            self.gui_insert_menu()

    def insert_new_questions(self):
        self.gui_insert_menu()

    @staticmethod
    def delete_row(table_name, row_id, *args):
        """Deletes the passed row in the passed table. *args is used only in the button widget to delete input
            inside the entry widget.
            *args: only needed to delete the gui entry_field after passing of data
        """
        sql_m = SqlManager()
        sql_m.sql_delete_row(table_name, row_id)

    def start_testing(self, table_name=SettingVariables().selected_database_copy):
        """Queries content of the selected_database_copy table and selects randomly some row.
        Creates a random sequence
            of 5 digits in range 0 and 4 to sort newly the possible answers as well as right_answers sequence.
            Then pass all variables to the testing gui.
        """
        sql_m = SqlManager()
        all_questions = sql_m.sql_get_database_content(table_name)
        random_row_id = random.randint(1, len(all_questions))
        random_answer_seq = random.sample([0, 1, 2, 3, 4], 5)

        question_vars = all_questions[random_row_id-1]
        random_question = [question_vars.row_id,
                           question_vars.question,
                           question_vars.answer1,
                           question_vars.answer2,
                           question_vars.answer3,
                           question_vars.answer4,
                           question_vars.answer5,
                           question_vars.right_answers,
                           question_vars.firsts]

        row_id = random_question[0]
        question_var = random_question[1]
        answer_vars = random_question[2:7]
        answer_vars = [answer_vars[i] for i in random_answer_seq]
        # transform right_answer variable from str to list with 5 integers
        right_answers = random_question[7]
        right_answers = [int(right_answers[i]) for i in range(1, len(right_answers), 3)]
        # save the right_answer variable in same order as the random_answer_seq
        right_answers_new = [right_answers[i] for i in random_answer_seq]
        firsts = random_question[8]
        question_obj = Question(row_id, question_var, answer_vars[0], answer_vars[1], answer_vars[2], answer_vars[3], answer_vars[4], right_answers_new, firsts)

        self.gui_testing_menu(question_obj)

        return random_answer_seq, random_row_id, question_obj

    def next_question(self, row_id, question, right_answers, user_answers, start_time, firsts):
        """Sets the score variable to 1 if right_answers and user_answers are equally.
            Creates the time_track_variable to save how long user took to answer a question.
            Adds or subtracts firsts variable accordingly to the score(add if score=0 add subtract if score=1).
            Checks if any firsts variable is lower than one and deletes that row if true.
            Passes all variables to the selected_results table.
            Then call the start_testing function again.
        """
        try:
            if right_answers == user_answers:
                score = 1
            else:
                score = 0
            end_time = time.time()
            time_track = round(((end_time - start_time) / 60), 2)
            results = Results(row_id, question, right_answers, user_answers, score, time_track, firsts)
            results_list = [results]

            sql_m = SqlManager()
            sql_m.sql_insert_new_results(results_list, SettingVariables().selected_results_table)
            if score == 1:
                sql_m.sql_subtract_firsts(row_id, SettingVariables().selected_database_copy)
            elif score == 0:
                sql_m.sql_add_firsts(row_id, SettingVariables().selected_database_copy)

            if score == 1:
                firsts = sql_m.sql_get_row(SettingVariables().selected_database_copy, row_id)[0].firsts

            if firsts < 1:
                sql_m.sql_delete_row(SettingVariables().selected_database_copy, row_id)
        except IndexError as ie:
            print(str(ie) + " in next_question")
            print("Possible reason might be that the database itself is empty or you choose an empty database_copy")

        try:
            self.testing_top.destroy()
            self.start_testing(SettingVariables().selected_database_copy)
        except Exception:
            print("Another exception in next_question occurred")

    def questions_from_file(self):
        """Calls the gui_questions_from_file function."""
        self.gui_questions_from_file()

    @staticmethod
    def insert_new_questions_from_file(*args):
        """Imports data from txt file into the selected_database table.
            *args: only needed to delete the gui entry_field after passing of data
        """
        with open("import_questions.txt", encoding="utf8") as f:
            r = f.read()

        test_questions = r.split("Exercise")
        test_questions = test_questions[1:]
        questions_list = []
        for i in range(0, len(test_questions)):
            questions_list.append(test_questions[i].split("\n\n"))

        for ii in range(0, len(questions_list)):
            states = []
            answer_states = questions_list[ii][1]
            for i in range(0, len(answer_states)):
                answer_state = answer_states[i]
                if answer_state == "*":
                    state = 1
                    states.append(state)
                elif answer_state == "-":
                    state = 0
                    states.append(state)

            question = questions_list[ii][0].replace("\n", ".")
            answer1 = questions_list[ii][2].replace("\n", "."),
            answer2 = questions_list[ii][3].replace("\n", "."),
            answer3 = questions_list[ii][4].replace("\n", "."),
            answer4 = questions_list[ii][5].replace("\n", "."),
            answer5 = questions_list[ii][6].replace("\n", "."),
            right_answers = [states[0], states[1], states[2], states[3], states[4]]

            sql_m = SqlManager()
            table_content = sql_m.sql_get_database_content(SettingVariables().selected_database)
            if len(table_content) > 0:
                row_id = table_content[-1].row_id + 1
            else:
                row_id = 1

            variables = Question(row_id, question, answer1, answer2, answer3, answer4, answer5, right_answers)
            variables = [variables]

            sql_m = SqlManager()
            sql_m.sql_insert_new_questions(variables, SettingVariables().selected_database)

    def show_database_content(self):
        """Opens a window which shows contents of selected_database table."""
        sql_m = SqlManager()
        database_copy = sql_m.sql_get_database_content(SettingVariables().selected_database)
        self.gui_show_database_content(database_copy)

    def show_testing_results(self):
        """Opens a window which shows contents of selected_results table."""
        sql_m = SqlManager()
        results_list = sql_m.sql_get_results_content(SettingVariables().selected_results_table)
        self.gui_show_testing_results(results_list)

    def show_remaining_questions(self):
        """Opens a window which shows contents of selected_database_copy table."""
        sql_m = SqlManager()
        database_copy = sql_m.sql_get_database_content(SettingVariables().selected_database_copy)
        self.gui_show_remaining_questions(database_copy)

    def results_overview(self, top):
        """Calculates the average score and passes it as well as the last score to the gui_results_overview."""
        try:
            sql_m = SqlManager()
            results_list = sql_m.sql_get_results_content(SettingVariables().selected_results_table)
            last_score = results_list[-1].score
            score_list = [score.score for score in results_list]
            score_average = 0
            for score in score_list:
                score_average += score
            score_average = str(round(score_average / len(score_list) * 100, 2)) + " %"
            self.gui_results_overview(top, score_average, last_score)
        except IndexError as ie:
            print(str(ie) + " in results_overview")
            print("This is OK, if our results table is empty. Otherwise you should inform your admin.")

    def exit_app(self):
        # master is a tuple
        for root in self.master:
            root.quit()

    # ===== Function for Development and Testing =====
    # def populate_test_database(self):
    #     settings_obj = SettingVariables()
    #     selected_database = settings_obj.selected_database
    #     new_q1 = Question(9, "Question1", "Answer1", "Answer2", "Answer3", "Answer4", "Answer5", '[1, 0, 1, 0, 1]')
    #     new_q2 = Question(10, "Question2", "Answer1", "Answer2", "Answer3", "Answer4", "Answer5", '[0, 0, 0, 1, 1]')
    #     new_q3 = Question(11, "Question3", "Answer1", "Answer2", "Answer3", "Answer4", "Answer5", '[1, 0, 1, 0, 1]')
    #     new_q4 = Question(12, "Question4", "Answer1", "Answer2", "Answer3", "Answer4", "Answer5", '[1, 1, 1, 0, 0]')
    #     new_q5 = Question(13, "Question5", "Answer1", "Answer2", "Answer3", "Answer4", "Answer5", '[1, 1, 1, 1, 1]')
    #     new_q6 = Question(14, "Question6", "Answer1", "Answer2", "Answer3", "Answer4", "Answer5", '[0, 0, 0, 0, 0]')
    #     new_q7 = Question(15, "Question7", "Answer1", "Answer2", "Answer3", "Answer4", "Answer5", '[1, 0, 1, 0, 1]')
    #     sql_m = SqlManager()
        # sql_m.sql_insert_new_questions([new_q1], selected_database)
        # sql_m.sql_insert_new_questions([new_q2], selected_database)
        # sql_m.sql_insert_new_questions([new_q3], selected_database)
        # sql_m.sql_insert_new_questions([new_q4], selected_database)
        # sql_m.sql_insert_new_questions([new_q5], selected_database)
        # sql_m.sql_insert_new_questions([new_q6], selected_database)
        # sql_m.sql_insert_new_questions([new_q7], selected_database)
