# Welcome young padawan :)

# Exam Emulator
An emulator to practice multiple choice exams

This is my first python project using classes, multiple files and unit-testing. So any feedback and support is highly appreciated.
Please, don't hesitate to contact me about what ever issue, since all input is helping me to improve my programmer skills.




## Motivation
Some time ago I was preparing for the Oracle SQL Certification exam, so I needed to practice the exam conditions upfront. The idea was to build an application to simulate the same conditions. 
After passing the exam I was eager to improve my python skills and help other fellows who want to pass an exam with similar conditions. 
So I improved the app step by step.
I believe that my application can be used to prepare for any kind exam. It should be also useful if you have to memorize a lot in short time.




## Kinda Users Manual
* Every time you start the application an addition window will pop out. Here you can set up the tables to query multiple choice questions from and save your testing results. If you haven't set up these tables yet, please just close it.
![Settings_Menu](https://github.com/sergioserge/exam-emulator/blob/master/Emulator_Settings_Menu.png)
* Type in the database name in the input field on the bottom and click on "Create New Questions Database"
![Main Menu](https://github.com/sergioserge/exam-emulator/blob/master/Emulator_Main_Menu.png)
* Click on "Insert New Questions Manually" or "Insert New Questions From File" to insert new questions into the database
* Click on "Select Working Tables" and select the database_name(with ending"_db"), which will be used to be copied automatically in the next step(that copy is going to have the ending "_copy").
* Now you can create a new table to save the testing results into. So type in the name into the same input field and click on "Create Testing Session"
* Now you have created 3 tables in sum and can click on "Select Working Tables".
* Now you can click on "Start Testing" to start the exam.

* BTW: the automatically created table is the one is going to be used for the actual exam. So if you answer a question two times in a row, the question is going to be deleted. Every time you answered a certain question wrong, you have to answer it one more time correctly to be deleted.




## App Logic
* every request from app_interface is passed as a specific data_container class to the sql_manager and if necessary passed as another data_container back to app_interface




## To-Do
* testin-modus feature: to set up the testing time or other conditions to fit other kind of tests(like linkedin)
* provide the application as an executable file
* reduce complexity of Questions class
* unify the data container classes
* add more unit-testing
* add info messages to help a user, if something went wrong
* in general: improve cleanness and readability of the code


## Bugs
* issues with functioning on Linux 5.4.0-45-generic; 49-Ubuntu 20.04.1 LTS
