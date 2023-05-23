import random
import  os
from tkinter import *
from tkinter import ttk
import pandas as pd



class QUIZ:
    def __init__(self, path : str,question_num:int,answer_num:int)-> object:
        self.path = path
        self.quiz = {}
        self.correct_answers = 0
        self.Quiz_window = None
        self.Quiz_labels = {}
        self.Quiz_checkboxes = {}
        self.Quiz_buttons ={}
        self.totalwrong = 0
        print(question_num)
        self.setup(question_num)
        self.select_num(answer_num)
        self.setup_window()

        self.Quiz_canvas = Canvas(self.Quiz_window)
        self.Quiz_scrollbar = Scrollbar(self.Quiz_window, orient="vertical", command=self.Quiz_canvas.yview)
        self.Quiz_canvas.configure(yscrollcommand=self.Quiz_scrollbar.set)
        self.Quiz_scrollbar.pack(side="right", fill="y")
        self.Quiz_canvas.pack(side="left", fill="both", expand=True)
        self.create_widgets()


        self.Quiz_canvas.create_window((0, 0), window=self.Quiz_frame, anchor="nw")

        self.Quiz_frame.bind("<Configure>", self.on_frame_configure)
        self.Quiz_frame.bind("<Enter>", self.bind_mousewheel)
        self.Quiz_frame.bind("<Leave>", self.unbind_mousewheel)
        self.Quiz_window.mainloop()


    def on_frame_configure(self, event):
        self.Quiz_canvas.configure(scrollregion=self.Quiz_canvas.bbox("all"))


    def bind_mousewheel(self, event):
        self.Quiz_frame.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbind_mousewheel(self, event):
        self.Quiz_frame.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        self.Quiz_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


    def get_questions(self):
        return self.questions.keys()    
    def setup_window(self):
        self.Quiz_window = Tk()
        self.Quiz_window.title(f"Business QUIZ - correct answers: 0/{self.correct_answers}")

        self.Quiz_window.geometry("800x600")
        self.Quiz_window.resizable(True, True)
        self.Quiz_window.config(bg="black")
    def create_widgets(self):
        self.Quiz_frame = Frame(self.Quiz_canvas, bg="black")
        for i,question in enumerate(self.quiz.keys()):
            self.Quiz_labels[question] = Label(self.Quiz_frame, text=question, font=("Helvetica", 20), fg="white",bg="black")
            self.Quiz_labels[question].pack(anchor=W)
            for i, answer in enumerate(self.quiz[question]["all"]):
                if question not in self.Quiz_checkboxes.keys():
                    self.Quiz_checkboxes[question] = [[answer, BooleanVar()]]
                else:
                    self.Quiz_checkboxes[question].append([answer, BooleanVar()])

                checkbox = Checkbutton(self.Quiz_frame, text=answer, highlightthickness=0,
                                       variable=self.Quiz_checkboxes[question][i][1], bg="black", fg="white",
                                       selectcolor="black", activebackground="black", activeforeground="white",
                                       font=("Helvetica", 15))
                checkbox.pack(anchor=W)
                self.Quiz_checkboxes[question][i].append(checkbox)
        self.Quiz_buttons["Submit"] = Button(self.Quiz_frame, text="Submit", command=self.submit)
        self.Quiz_buttons["Submit"].pack()

    def setup(self,question_num:int ):
        # read csv file
        df = pd.read_csv(self.path)
        # select random n  questions in random order
        random_numbers = random.sample(range(0, len(df)), min(question_num,len(df)))

        # create dictionary
        for i in range(0, len(random_numbers)):
            self.quiz[df["Question"][random_numbers[i]]] = [
                df["Correct Answers"][random_numbers[i]].split(sep=","),
                df["Wrong Answers"][random_numbers[i]].split(sep=","),
            ]
        print(df)
    
    def submit(self):
        correct=0
        real_correct=0
        for question in self.quiz.keys():
            this_question_correct = 0
            for checkbox in self.Quiz_checkboxes[question]:
                checkbox[2].config(fg="white")
                if checkbox[1].get() and checkbox[0] in self.quiz[question]["wrong"]:
                   checkbox[2].config(fg="red")
                   this_question_correct-=1
                   self.totalwrong+=1
                elif checkbox[1].get() and checkbox[0] in self.quiz[question]["correct"]:
                    this_question_correct+=1
                    real_correct+=1
                    checkbox[2].config(fg="light green")

            correct+=this_question_correct
            if this_question_correct == len(self.quiz[question]["correct"]) :
                self.Quiz_labels[question].config(fg="light green")
            
        self.Quiz_window.title(f"Business QUIZ - correct answers: {real_correct}/{self.correct_answers}")
        if correct == self.correct_answers:
            #create popup and on ok close everything
            popup = Tk()
            popup.title("Congratulation")
            popup.resizable(False, False)
            popup.config(bg="black")
            label = Label(popup, text=f"Congratulation you answered all questions correctly with {self.totalwrong} wrong answers", font=("Helvetica", 15),fg="white",bg="black")
            label.pack()
            button = Button(popup, text="OK", command=quit)
            button.pack()
            popup.mainloop()

        
        
    def select_num(self,num):
        new_dict = {}
        keys = list(self.quiz.keys())
        for i in keys:
            # select proportionally but  randomically correct and wrong answers
            correct = random.sample(
                self.quiz[i][0], random.randint(1, min(num, len(self.quiz[i][0])))
            )
            wrong = random.sample(self.quiz[i][1], num - len(correct))
            all = correct + wrong
            random.shuffle(all)
            new_dict[i] = {"all": all, "correct": correct, "wrong": wrong}
            self.correct_answers = len(new_dict[i]["correct"])+self.correct_answers
        self.quiz = new_dict


def main(path :str):
   # a window to select how many questions to generate and how many answers per question
    root = Tk()
    root.title("Business QUIZ")
    root.geometry("500x500")
    root.resizable(False, False)
    root.config(bg="black")
    label = Label(root, text="How many questions do you want to answer?", font=("Helvetica", 15),fg="white",bg="black")
    label.pack()
    num_questions = IntVar()
    num_questions.set(30)
    num_questions_spin = Spinbox(root,textvariable=num_questions)
    num_questions_spin.pack()
    label = Label(root, text="How many answers per question do you want to have?", font=("Helvetica", 15),fg="white",bg="black")
    label.pack()
    num = IntVar()
    num.set(4)
    num_answers = Spinbox(root, from_=1, to=10, textvariable=num)
    num_answers.pack()
    button = Button(root, text="OK", command=lambda: [root.destroy(),QUIZ(path,int(num_questions.get()),int(num.get()))])
    button.pack()
    root.mainloop()


if __name__ == "__main__":
    main("question.csv")