import csv

#File variables
entrants_file = open("entrants.csv")
entrants  = csv.reader(entrants_file, delimiter=',')
student_answers_file = open("student_answers.csv")
student_answers  = csv.reader(student_answers_file, delimiter=',')
answer_key_file = open("answer_key.csv")
answer_key  = csv.reader(answer_key_file, delimiter=',')

scoreboard = dict() #This is a dictionary whose keys are tuples (email,name) and whose values are lists

#Populate the "score board"
for entrant in entrants:
    blank_list = [0]*26
    scoreboard.update({(entrant[0],entrant[1]) : blank_list})

#Variables
WEEK = 0
comparison = list()
amount_of_questions = 25 #How many questions available this quiz

#Evaluate each pick of every answer in every quiz.
for pick in student_answers:
    if pick[-1] != WEEK: #only runs if week is different
        WEEK = pick[-1] #Determine which week we are comparing, which we assume is the last column
        for answer in answer_key:
            #This finds the week of the given pick
            if answer[0] == WEEK:
                comparison = answer[:]
                amount_of_questions = len(comparison) - 4
    #The comparison array now contains the correct values.
    quiz_score = 0
    for i in range(2,amount_of_questions):
        if pick[i] == comparison[i-1]:
            quiz_score = quiz_score + 1
    try:
        scoreboard[(pick[0],pick[1])][int(WEEK)-1] = quiz_score
    except:
        pass #The entrant is not in the registrants. Score not updated.

#Given the weekly scores, we now compute all scores.
for score in scoreboard:
    total = 0
    for i in range(0,25):
        total = total + scoreboard[score][i]
    scoreboard[score][25] = total
    with open("out.txt", "a") as f:
        f.write(str(score))
        f.write(str(scoreboard[score]))
        f.write('\n')