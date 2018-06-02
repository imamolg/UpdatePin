
import tkinter
from tkinter import *
from tkinter.messagebox import *
import os
import pickle




#### Region 1. Message Boxes 


## Message to show when file not found.
def file_not_found():
    showerror(title="File error", message="Error opening the pin number file.")
    

    
## Message to show when user name does not found.
def wrong_user():
    showwarning(title="User name problem", message="User name was not found.")
    

## Message to show when pin does not match
def wrong_pin():
    showwarning(title="Pin number status", message="Your old pin is incorrect.")

## Message to show when about button pressed
def pin_updated():
    showinfo(title="Pin number status", message="Your pin has been updated.")

## Message to show when pin is updated
def about_button():
    showinfo(title="Help about", message="Version 1.0 By Amol G ")


## Message to show when new pin number does not meet requirement

def new_pin_standard():
    showwarning(title="Pin number status", message="Your new pin does not meet the security standard.")



#### Region 2. All required Functions 
    
## Check if pin file readable.
## Pin file to read and write.
pin_file = "PinNumbers.p"
    
def read_file():
    """
        Read the file and saves it in dictionary
        Also takes user input and stores it to variables.
    """
    try:
        fileRead =open(pin_file,"rb")
        global userPwd_Dict
        userPwd_Dict = pickle.load(fileRead)
        ## taking user input and saving to variables. 
        global userName
        userName= user_name.get().lower()
        global oldPin
        oldPin= old_pin.get()
        global newPin
        newPin= new_pin.get()
        global confirmNewPin
        confirmNewPin= confirm_new_pin.get()
        clear_text()
        if(len(userPwd_Dict) == 0): #If there is nothing in dictionary then give msg.
            wrong_user()
        else:# If everything is ok 
            user_input()

    # If file not found.    
    except:
        file_not_found()

        
   
    
## get user input and check user name and password is match.

def user_input():
    """Checks if user name and password is match."""   
    if (userName in userPwd_Dict):
        pinInFile = userPwd_Dict[userName]
        if (pinInFile == oldPin):
            ## Check if new password meets requirements.
            errorVal=password_requirement()
            if(errorVal == 0):
                ## If all good store new pin to file.
                update_password()
            else:new_pin_standard()
        else:wrong_pin()
    else:wrong_user()
 
  





## Checking password requirement
"""password requirnment
"Must be only digits in the range 0 to 9"
"Must be exactly 5 digits in length.
"No digits can be repeated.
"Adjacent digits must not be sequential."
"""

def password_requirement():
    """
    Checks password requirement.
    Password must be,
       only number in range 0-9,
       exactly 5 digits,
       no repetation,
       no sequential.
    """
    numList=[]
    error=0
    if(newPin==confirmNewPin and len(newPin) == 5 and newPin.isnumeric() and newPin != ''):
        passwordLen=len(newPin)
        for n in range(passwordLen):          
            curNum= int(newPin[n])
            if(n < passwordLen-1):
                nextNum= int(newPin[n+1])
                if(curNum == nextNum-1 or curNum == nextNum+1 or curNum == nextNum):
                    error=1
                    break
            if(curNum in numList):
                error=1
                break
            numList.append(curNum)
            
    else:
        error = 1
        
    return error


## Clear text boxes
def clear_text():
    user_name.delete(0, 'end')
    old_pin.delete(0, 'end')
    new_pin.delete(0, 'end')
    confirm_new_pin.delete(0, 'end')


## If pin meets requirement, update the file.
def update_password():
    """ Updates the file and set new user pin"""
    try: 
        userPwd_Dict[userName]= newPin
        fileWrite=open(pin_file,"wb")
        pickle.dump(userPwd_Dict,fileWrite)
        fileWrite.close()
        pin_updated()
    # If problem with file while writing.    
    except:
        file_not_found()
        
    
     

    
#### Region 3. Graphical User Interface

# Create the root window
pin_window = tkinter.Tk()
pin_window.title("Pin number validation")
pin_window.geometry("380x280+500+100")

# menu buttons
main_menu = Menu(pin_window)
pin_window.config(menu=main_menu)
file_menu = Menu(main_menu)
main_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label = "Update Pin", command = read_file)
file_menu.add_separator()
file_menu.add_command(label = "Exit", command =pin_window.destroy)
help_menu = Menu(main_menu)
main_menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label = "About", command = about_button)

#text buttons

middle_frame = Frame(pin_window)
middle_frame.pack()


user_name_label = Label(middle_frame, text="User name : ",height =2)
user_name_label.grid(column=0, row=2 )

user_name = Entry(middle_frame, width=10)
user_name.grid(column=0, row=3)
user_name.focus_set()

old_pin_label = Label(middle_frame, text="Pin number : ",height =2)
old_pin_label.grid(column=0, row=5)

old_pin = Entry(middle_frame, show="*", width=7)
old_pin.grid(column=0, row=6)

new_pin_label = Label(middle_frame, text="New pin number : ",height =2)
new_pin_label.grid(column=0, row=8)

new_pin = Entry(middle_frame, show = "*", width=7)
new_pin.grid(column=0, row=9)

confirm_new_pin_label = Label(middle_frame, text="Confirm new pin number : ",height =2)
confirm_new_pin_label.grid(column=0, row=10)

confirm_new_pin = Entry(middle_frame, show = "*", width=7)
confirm_new_pin.grid(column=0, row=11)

update_pin_buttun = Button(text="Update Pin", width=15,height =2,command = read_file)
update_pin_buttun.place(relx=.5, rely=.9, anchor="c")

pin_window.resizable(width=False, height=False)

# Keep the window running
pin_window.mainloop()

