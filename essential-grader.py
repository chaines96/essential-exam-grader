import csv, sys

def evaluate_quizzes(entrant_path="entrants.csv", selections_path="selections.csv",answers_path="answers.csv",total_quizzes=25):
    selections = list() 

    #File variables
    entrants_file = open(entrant_path, encoding="utf8")
    entrants = csv.reader(entrants_file, delimiter=',')
    try:
        selections_file = open(selections_path)
        selections  = csv.reader(selections_file, delimiter=',')
    except Exception as e:
        pass
    answers_file = open(answers_path)
    answers = csv.reader(answers_file, delimiter=',')

    #If the selections were not a single CSV file, we will make a list out of new ones.
    selections_list = list()
    selections_list_num = []
    quiz_index = 0
    while(quiz_index < total_quizzes):
        quiz_index = quiz_index + 1
        try:
            selections_quizfile = open("Quiz" + str(quiz_index) + "_Selections.csv", encoding="utf8")
            selections_list.append(csv.reader(selections_quizfile, delimiter=','))
            selections_list_num.append(quiz_index)
        except Exception as e:
            pass

    scoreboard = dict() #This is a dictionary whose keys are tuples (email,name) and whose values are lists

    #Populate the "score board"
    for entrant in entrants:
        blank_list = [0]*(total_quizzes+1)
        scoreboard.update({(entrant[0].lower().replace(" ",""),entrant[1].lower().replace(" ","")) : blank_list})

    #Read the scoreboard from a previous file
    try:
        previous_scores_file = open("prev.csv")
        previous_scores = csv.reader(previous_scores_file, delimiter=",")
    except Exception as e:
        print(e)
    try:
        for score in previous_scores:
            new_list = [0]*(total_quizzes+1) #Minus two lines to account for the name and email.
            for h in range(0,(len(score) - 3)): #We substract one from the length of score here because the total can be zero at this stage.
                try:
                    new_list[h] = int(score[h+2])
                except Exception as e:
                    print("Problem occured importing the score for " + score[1])
                    print(e)
            scoreboard.update({(score[0].lower().replace(" ",""),score[1].lower().replace(" ","")) : new_list})
    except Exception as e:
        print(e)

    #Variables
    QUIZ = 0
    comparison = list()
    amount_of_questions = 25 #How many questions in this quiz.

    #Evaluate each pick, of every week.
    for pick in selections:
        if pick[-1] != QUIZ: #only runs if week is different
            QUIZ = pick[-1]
            try:
                int(QUIZ) #If the last column is a number, by convention, we consider that the week number and we use it instead of the week index.
            except Exception as e:
                print(e)
                continue
            for answer in answers:
                #This finds the week of the given pick
                if answer[0] == QUIZ:
                    comparison = answer[:]
                    amount_of_questions = len(comparison) - 1
        #The comparison array now contains the correct values.
        weekly_score = 0
        try:
            if scoreboard[(pick[0].lower().replace(" ",""),pick[1].lower().replace(" ",""))][int(QUIZ)-1] == 0: #Newer entries come first in the list, so a duplicate entry is skipped.
                for i in range(2,amount_of_questions):
                    if pick[i] == comparison[i-1]: 
                        weekly_score = weekly_score + 1
                scoreboard[(pick[0].lower().replace(" ",""),pick[1].lower().replace(" ",""))][int(QUIZ)-1] = weekly_score
        except:
            with open('non_registered.txt', 'a') as a: #The entrant is not in the registrants. Score not updated.
                a.write(str((pick[0],pick[1])) + " in Week " + str(QUIZ) + "\n")

    #This loop is for week CSVs which are not contained in a selections.csv or registrants.csv file.
    inde = 0
    for week in selections_list:
        QUIZ = selections_list_num[inde]
        #We zero out the arrays if this week's score in the scoreboard in case it was overwritten with an incomplete file earlier.
        for the_score in scoreboard.values():
            the_score[QUIZ] = 0
        for answer in answers:
            #This finds the week of the given pick
            try:
                week_lookat = int(answer[0])
            except:
                week_lookat = 0 #Week is not an integer in this column so it is invalid and ust be skipped.
            if int(week_lookat) == QUIZ:
                comparison = answer.copy()
                amount_of_questions = len(comparison)
                break
        for pick in week:
            weekly_score = 0
            try:
                if scoreboard[(pick[0].lower().replace(" ",""),pick[1].lower().replace(" ",""))][int(QUIZ)-1] == 0: #Newer entries come first in the list, so a duplicate entry is skipped.
                    for i in range(1,(amount_of_questions+1)):
                        if pick[i].lower() == comparison[i-1].lower():
                            weekly_score = weekly_score + 1
                        scoreboard[(pick[0].lower().replace(" ",""),pick[1].lower().replace(" ",""))][int(QUIZ)-1] = weekly_score
            except:
                with open('non_registered.txt', 'a') as a: #The entrant is not in the entrants' list. Score not updated.
                    a.write(str((pick[0],pick[1])) + " in Week " + str(QUIZ) + "\n")
        #This space seems to cause the following two statements not to execute if it isn't here.
        inde = inde + 1 #Looks at the next entry in selections_list_num.
        comparison = list() #resetting

    #Given the weekly scores, we now compute all scores.
    for score in scoreboard:
        total = 0
        for i in range(0,total_quizzes):
            total = total + scoreboard[score][i]
        scoreboard[score][total_quizzes] = total
        with open("out.csv", "a", encoding="utf8") as f:
            output_string = str(score[0]) + "," + str(score[1]) + ","
            for k in range (0,(total_quizzes+1)): #The total is total_quizzes+1 because we write the final score too.
                output_string = output_string + str(scoreboard[score][k]) + ","
            output_string = output_string + "\n"
            f.write(output_string)

def main():
    entrant_path="entrants.csv"
    selections_path="selections.csv"
    answers_path="answers.csv"
    total_quizzes=25
    #Iterator over the arguments
    for i in range(1,len(sys.argv)):
        match argv[i]:
            case "-e":
                entrant_path = argv[i+1]
            case "-s":
                selections_path = argv[i+1]
            case "-a":
                answers_path = argv[i+1]
            case "-n":
                try:
                    total_quizzes = int(argv[i+1])
                except:
                    total_quizzes = 25
    evaluate_quizzes(entrant_path,selections_path,answers_path,total_quizzes)

main()