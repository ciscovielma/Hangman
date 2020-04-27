"""
Cisco Vielma
cvielma@wesleyan.edu
COMP 112 section 4
Final Project 2018.12.10

Hangman using a two classes
1 for logic and 1 for GUI
Widgets:root window,labels,Buttons, canvas
"""

import tkinter as tk
import random

#utility functions

#used to see if all chars in a word have been typed
#Thus you WIN when string_minus returns the empty string
def string_minus(s1,s2):
    """
    s1,s2:strings
    return:string consisting of letters in s1 not in s2
    string_minus("automobile","aom") ==> "utbile"
    string_minus("hola","lhaoxy") ==>""
    """
    diff=""
    for char in s1:
        if not(char in s2):
            diff=diff+char
    return diff

def make_display_word(word,letters_used):
    """
    word:str
    letters_used:str
    return:str - word, with underscores for letters
    that have not been used yet
    make_display_word ("automobile","aom") ==> "a __ __ o m o __ __ __ __"
    """
    display_word = ""
    for char in word:
        if char in letters_used:
            display_word += char+"  "
        else:
            display_word += "__  "
    return display_word


#graphical layer
class Hangman_gui:
    """
    The graphical display part of
    Hangman
    """
    def __init__(self):
        """
        hangman_gui attributes:
        a root window, two labels, a button
        and a canvas
        label 1 will dislay the word
        label 2 displays "you won" or "you lost"
        """
        self.game = Hangman_game()
        self.tkroot = tk.Tk()     #The frame holding all the components

        labelfont= ('helvetica',12,'bold')

        self.label1 = tk.Label(self.tkroot)
        self.label2 = tk.Label(self.tkroot)
        self.label3 = tk.Label(self.tkroot) #elegance???
        self.make_labels(labelfont)

        button = tk.Button(self.tkroot,text="Restart Game") #elegance???
        self.make_buttons(button)

        self.canvas = tk.Canvas(self.tkroot)
        self.make_canvas()

        self.tkroot.title("Hangman")
        self.tkroot.geometry("400x400+5+5")
        self.tkroot.focus()

        #create a hangman game object
        #self.game = Hangman_game()
        self.start()

    def start(self):
        self.game.start()
        #start the logic part, and then do the following:
        self.label1.config(text = make_display_word(self.game.word,""))
        self.label1.pack()
        self.make_canvas()
        self.tkroot.bind('<KeyPress>',self.onkeypress)

        self.tkroot.mainloop()


    def make_buttons(self,button):
        """
        configure restart button and pack it
        set its command function to self.restart
        """
        button.config(command = self.restart)
        button.pack()


    def make_canvas(self):
        """
        configure and pack canvas
        """

        """
        Scaffold for Hangman Game
        """
        self.canvas.config(height = 150,width=50)
        self.canvas.pack(expand=True,fill='both')
        self.canvas.create_line(0,150,100,150, fill="black") #base
        self.canvas.create_line(50,25,50,150, fill="black")  #vertical stick
        self.canvas.create_line(50,25,100,25, fill="black")  #horizontal stick
        self.canvas.create_line(100,25,100,50, fill="black")  #noose

        """
        actual hangman
        """
        if len(self.game.body_parts_used) == 1:
            self.canvas.create_oval(90,50,110,70, fill="black")   #head
        elif len(self.game.body_parts_used) == 2:
            self.canvas.create_line(100,70,100,100, fill="black") #body
        elif len(self.game.body_parts_used) == 3:
            self.canvas.create_line(100,85,110,75, fill="black")  #rightarm
        elif len(self.game.body_parts_used) == 4:
            self.canvas.create_line(100,85,90,75, fill="black")   #leftarm
        elif len(self.game.body_parts_used) == 5:
            self.canvas.create_line(100,100,110,110, fill="black")  #rightleg
        if len(self.game.body_parts_used) == 6:
           self.canvas.create_line(100,100,90,110, fill="black")   #leftleg
        else:
            pass

        labelfont= ('helvetica',12,'bold')
        self.make_labels(labelfont)

    def make_labels(self,fnt):
        """
        configure the necessary labels
        and pack them
        """

        self.label2.config(text = self.game.message_string)
        self.label2.pack()
        """
        Elegance?
        """
        self.label3.config(text = "Letters used: {}".format(self.game.letters_used))
        self.label3.pack()

        if self.game.status() == Hangman_game.LOSE:
            self.label1.config(text = "THE WORD WAS:  {}".format(self.game.word))
            self.label1.pack()
        else:
            self.label1.config(text = make_display_word(self.game.word,self.game.letters_used))
            self.label1.pack()

    def onkeypress(self,event):
        """
        define action carried out when user types a character
        it will be called self.onkeypress
        --grab the character typed by the user
        --update the logic game with the character typed by the user
        --update the texts on labels 1 and 2
        display the word (by updating the text on label1)
        """
        ch = event.char  #get the character typed by the user
        self.tkroot.bind('<KeyPress>',self.onkeypress)
        self.game.update_game(ch)
        self.make_canvas()

        #and more


    def restart(self):
        """
        restart the game
        change text displayed on labels
        clear the canvas
        using  self.canvas.delete("all")
        """
        self.canvas.delete("all")
        self.start()




#logic part of game
class Hangman_game:

    WIN = 1
    LOSE =-1
    PLAY = 0
    def __init__(self):
        #you can replace this with a list of the words in the file
        #words.txt (100,000 words!) on the Moodle page.
        #then you can uncommlent the following:

        vocab = open("words.txt")
        self.words = list(vocab)

        """
        The file words.txt should be in the
        same folder as this program for everything to work
        Download the file from
        """
        self.start()

    def start(self):
        self.game_over = False
        self.body_parts_remaining = ["head","body","right arm","left arm","right leg","left leg"]
        self.body_parts_used =  []

        self.word = random.choice(self.words).strip();
        self.letters_used = ""
        self.message_string="" # to report a win or loss to player

    def make_display(self):
        """
        creates word with underscores for missing letters
        uses make_display_word, defined at top
        make_display_word ("automobile","aom") ==> "a __ __ o m o __ __ __"
        """
        return make_display_word(self.word,self.letters_used)

    def update_game(self,char):
        """
        THIS IS THE MOST IMPORTANT METHOD
        char:str - a single letter
        result:update letters_used,
        If char not in word update body_parts_used and
        body_parts_remaining (using the update_body_parts method)
        """
        #DO NOTHING if letter has already been typed
        #or if the game is over
        if char in self.letters_used or self.game_over:
            pass #leave this pass here
        else:
            self.letters_used += char
            if char not in self.word:
                self.update_body_parts()
            else:
                pass
            self.make_display()
            self.status()
            self.win_game()
            self.lose_game()
            """
            update letters_used, also body parts information
            if necessary
            and check for the end of the game (win or loss)
            """

    def update_body_parts(self):
        self.body_parts_used.append(self.body_parts_remaining[0])
        del self.body_parts_remaining[0]
        """
        add the next body part to body_parts_used and remove it from
        body_parts_remaining
        """

    def status(self):
        if self.body_parts_remaining == []:
            st = Hangman_game.LOSE
        elif string_minus(self.word,self.letters_used) == "":
            st = Hangman_game.WIN
        elif string_minus(self.word,self.letters_used) != "":
            st = Hangman_game.PLAY
        else:
            pass
        return st


    def win_game(self):
        """
        result:notify player of win (by changing self.message string)
        and update the game_over attribute
        """
        if self.status() == Hangman_game.WIN:
            self.message_string = "YOU WIN!"
            self.game_over = True
            return str(self.message_string)
        else:
            pass

    def lose_game(self):
        """
        result:notify player of loss
        and display the word they failed to guess
        (by updating self.message_string)
        and update the game_over attribute
        """
        if self.status() == Hangman_game.LOSE:
            self.message_string = "YOU LOSE!"
            self.game_over = True
            return str(self.message_string)
        else:
            pass


#This starts everything.
Hangman_gui()
