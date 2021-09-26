import xml.etree.cElementTree as ET
import lxml.etree as etree
import numpy as np
from xml.dom import minidom
from itertools import cycle
# grace doesnt work but everything else does -ALP


def xmlConverter(someFile, nameFile, piece_name, timeSig):
    
    timeSig = timeSig[0]
    def isAlter(alterednote):
        arrOfAlter = ['F#', 'G#', 'A#', 'C#', 'D#']
        arrOfNonAlter = ['F', 'G', 'A', 'C', 'D']
        if alterednote in arrOfAlter:
            return arrOfNonAlter[arrOfAlter.index(alterednote)]
        else:
            return False
    # =======CLASSES TO USE LATER=============

    class Note:
        letter = ''
        Octave = ''
        duration = ''
        typeOfNote = ''  # type of note
        alter = 'not_altered'  # sharp or not
        string = ''
        fret = ''
        voice = '1'
        grace = False
        position = 0
        hstart = False
        hstop = False
        pstart = False
        pstop = False
        isitslur = False
        slurAmount = 0



        def __init__(self, letter, Octave):
            if isAlter(letter):
                self.letter = isAlter(letter)
                self.alter = '1'
            else:
                self.letter = letter
            self.Octave = Octave

        def setDuration(self, duration):
            self.duration = str(duration)

        def setTypeOfNote(self, typeOfNote):
            self.typeOfNote = typeOfNote

        def isChord(self):
            return False

        def getType(self):
            return self.typeOfNote

        def setAlter(self):
            self.alter = '1'

        def getAlter(self):
            return self.alter

        def setString(self, string):
            self.string = string

        def setFret(self, fret):
            self.fret = str(fret)

        def setVoice(self, voice):
            self.voice = voice

        def isGrace(self):
            return self.grace

        def countSlurs(self):
            if self.hstart:
                self.slurAmount += 1
            if self.hstop:
                self.slurAmount += 1
            if self.pstart:
                self.slurAmount += 1
            if self.pstop:
                self.slurAmount += 1




    def whatOctave(string, fret):
        tempoctave = 0
        fret = int(fret)

        if string == 3:
            if fret <= 7:  # indexed E = 0 and b = 7 for me -alp: kalin e teli bu
                tempoctave = 1
            else:
                tempoctave = 2
        elif string == 2:  # A
            if fret <= 3:
                tempoctave = 1
            else:
                tempoctave = 2
        elif string == 1:  # D
            if fret <= 9:
                tempoctave = 2
            else:
                tempoctave = 3
        elif string == 0:
            if fret <= 4:
                tempoctave = 2
            else:
                tempoctave = 3
        else:
            print("String input might be wrong")
        # print string, 'string whattt'
        # print fret, 'fret'

        # print(tempoctave)
        return str(tempoctave)





    
    text = someFile.split()
    textarr = []



    # Python3 program to Split string into characters
    for t in text:
        textarr.append(list(t))

    numpy_array = np.array(textarr)
    transpose = numpy_array.T
    transpose_list = transpose.tolist()




    def duration(fret):  # find the next occurence of a number
        dur = 0

        for i in range(fret, len(transpose_list)):
            if transpose_list[i][0] == "-" and len(
                    set(transpose_list[i])) == 1:  # if the first "|" occurs, then the first measure starts
                dur += 1
            else:
                break
        if dur > 8:
            return 8
        else:
            return dur


    durations = []
    for i in range(len(transpose_list)):
        durations.append(duration(i))

    notes = []


    ##function gets the name of the note that was played
    def noteFun(_string, fret):
        fret = int(fret)
        enote = ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"]

        enote = ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"]
        if fret >= 12:
            fret_use = fret - 12
        else:
            fret_use = fret

        switcher = {  # default tuning mapping based of string.
            0: ["G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#"],
            1: ["D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#"],
            2: ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
            3: ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#"],
        }


        return switcher.get(_string)[fret_use]



    def isChord(fret):
        if len(set(fret)) > 2:
            return True
        else:
            return False


    def isNum(x):
        num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "13", "14"]
        return x in num


    def numToString(n):
        letters = ["E", "A", "D", "G", "B", "E"]
        return letters[n]


    score_partwise = ET.Element("score-partwise", version="3.1")
    part_list = ET.SubElement(score_partwise, "part-list")

    score_part = ET.SubElement(part_list, "score-part", id="P1")

    part_name = ET.SubElement(score_part, "part-name").text = piece_name  # input part name here from user

    part = ET.SubElement(score_partwise, "part", id="P1")

    tree = ET.ElementTree(score_partwise)


    # place notes

    def makeNote(letter, octave):
        return Note(letter, octave)




    # function that takes one line until the '|' and sets everything for that line only, call a for loop later
    def isLetter(string):
        if string == '-':
            return False
        else:
            return True


    class Measure:
        notes = []
        repeates = 1
        measureLineLength = 0
        timeSig = ""
        changed = False

        def __init__(self):
            pass

        def setRepeats(self, repeats):
            self.repeates = repeats

        def addNotes(self, notes):
            self.notes = notes

        def chordType(self):
            # print self.notes
            if self.notes[0].typeOfNote == '':
                for idx, note in enumerate(self.notes):
                    if note.typeOfNote != '':
                        default = note.typeOfNote
                        defaultDur = note.duration
                        break
                for i in range(0, idx):
                    self.notes[i].typeOfNote = default
                    self.notes[i].duration = defaultDur

            for index, nt in enumerate(self.notes):
                if nt.typeOfNote == '':
                    tempi = index
                    beggining = index
                    while(self.notes[tempi].typeOfNote == ''):
                        tempi += 1
                    for j in range(beggining, tempi):
                        self.notes[j].typeOfNote = self.notes[tempi].typeOfNote
                        self.notes[j].duration = self.notes[tempi].duration

        def doLastThing(self):
            for note in self.notes:
                if note.hstart or note.hstop or note.pstart or note.pstop:
                    note.isitslur = True
                note.countSlurs()






    def MeasureNoteTypeHelper(note, ratio, timeSig):
        typeOfNotes = ["16th", "eighth", "quarter", "half", "whole"]
        total = 8

        if timeSig == "4/4":
            total = 8
        elif timeSig == "3/4":
            total = 6
        elif timeSig == "3/8":
            total = 3
        elif timeSig == "2/4":
            total = 4
        elif timeSig == "2/2":
            total = 8
        elif timeSig == "5/4":
            total = 10

        amountOfEight = float(total * ratio)
        # print float(total * ratio)

        if amountOfEight <= 0.65:
            note.typeOfNote = typeOfNotes[0]
            note.duration = "1"
        elif amountOfEight <= 1.25:
            note.typeOfNote = typeOfNotes[1]
            note.duration = "1"
        elif amountOfEight <= 2.5:
            note.typeOfNote = typeOfNotes[2]
            note.duration = "2"
        elif amountOfEight <= 5:
            note.typeOfNote = typeOfNotes[3]
            note.duration = "4"
        elif amountOfEight <= 7.9:
            note.typeOfNote = typeOfNotes[4]
            note.duration = "8"



    # ==The new type calculator
    def MeasureTypeCalculator(timeSig, measureList):
        for measure in measureList:
            #  if position can not be assigned == 0 then leave it for later, if positions are the same,assign it later
            for idx, note in enumerate(measure.notes):

                notePosition = note.position
                if idx == len(measure.notes) - 1:
                    NextNotePosition = measure.measureLineLength
                else:
                    NextNotePosition = measure.notes[idx + 1].position



                if NextNotePosition - notePosition == 0:
                    pass
                else:
                    diff = NextNotePosition - notePosition
                    ratio = float(diff) / measure.measureLineLength
                    # print ratio, 'ratio  ', note.fret, 'fret'
                    MeasureNoteTypeHelper(note, ratio, timeSig)
                pass




                # if in fact the note itself has 0, that means its part of the chord so make
                # the note before and after part of the chord




    def noteArrayMaker(tra_list, timeSig):
        isItRepeatTime = False
        measures = []  #  all the measures are gonna be stored here
        lengthOfMeasure = 0
        currentPos = 0
        measureObj = Measure()
        isitgrace = False

        for idx, vertLine in enumerate(tra_list):
            currentPos += 1
            lengthOfMeasure += 1

            #  this part handles if it is a repeated measure below
            if isItRepeatTime:
                isItRepeatTime = False
                lengthOfMeasure -= 1
            elif idx == len(tra_list) - 1:  # in case it is the very last character
                measureObj.measureLineLength = lengthOfMeasure
                measures.append(measureObj)
                pass
            elif tra_list[idx][0] == '|' and tra_list[idx + 1][0] == '|':
                lengthOfMeasure -= 1
                pass
            else:
                # main algo starts here before the for loop for measurement reset
                if tra_list[idx][1] == '|':
                    tempListOfNotes = []
                    currentPos = -1
                    measures.append(measureObj)
                    measureObj.measureLineLength = lengthOfMeasure
                    lengthOfMeasure = -1

                    measureObj = Measure()
            # main algo starts here
            # ntidx is whichever string it is
                for ntidx, char in enumerate(vertLine):
                    # IRRELEVANT TO THE MAIN ALGO, JUST REPEATS AND STUFF
                    if char == '*':  # this needs to happen at first, doesnt matter later
                        if tra_list[idx + 1][ntidx] == '|':
                            isItRepeatTime = True
                            measureObj.repeates = int(tra_list[idx + 1][0])

                    # this is parser number or pull offs
                    string = char
                    if isNum(char):
                        if isNum(tra_list[idx + 1][ntidx]):
                            string = char + tra_list[idx + 1][ntidx]
                        # print string
                            tra_list[idx + 1][ntidx] = '-'
                        tempNote = Note(noteFun(ntidx, string), whatOctave(ntidx, string))
                        tempNote.setString(ntidx)
                        tempNote.setFret(string)
                        tempNote.position = currentPos
                        
                        # == THESE ARE FOR PULL AND HAMMER ENDING ==
                        if tra_list[idx - 1][ntidx] == 'h':
                            tempNote.hstop = True
                        elif tra_list[idx - 1][ntidx] == 'p':
                            tempNote.pstop = True
                        # == END OF PULL AND HAMMER ENDS
                        tempListOfNotes.append(tempNote)
                        measureObj.notes = tempListOfNotes

                    # == THESE ARE FOR HAMMER AND PULL BEGINNING DETECTION ==
                    elif char == 'h':
                        for note in reversed(measureObj.notes):
                            if note.string == ntidx:
                                note.hstart = True
                                break
                    elif char == 'p':
                        for note in reversed(measureObj.notes):
                            if note.string == ntidx:
                                note.pstart = True
                                break
                    
                    # == ENDING FOR HAMMER AND PULL BEGINNING DETECTION ==
                    else:
                        pass
        MeasureTypeCalculator(timeSig, measures)


        measures.pop(0)  # stupid algo makes an empty measure so have to do this
        for meas in measures:
            meas.chordType()
            meas.doLastThing()
            meas.timeSig = timeSig
        return measures

 

    def changeMeasureTimeSig(measures, measureNumb, timeSig):
        measureToBeChanged = measures[measureNumb - 1]
        tempMeasureList = [measureToBeChanged]
        MeasureTypeCalculator(timeSig, measures)
        measureToBeChanged.changed = True

    def startProgram(arr):

        m = 1
        for meas in arr:
            repeat = False
            s = 1
            measure = ET.SubElement(part, "measure", number=str(m))  # place a measure
            if meas.repeates > 1:
                repeat = True
                barline = ET.SubElement(measure, "barline", location="left")
                ET.SubElement(barline, "bar-style").text = "heavy-light"
                ET.SubElement(barline, "repeat", direction="forward")
                direction = ET.SubElement(measure, "direction", placement="above")
                directiontype = ET.SubElement(direction, "direction-type")
                ET.SubElement(directiontype, "words").text = "Repeat " + str(meas.repeates) + " Times"
            if m == 1:
                attributes = ET.SubElement(measure, "attributes")
                divisions = ET.SubElement(attributes, "divisions").text = str(2)
                key = ET.SubElement(attributes, "key")
                fifths = ET.SubElement(key, "fifths").text = str(0)
                t = ET.SubElement(attributes, "time")
                # print meas.timeSig
                _beats = ET.SubElement(t, "beats").text = meas.timeSig[0]
                beats_type = ET.SubElement(t, "beats_type").text = meas.timeSig[2]
                clef = ET.SubElement(attributes, "clef")
                sign = ET.SubElement(clef, "sign").text = "TAB"
                line = ET.SubElement(clef, "line").text = str(5)
                staff_details = ET.SubElement(attributes, "staff-details")
                staff_lines = ET.SubElement(staff_details, "staff-lines").text = "6"
                for i in range(6):
                    staff_tuning_line = ET.SubElement(staff_details, "staff-tuning", line="{}".format((i + 1)))
                    tuning_step = ET.SubElement(staff_tuning_line, "tuning-step").text = numToString(i)
                    switcher = {  # default tuning mapping based of string.
                        0: "3",
                        1: "3",
                        2: "3",
                        3: "4",
                    }
                    tuning_octave = ET.SubElement(staff_tuning_line, "tuning-octave").text = switcher.get(i)
            m += 1
            for idx, noteObject in enumerate(meas.notes):


                note = ET.SubElement(measure, "note")
                # print noteObject.position, 'curr pos'
                # if noteObject.grace == True:
                    # ET.SubElement(note, "grace")
                if noteObject.position == meas.notes[idx - 1].position:
                    if len(meas.notes) != 1 and idx != 0:
                        chord = ET.SubElement(note, "chord")

                pitch = ET.SubElement(note, "pitch")
                step = ET.SubElement(pitch, "step").text = noteObject.letter
                if noteObject.alter != 'not_altered':
                    alter = ET.SubElement(pitch, "alter").text = noteObject.alter
                octave = ET.SubElement(pitch, "octave").text = noteObject.Octave
                ET.SubElement(note, "duration").text = noteObject.duration
                voice = ET.SubElement(note, "voice").text = noteObject.voice
                type = ET.SubElement(note, "type").text = noteObject.typeOfNote
                notations = ET.SubElement(note, "notations")
                technical = ET.SubElement(notations, "technical")


                if noteObject.hstop:
                    hammeroff = ET.SubElement(technical, "hammer-on", number=str(s), type="stop")
                if noteObject.pstop:
                    hammeroff = ET.SubElement(technical, "pull-off", number=str(s), type="stop")
                if noteObject.hstart:
                    hammeron = ET.SubElement(technical, "hammer-on", number=str(s), type="start").text = "H"
                if noteObject.pstart:
                    hammeron = ET.SubElement(technical, "pull-off", number=str(s), type="start").text = "P"


                string = ET.SubElement(technical, "string").text = str(int(noteObject.string) + 1)
                # print(noteObject.fret, 'fret is this one')
                fret = ET.SubElement(technical, "fret").text = str(noteObject.fret)

                if noteObject.slurAmount == 1 and (noteObject.hstart or noteObject.pstart):
                    slurstart = ET.SubElement(notations, "slur", number=str(s), placement="above", type="start")

                if noteObject.slurAmount == 1 and (noteObject.hstop or noteObject.pstop):
                    slurstop = ET.SubElement(notations, "slur", number=str(s), type="stop")
                    s += 1

            if repeat == True:
                barline = ET.SubElement(measure, "barline", location="right")
                ET.SubElement(barline, "bar-style").text = "light-heavy"
                ET.SubElement(barline, "repeat", direction="backward")
                






    startProgram(noteArrayMaker(transpose_list, timeSig))



    xmlstr = minidom.parseString(ET.tostring(score_partwise)).toprettyxml(indent="   ")

    tree.write(nameFile)

    with open(nameFile, "w") as f:
        f.write(xmlstr)
