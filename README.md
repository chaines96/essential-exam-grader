# Essential Exam Grader
A program which can mark CSVs of answers accross quizzes and saves a report of the final scores for each entrant. 

The structure and default names for the CSVs are as follows:
- entrants.csv: Contains the email address and name of each entrat.
- selections.csv: Each line must contain the entrant email, name, and the answer to each question. The final cell of the row will be the quiz number.
- OPTIONAL: QuizN_Report.csv - Like the above, but only the entries for quiz number N.
- answers.csv: The first column is the quiz number followed by the correct answers. This program uses string comparison and will only mark a selection correct if the answer matches exactly.
- prev.csv - The output of a previous run of hte program.

The output is a CSV with the names and emails from entrants.csv followed by the amount of correct answers to each quiz. The total is calculated in the final cell.

The amount of quizzes is currently set to a maximum of 26.

# TO-DOs
- Allow the user to pass parameters for file names.
- Allow a variable number of quizzes and quiz answers.
- Error checking.
