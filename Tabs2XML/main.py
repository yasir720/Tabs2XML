# hello_world.py

import PySimpleGUI as sg
import os.path
import conversionEngine as CE
import shutil
import string
import numpy as np

# First the window layout in 2 columns





def isAllStringsSameLength(tab):
  same = True
  stringLength = 0
  for s in tab:
    setS = set(s)
    if '|' in setS:
      if stringLength == 0:
        stringLength = len(s)
      else: 
        if len(s) != stringLength:
          same = False; 
          break
  return same


def isNotEmpty(tab):
  return len(tab) != 0



  
def isAllBarsonSameLine(tab):
  b = True
  for s in tab: 
    setS = set(s)
    if len(setS) > 1 and s[0] == "|": 
      b = False
      break
  return b;   

def isBounded(regTab): #input regular tab as well, 
    first = regTab[0].find("|")
    last = regTab[0].rfind("|")
    return first == 0 or first == 1 or first == 2 and last == len(regTab[0])
    
    
   

def isFirstCharactersInTabValid(tab):
    #check the letters before the first vert bar
    if tab[0][0] != "|":
        #do something
        print(tab[0])
    else:
        return True 

      


          

    


#say that there is no elemnt besides the wierd letter thing to show what string it is before the first bare, and show there is no element after last occurance of a vertical bar.

def isUnrecognizedCharacter(tab):
    row = 0 
    col = 0
    problem = False
    character = ""
    ind = 0; 
    for t in tab:
        
        
        row = row + 1 
        
        for x in t:  
            if x != "|" and x != "-" and x != "h" and x != "p" and x != "b" and x != "r" and x != "/" and x != "\\" and x != "v" and x != "t" and x != "s" and x != "S" and x != "*" and x != "[" and x != "]" and x != "n" and x != "(" and x != ")" and x != "T" and x != "P" and x != "M" and x != "=" and x != "<" and x != ">" and x != "x" and x != "o" and x != "·" and x != "0" and x != "1" and x != "2" and x != "3" and x != "4" and x != "5" and x != "6" and x != "7" and x != "8" and x != "9" and x!="e" and x!="B" and x!="G" and x!="D" and x!="A" and x!="E":
                problem = True; 
                print(x)
                character = x
                ind = t.index(x)
                break

            col = col + 1
    if problem: 
        return ind
    else: 
        return problem

      


varTimeSig = ["1/4", "2/4", "3/4", "4/4"]

file_list_column = [
    [
        sg.Text("Tablature File Location"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
    [
        sg.Text("Enter name of piece:          "),
        sg.In(size=(25, 1), enable_events=True, default_text = "Classical Guitar", key="-pieceName-"),
        
        
    ],
    [
        sg.Text("Select time signature of piece"),
        sg.Listbox(varTimeSig, default_values = varTimeSig[3], size=(5,4), key='-LIST-'),
        
        
    ],
    [
        sg.Text("Save Location of MusicXML"),
        sg.In(size=(25, 1), enable_events=True, key="-saveLocation-"),
        sg.FolderBrowse(),
        
    ],
    [
        sg.Button("convert")
    ],

    #[sg.Text(size=(40,1), text = "Error: none", key="-errorCheck-")],

    

]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    #[sg.Text("Choose a tablature from list on left:")],
    [sg.Text(size=(60,2), text = "Todo: Choose a tablature from the list on the left", text_color = "pink", key="-userTodo-")],
    [sg.Multiline(size=(60, 30), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
    [sg.Text(size=(60,2), text = "", text_color = "pink", key="-error-")],

    
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Tabs2XML", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".txt"))
        ]
        window["-FILE LIST-"].update(fnames)
        window["-userTodo-"].update("Todo: Select tablature to convert from the list on the left")
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-userTodo-"].update("Todo: Enter the name and the save location then hit convert")
            
            assPoop = open(filename, "r")
            window["-TOUT-"].update(assPoop.read())

           
            
            window["-IMAGE-"].update()
            

        except:
            pass
    elif event == "convert" :
        try:
            save_path = values["-saveLocation-"]
            file_name = values["-pieceName-"]
            timesig = values["-LIST-"]
            text = values["-TOUT-"]
            
            
            completeName = os.path.join(save_path, file_name+".musicxml")
            

            if filename == "" or text == "":
                sg.popup("please choose a file to convert") 
            elif save_path == "":
                sg.popup("please specify save path")
            elif file_name == "":
                sg.popup("please specify the name of the piece")
            elif timesig == "":
                sg.popup("please specify the timeig of the piece")
            
            else: 
                #test if its a valid tab
                txt = text.split() # txt is array for file, text is string of file

                textarr = []
                for t in txt:
                    textarr.append(list(t))

                
                if isAllStringsSameLength(txt) == False: 
                    window["-error-"].update("all strings are not the same length!")
                elif isNotEmpty(txt) == False:
                    window["-error-"].update("the Ascii Tab is empty")
                else:
                    window["-error-"].update("")
                    numpy_array = np.array(textarr)
                    transpose = numpy_array.T
                    transpose_list = transpose.tolist()
                        
                    print("all strings same length "+str(isAllStringsSameLength(txt)))
                    print("not empty "+str(isNotEmpty(txt)))
                    
                    print("is bars on same line "+str(isAllBarsonSameLine(transpose_list)))
                    print("is bouded "+str(isBounded(txt)))
                    print("is first characted in the tab valid "+str(isFirstCharactersInTabValid(transpose_list)))
                    CE.xmlConverter(text,completeName, timesig)
                    bigPoop = open(completeName, "r")
                    window["-TOUT-"].update(bigPoop.read())
                    window["-userTodo-"].update("Todo: Select another tablature text file and if needed, change the tablature directory")
                


  

                

                
                # file1 = open(completeName, "w")
                # file1.write("")
                # file1.close()
            

        except:
            #onl shows if there is nothing to convert thats why this popup is here instead of an if statement 
            sg.popup("please choose a file to convert")
            
        
        