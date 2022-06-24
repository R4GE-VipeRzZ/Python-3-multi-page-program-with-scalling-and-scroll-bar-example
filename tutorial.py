from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.state("zoomed")


#Setup the main frame, canvas, scrollbar and child frames ----------------------------------------------------------------------------------------

#Create a main frame
mainFrame = Frame(root)
mainFrame.grid(row=0, column=0, sticky="nesw")
mainFrame.rowconfigure(index=0, weight=1)        #Set the row and column weight so that the frames that are added scale to the whole window
mainFrame.columnconfigure(index=0, weight=1)

#Creates a canvas
myCanvas = Canvas(mainFrame)
myCanvas.grid(row=0, column=0, sticky="nesw")

#Adds a scrollbar to the canvas
myScrollbar = Scrollbar(mainFrame, orient=VERTICAL, command=myCanvas.yview)     #Orient the scrollbar vertically and assign it to scroll in the y axis
myScrollbar.grid(row=0, column=1, sticky="ns")  #Places the scrollbar in column 1 as the canvas is in column 0

#Configure the canvas
myCanvas.configure(yscrollcommand=myScrollbar.set)      #Links the canvas with the scrollbar 
myCanvas.bind("<Configure>", lambda e: myCanvas.configure(scrollregion = myCanvas.bbox("all")))     #Set the Bbox so the scoll bar knows the scroll region when the scroll bar is first added to the canvas

#Create the frames for inside the canvas
canvasParentFrame = Frame(myCanvas)
menuFrame = Frame(canvasParentFrame)
childFrame1 = Frame(canvasParentFrame)
childFrame2 = Frame(canvasParentFrame)
childFrame3 = Frame(canvasParentFrame)

childFrameArray = [childFrame1, childFrame2, childFrame3]   #This array is used for controlling which childFrame is visible
CURRENT_CHILD_FRAME = 1       #Used to tell what frame is currently visible

menuFrame.grid(row=0, column=0, sticky="nesw")  #Places the menuFrame in row 0 of the canvasParentFrame
childFrame1.grid(row=1, column=0, sticky="nesw")    #Places the childFrame1 in row 1 of the canvasParentFrame

#Add that new frame to a window in the canvas
myCanvas.create_window((0,0), window=canvasParentFrame, anchor="nw")      #Adds a window into the top left corner of the canvas containing the specified frame
#--------------------------------------------------------------------------------------------------------------------------------------------------



#menuFrame code -----------------------------------------------------------------------------------------------------------------------------------

def hidePageFunc():     #This function hides all the child frames of the canvasParentFrame except the menuFrame
    for widget in canvasParentFrame.winfo_children():   #This for statemnt iterates through all the child frames in the canvasParentFrame
        if str(widget) != ".!frame.!canvas.!frame.!frame":      #Checks that the frame isnt the menuFrame
            widget.grid_forget()
    
def changeChildFrameFunc():     #The function is responsible for placing the correct childFrame onto the canvas and calling the correct functions to remove the other childFrame from the canvas and to resize the widgets
    global CURRENT_CHILD_FRAME

    hidePageFunc()  
    childFrameArray[CURRENT_CHILD_FRAME - 1].grid(row=1, column=0, sticky="nesw")     #This line places the new childFrame onto the grid in the canvasParentFrame grid
    resizeFunc()    #Called so that all the widgets in the newly added frame are scalled correctly to the window

#Click functions for the menu buttons

def clickBtn1Func():
    global CURRENT_CHILD_FRAME

    if CURRENT_CHILD_FRAME != 1:
        CURRENT_CHILD_FRAME = 1   #Set so that the correct button can be underlined in the menu
        changeChildFrameFunc()

def clickBtn2Func():
    global CURRENT_CHILD_FRAME

    if CURRENT_CHILD_FRAME != 2:
        CURRENT_CHILD_FRAME = 2   #Set so that the correct button can be underlined in the menu
        changeChildFrameFunc()

def clickBtn3Func():
    global CURRENT_CHILD_FRAME

    if CURRENT_CHILD_FRAME != 3:
        CURRENT_CHILD_FRAME = 3   #Set so that the correct button can be underlined in the menu
        changeChildFrameFunc()

#Sets the weight for the menuFrame grid
menuFrame.rowconfigure(index=0, weight=1)
menuFrame.columnconfigure(index=0, weight=1)
menuFrame.columnconfigure(index=1, weight=1)
menuFrame.columnconfigure(index=2, weight=1)

#Create menu buttons
menuBtn1 = Button(menuFrame, text="Page 1", command=clickBtn1Func, borderwidth=0)     #Borderwidth removes the buttons style
menuBtn2 = Button(menuFrame, text="Page 2", command=clickBtn2Func, borderwidth=0)
menuBtn3 = Button(menuFrame, text="Page 3", command=clickBtn3Func, borderwidth=0)

menuBtnArray = [menuBtn1, menuBtn2, menuBtn3]

#Adds the menu buttons to the menuFrame's grid
menuBtn1.grid(row=0, column=0)
menuBtn2.grid(row=0, column=1)
menuBtn3.grid(row=0, column=2)

#--------------------------------------------------------------------------------------------------------------------------------------------------



#ChildFrame1 code ---------------------------------------------------------------------------------------------------------------------------------

opened_img = Image.open(r"btn_image.jpg")   #Opens the image
scaled_img = ImageTk.PhotoImage(opened_img.resize((353, 199), Image.Resampling.LANCZOS)) #Resizes the image

imageBtnsArray = []         #Array used to store all of the image buttons so that they can be referenced later on

#This for loop creates all of the imageButtons that are in childFrame1
for imageBtn in range(0, 20):   #The range of this for loop decides the number of button that are created
    imageBtnsArray.append(Button(childFrame1, text=("Btn " + str(imageBtn + 1)), image = scaled_img, compound="top", borderwidth=0))
    #The text options sets the text that will be displayed in the button, the image option sets the image that will be displayed in the buuton, the compound option is
    #used to allow us to have both text and an image in the button, and top specifies that we want the image on top of the text, the borderwidth option remove the default
    #styling from the button


#Places the imagesButtons into the childFrame1's grid
x = 0 #x is used for the starting column number
n = 1 #n is used for the starting row number
for i in range(0, len(imageBtnsArray)):
    if x == 5:      #The value in this if statment is set to the number of columns that you want
        x = 0
        n = n + 1
    
    imageBtnsArray[i].grid(row=n, column=x)
    x = x + 1
#--------------------------------------------------------------------------------------------------------------------------------------------------



#ChildFrame2 code ---------------------------------------------------------------------------------------------------------------------------------

pg2Label = Label(childFrame2, text="This is frame 2", bg="green")
pg2Label.grid(row=1, column=0, columnspan = 3, sticky="nesw")
#--------------------------------------------------------------------------------------------------------------------------------------------------



#ChildFrame3 code ---------------------------------------------------------------------------------------------------------------------------------

pg3Label = Label(childFrame3, text="This is frame 3", bg="red")
pg3Label.grid(row=1, column=0, sticky="nesw")
#--------------------------------------------------------------------------------------------------------------------------------------------------



#scale widgets code--------------------------------------------------------------------------------------------------------------------------------
    
PREV_WIDTH = 0      #Used to store the windows width the last time it was resized
NEED_RESIZE = False     #Used to store a boolean value so that the resize function doesn't get run mulitiple times due to both the screen changing size
                        #and the mouse entering the screen having the potential to the ultimatly trigger the resize function

def menuUnderlineFunc(fontSize):        #This function is responsible for changing the size of the menu buttons text and underlining the text of the button that is currently been displayed
    for i in range (0, len(menuBtnArray)):
        if i == (CURRENT_CHILD_FRAME - 1):    #This if statement controls which menu option in underlined and sets the texts size
            menuBtnArray[i].config(font=("Times New Roman", fontSize, "underline"))
        else:
            menuBtnArray[i].config(font=("Times New Roman", fontSize))
            
def windowSizeChangeFunc(e):
    global NEED_RESIZE

    resizeBool = checkResizeFunc() #Calls the function to see if the window width has changed

    if resizeBool == True:  #This if stement check if the checkResizeFunc has returned True meaning that the widgets do need resizing
        if NEED_RESIZE != True:     #Checks that the NEED_RESIZE variable isn't already true as the mouse entering the screen could have already cause it to become true
            NEED_RESIZE = True
        print("Need to resize")

        root.after(600, resizeAfterTimeFunc)   #Used so that the widgets are resized after half a second if the mouse hasn't already triggered a resize by entering the window

def resizeAfterTimeFunc():
    global NEED_RESIZE

    #This if statment checks that the NEED_RESIZE variable is still true as the resizing of the widgets could have already been triggered by the mouse entering the scrollbar or canvas
    #meaning that the NEED_RESIZE variable would thus be False as the widgets would no longer need resizing
    if NEED_RESIZE == True: 
        resizeFunc()    

def updateBbox():   #This function is used to update the Bbox for the scrollbar so that the scroll will scroll to the correct location in the yaxis after the widgets have been resized
    myCanvas.configure(scrollregion=myCanvas.bbox("all"))

def resizeFunc():       #This function is responsible for resizing the widgets to the size of the window
    global NEED_RESIZE  #Needed so that it can be set back to false after resizing the widgets so that the widgets don't get unnecessarily scaled multiple times
    global RESIZED #Need to make the image a global variable so that the python garbage collector doesn't clean it up
    global CURRENT_CHILD_FRAME #Used to tell what child frame is currently visible

    canvas_width = myCanvas.winfo_width()    #Stores the current width of the canvas
        
    size = canvas_width / 40    #Dividing the window widths by 40 gives a good menu font size 
    menuUnderlineFunc(int(size))    #Calls the function that adjustts the text size of the menu buttons in accordance with the screen width and underlines the correct buttons text


    if int((canvas_width/38.6)) > 17:     #This if statement scales the x padding of the menu frame
        menuFrame.grid_configure(padx=(int((canvas_width/38.6) - 17),0))

    if int((canvas_width/46)) > 17:       #This if statement scales the x padding of the child frame that is currently visible
        childFrameArray[(CURRENT_CHILD_FRAME - 1)].grid_configure(padx=(int((canvas_width/46) - 17),0))


    #This if statement is responsible for making it so that only the child frame that is currently visible is resized to the window width
    if CURRENT_CHILD_FRAME == 1:  #If true this scales all the widgets on childFrame1 to the window width      
        if  int(canvas_width/9.64) > 0:       #Used to stop it from trying to scale an image to less than 1px
            RESIZED = ImageTk.PhotoImage(opened_img.resize((int(canvas_width/5.43), int(canvas_width/9.64)), Image.Resampling.LANCZOS))

            #Scales the meal buttons and images depending on the screen width
            for i in range(0, len(imageBtnsArray)):
                imageBtnsArray[i].config(width=int(canvas_width/5.43), height=int(canvas_width/8), font=("Times New Roman", int(canvas_width/87.27)), image=RESIZED, padx=int(canvas_width/192), pady=int(canvas_width/192))
    elif CURRENT_CHILD_FRAME == 2:    #If true this scales all the widgets on childFrame2 to the window width
        pg2Label.config(width = int(canvas_width/7.3), height = int((myCanvas.winfo_height() / 17.84)))
    elif CURRENT_CHILD_FRAME == 3:    #If true this scales all the widgets on childFrame3 to the window width
        pg3Label.config(width = int(canvas_width/7.3), height = int((myCanvas.winfo_height() / 17.84)))
        
    print("Widgets resized")
    

    root.after(200, updateBbox)     #Updates the Bbox for the scrollbar after a small time delay so that the changes in widgets dimensions have time to be implimented before the Bbox is updated 
    NEED_RESIZE = False

def checkResizeFunc():      #Checks the windows previous known width with the current known width so that the widgets arn't resized when they don't need to be
    global PREV_WIDTH
    canvas_width = int(myCanvas.winfo_width())    #Stores the current width of the canvas
    
    if canvas_width > 1:
        if PREV_WIDTH != canvas_width:
            PREV_WIDTH = canvas_width       #Save the canvas width to the PREV_WIDTH variable
            return True

def mouseEnterFunc(e):      #This function is triggered whenever the mouse enters the canvas or scrollbar
    global NEED_RESIZE

    if NEED_RESIZE == True:
        resizeFunc()
#--------------------------------------------------------------------------------------------------------------------------------------------------



#Event binding code--------------------------------------------------------------------------------------------------------------------------------
        
#Bind the apps configuration so that screen size chnages can be detected
root.bind("<Configure>", windowSizeChangeFunc)  #Event that is triggered when windows changes size
myCanvas.bind("<Enter>", mouseEnterFunc)   #Event that is triggered when the mouse enters the canvas
myScrollbar.bind("<Enter>", mouseEnterFunc)    #Event that is triggered when the mouse enters the scrollbar
#--------------------------------------------------------------------------------------------------------------------------------------------------



#Set the childFrame that is displayed when the window loads ---------------------------------------------------------------------------------------
CURRENT_CHILD_FRAME = 1
changeChildFrameFunc()
#--------------------------------------------------------------------------------------------------------------------------------------------------


root.mainloop()
