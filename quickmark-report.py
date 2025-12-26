import csv

#File variables
entrants_file = open("entrants.csv")
entrants  = csv.reader(entrants_file, delimiter=',')
try:
    student_answers_file = open("student_answers.csv")
    student_answers  = csv.reader(student_answers_file, delimiter=',')
except Exception as e:
    print(e)
answer_key_file = open("answer_key.csv")
answer_key  = csv.reader(answer_key_file, delimiter=',')

#If the picks were not a single CSV file, we will make a list out of new ones.
picks_list = list()
picks_list_num = []
quiz_index = 1
while(quiz_index < 30):
    try:
        picks_quizfile = open("Quiz_" + str(quiz_index) + "_Report.csv")
        picks_list.append(csv.reader(picks_quizfile, delimiter=','))
        picks_list_num.append(quiz_index)
    except Exception as e:
        pass
    quiz_index = quiz_index + 1

scoreboard = dict() #This is a dictionary whose keys are tuples (email,name) and whose values are lists

#Populate the "score board"
for entrant in entrants:
    blank_list = [0]*26
    scoreboard.update({(entrant[0],entrant[1]) : blank_list})

#Variables
QUIZ = 0
comparison = list()
amount_of_quizzes = 25 #How many games played this quiz

#Evaluate each pick, of every quiz.
for pick in picks:
    if pick[-1] != QUIZ: #only runs if quiz is different
        QUIZ = pick[-1]
        try:
            int(QUIZ) #If the last column is a number, by convention, we consider that the quiz number and we use it instead of the quiz index.
        except Exception as e:
            print(e)
            continue
        for answer in answer_key:
            #This finds the quiz of the given pick
            if answer[0] == QUIZ:
                comparison = answer[:]
                amount_of_quizzes = len(comparison) - 4
    #The comparison array now contains the correct values.
    quiz_score = 0
    if scoreboard[(pick[0],pick[1])][int(QUIZ)-1] == 0: #Newer entries come first in the list, so a duplicate entry is skipped.
        for i in range(2,amount_of_quizzes):
            if pick[i] == comparison[i-1]:
                quiz_score = quiz_score + 1
        try:
            scoreboard[(pick[0],pick[1])][int(QUIZ)-1] = quiz_score
        except:
            with open('non_registered.txt', 'a') as a: #The entrant is not in the registrants. Score not updated.
                a.write(str((pick[0],pick[1])) + " in Week " + str(QUIZ))

#This loop is for quiz CSVs which are not contained in a picks.csv or registrants.csv file.
for quiz in student_answers_file:
    ind = 0
    QUIZ = picks_list_num[ind]
    for answer in answer_key:
        #This finds the quiz of the given pick
        if answer[0] == QUIZ:
            comparison = answer[:]
            amount_of_quizzes = len(comparison) - 4
    for pick in quiz:
        quiz_score = 0
        if scoreboard[(pick[0],pick[1])][int(QUIZ)-1] == 0: #Newer entries come first in the list, so a duplicate entry is skipped.
            for i in range(2,amount_of_quizzes):
                if pick[i] == comparison[i-1]:
                    quiz_score = quiz_score + 1
            try:
                scoreboard[(pick[0],pick[1])][int(QUIZ)-1] = quiz_score
            except:
                with open('non_registered.txt', 'a') as a: #The entrant is not in the registrants. Score not updated.
                    a.write(str((pick[0],pick[1])) + " in Week " + str(QUIZ))
    ind = i + 1 #Looks at the next entry in picks_list_num.

#Given the quizly scores, we now compute all scores.
for score in scoreboard:
    total = 0
    for i in range(0,25):
        total = total + scoreboard[score][i]
    scoreboard[score][25] = total
    with open("out.csv", "a") as f:
        output = str(score[0]) + "," + str(score[1]) + "," + str(scoreboard[score][-1])
        f.write(output)