
import pandas
import random
import PySimpleGUI as sg

def setup():
    df= pandas.read_csv("question.csv")
    #take at maximum 30 elements from the dataframe randomically
    #if the dataframe has less than 30 elements take all
    df=df.sample(n=min(30,len(df)),random_state=random.randint(0,1000))
    questions={}
    for i in range(0, len(df)):
        questions[df["Question"][i]]=[df["Correct Answers"][i].split(sep=","),df["Wrong Answers"][i].split(sep=",")]
    
    return questions

def select_num(dictionary,num):
    new_dict={}
    keys=list(dictionary.keys())
    for i in keys:
        #select proportionally but  randomically correct and wrong answers
        correct=random.sample(dictionary[i][0],random.randint(1,min(num,len(dictionary[i][0]))))
        wrong=random.sample(dictionary[i][1],num-len(correct))
        all=correct+wrong
        random.shuffle(all)
        new_dict[i]={"all":all,"correct":correct,"wrong":wrong}
    return new_dict


def corrections(dictionary,answers_dict):
    return_dic=[]
    for question in answers_dict.keys():
        for answer in answers_dict[question]:
            if answer in dictionary[question]["wrong"]:
                return_dic.append((question,answer,"wrong"))
            else:
                return_dic.append((question,answer,"correct"))
    return return_dic
data=setup()
questions=select_num(data,4)
layout=[]
#print(questions)
correct_answers=0
for question in questions.keys():
    layout.append([sg.Text(question,key=question,font=("Helvetica", 20))])
    layout.append([sg.Checkbox(x,key=question+" "+x,font=("Helvetica",15)) for x in questions[question]["all"]])
    correct_answers=len(questions[question]["correct"])+correct_answers
layout.append([sg.Button("Submit")])
window=sg.Window(f"Quiz:0/{correct_answers}",layout,auto_size_text=True,auto_size_buttons=True)
while True:
    event,values=window.read()
    if event=="Submit":
        #reset color
        for element in values.keys():
            window[element].update(text_color='white')
        for element in questions.keys():
            window[element].update(text_color='white')

        #take only true values
        answers=[key for key,value in values.items() if value==True]

        answer_questions={}
        for element in answers:
            splitted=element.split(sep="? ")
            question=splitted[0]+"?"
            answer=splitted[1]
            if question in answer_questions.keys():
                answer_questions[question].append(answer)
            else:
                answer_questions[question]=[answer]
        correction=corrections(questions,answer_questions)
        correct=0
        wrong=0
        print(correction)
        countdic={}

        for element in correction:
            if element[2]=="correct":
                correct+=1
                if  element[0] in countdic and countdic[element[0]]!=False:
                    countdic[element[0]]+=1
                else:
                    countdic[element[0]]=1
                window[element[0]+" "+element[1]].update(text_color="light green")

            else:
                countdic[element[0]]=False
                wrong+=1
                window[element[0]+" "+element[1]].update(text_color="red")
        for element in countdic.keys():
            if countdic[element] == len(questions[element]["correct"]):
                window[element].update(text_color='light green')
        window.TKroot.title(f"Quiz:{correct}/{correct_answers}")
        if correct==correct_answers and wrong==0:
            sg.Popup("all correct")
            break
    if event==sg.WIN_CLOSED:
        break
window.close()

#MARTINA CHIEDE SE SU GITHUB POSSO DIRE CHE IL PYTHON NON SI PUò MODIFICARE
