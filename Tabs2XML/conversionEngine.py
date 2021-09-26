import xml.etree.cElementTree as ET
import lxml.etree as etree
import numpy as np
from xml.dom import minidom
from itertools import cycle


    # =======CLASSES TO USE LATER=============
def xmlConverter(someFile, nameFile, timeSig):
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


        def __init__(self, letter, Octave):
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




    def whatOctave(string, fret):
        tempoctave = 0

        if string == 5:
            if fret <= 7:  # indexed E = 0 and b = 7 for me -alp: kalin e teli bu
                tempoctave = 2
            else:
                tempoctave = 3
        elif string == 4:  # A
            if fret <= 3:
                tempoctave = 2
            else:
                tempoctave = 3
        elif string == 3:  # D
            if fret <= 9:
                tempoctave = 3
            else:
                tempoctave = 4
        elif string == 2:
            if fret <= 4:
                tempoctave = 3
            else:
                tempoctave = 4
        elif string == 1:
            if fret == 0:
                tempoctave = 3
            elif fret <= 12:
                tempoctave = 4
            else:
                tempoctave = 5
        elif string == 0:
            if fret <= 7:
                tempoctave = 4
            else:
                tempoctave = 5
        else:
            print("String input might be wrong")
        # print string, 'string whattt'
        # print fret, 'fret'

        # print(tempoctave)
        return str(tempoctave)

    # function for type calculation and selection gonna do something later
    def totalTime(timeSelection):
        if timeSelection == '4/4':
            return 4
        elif timeSelection == '3/4':
            return 3

    # ======== GONNA CHANGE IT LATER
    def noteTypeHelper(note, whatType):
        typeOfNotes = ["16th", "eighth", "quarter", "half", "whole"]

        if whatType <= 0.3:
            note.setTypeOfNote(typeOfNotes[0])
            note.setDuration("0.5")# 1th
        elif whatType <= 0.6:
            note.setTypeOfNote(typeOfNotes[1])  # eight
            note.setDuration(1)
        elif whatType <= 1.3:
            note.setTypeOfNote(typeOfNotes[2])  # quarter
            note.setDuration(2)
        elif whatType <= 2.3:
            note.setTypeOfNote(typeOfNotes[3])  # half
            note.setDuration(4)
        elif whatType <= 4:
            note.setTypeOfNote(typeOfNotes[4])  # whole
            note.setDuration(8)



    def noteTypeCalculator(arrOfNotes, lengthOfBar, timesignature):
        # trying something out here with the length
        tempLength = lengthOfBar - 1
        totalQuarterNoteTime = totalTime("4/4")
        #  Arjit can u link this up to the time signature selection.
        # it should be as follows
        # totalQuarterNoteTime = totalTime(timesignature)

        for j in range(0, len(arrOfNotes)):
            # it takes 4 quarter notes to play

            if arrOfNotes[j] != 'measure':
                notePosition = arrOfNotes[j][1]
                note = arrOfNotes[j][0]
                if note.grace:
                    pass
                else:
                    nextNotePosition = -1

                    if j != len(arrOfNotes) - 2:
                        if arrOfNotes[j + 1] == 'measure':
                            nextNotePosition = arrOfNotes[j + 2][1]
                        else:
                            nextNotePosition = arrOfNotes[j + 1][1]

                        if nextNotePosition <= notePosition:
                            nextNotePosition = lengthOfBar

                # if there are no notes until the next | which resets the numbers
                    else:
                        nextNotePosition = lengthOfBar
                # variables are set for comparison
                # print nextNotePosition, 'next note'
                # print notePosition, 'not position 2'
                    difference = (nextNotePosition - notePosition)
                    how_much_ratio = float(difference) / tempLength
                    whatType = how_much_ratio * totalQuarterNoteTime
                    if len(arrOfNotes[j]) > 2:
                    # later idea below
                    # for i in range(0, len(arrOfNotes[j]) - 1, 2):
                    # min = whatType
                        for i in range(0, len(arrOfNotes[j]),
                                2):  # need to increment by 2 for chords because i am sleepy and i fucked up
                            noteTypeHelper(arrOfNotes[j][i], whatType)
                    else:
                        noteTypeHelper(note, whatType)


    text=someFile.split()
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
        enote = ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"]

        enote = ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"]

        switcher = {  # default tuning mapping based of string.
            0: ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"],
            1: ["B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
            2: ["G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"],
            3: ["D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D"],
            4: ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A"],
            5: ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"],
        }


        return switcher.get(_string)[fret]


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

    part_name = ET.SubElement(score_part, "part-name").text = "Classical Guitar"  # input part name here from user

    part = ET.SubElement(score_partwise, "part", id="P1")

    tree = ET.ElementTree(score_partwise)


    # place notes

    def makeNote(letter, octave):
        return Note(letter, octave)


    def isAlter(alterednote):
        arrOfAlter = ['F#', 'G#', 'A#', 'C#', 'D#']
        arrOfNonAlter = ['F', 'G', 'A', 'C', 'D']
        if alterednote in arrOfAlter:
            return arrOfNonAlter[arrOfAlter.index(alterednote)]
        else:
            return False

    # function that takes one line until the '|' and sets everything for that line only, call a for loop later
    def isLetter(string):
        if string == '-':
            return False
        else:
            return True

    def noteArrayMaker(tra_list):
        notesAndChords = []
        position = -1
        length = 0
        barNumber = -1
        for idx, vertLine in enumerate(tra_list):
            if idx == len(tra_list) - 1:
                notesAndChords.append('measure')
                barNumber += 1
            else:
                if vertLine[1] != '|':
                    position += 1
                    length += 1
                else:
                    barNumber += 1
                    position = -1
                    notesAndChords.append('measure')
                tempList = []

                # the list of chars are tralist [[][][][][]]
                for i in range(0, len(vertLine)):
                    isItLetters = False
                    isGrace = False
                    string = vertLine[i]
                    backString = tra_list[idx - 1][i]
                    if isNum(string):
                        nextString = tra_list[idx + 1][i]
                        nextNextString = tra_list[idx + 2][i]

                        if isNum(backString):
                            pass
                        else:
                            if isLetter(backString):
                                if backString == 'g':
                                    isGrace = True

                            if isNum(nextString):
                                string = string + nextString

                            if not isAlter(noteFun(i, int(string))):
                                tempNote = makeNote(noteFun(i, int(string)), whatOctave(i, int(string)))
                            # print tempNote.letter
                                tempNote.setString(i)
                                tempNote.setFret(string)
                                tempList.append(tempNote)
                                if isGrace:
                                    tempNote.grace = True
                            else:
                                # makes a note with the parameter type (the letter) and the octave of that note which are set
                                tempNote = makeNote(isAlter(noteFun(i, int(string))), whatOctave(i, int(string)))
                                tempNote.setAlter()
                                tempNote.setString(i)
                                tempNote.setFret(int(string))
                                tempList.append(tempNote)
                                if isGrace:
                                    tempNote.grace = True
                            tempList.append(position)


                if len(tempList) >= 1:
                    notesAndChords.append(tempList)
            # end of first for loop
        # after all the notes are done the second for loop


        noteTypeCalculator(notesAndChords, length / barNumber, "4/4")
        return notesAndChords


    def startProgram(arr):

        m = 1
        chordPresent = False
        for idx, lists in enumerate(noteArrayMaker(arr)):
            if lists == 'measure':
                if idx != len(noteArrayMaker(arr)) - 1:
                    measure = ET.SubElement(part, "measure", number=str(m))  # place a measure
                if m == 1:
                    attributes = ET.SubElement(measure, "attributes")
                    divisions = ET.SubElement(attributes, "divisions").text = str(2)
                    key = ET.SubElement(attributes, "key")
                    fifths = ET.SubElement(key, "fifths").text = str(0)
                    t = ET.SubElement(attributes, "time")
                    if timeSig[0] == "1/4":
                        _beats = ET.SubElement(t, "beats").text = str(1)
                        beats_type = ET.SubElement(t, "beats_type").text = str(4)
                    elif timeSig[0] == "2/4":
                        _beats = ET.SubElement(t, "beats").text = str(2)
                        beats_type = ET.SubElement(t, "beats_type").text = str(4)
                    elif timeSig[0] == "3/4":
                        _beats = ET.SubElement(t, "beats").text = str(3)
                        beats_type = ET.SubElement(t, "beats_type").text = str(4)
                    elif timeSig[0] == "4/4":
                        _beats = ET.SubElement(t, "beats").text = str(4)
                        beats_type = ET.SubElement(t, "beats_type").text = str(4)
                    
                    clef = ET.SubElement(attributes, "clef")
                    sign = ET.SubElement(clef, "sign").text = "TAB"
                    line = ET.SubElement(clef, "line").text = str(5)
                    staff_details = ET.SubElement(attributes, "staff-details")
                    staff_lines = ET.SubElement(staff_details, "staff-lines").text = "6"
                    for i in range(6):
                        staff_tuning_line = ET.SubElement(staff_details, "staff-tuning", line="{}".format((i + 1)))
                        tuning_step = ET.SubElement(staff_tuning_line, "tuning-step").text = numToString(i)
                        switcher = {  # default tuning mapping based of string.
                            0: "2",
                            1: "2",
                            2: "3",
                            3: "3",
                            4: "3",
                            5: "4",
                        }
                        tuning_octave = ET.SubElement(staff_tuning_line, "tuning-octave").text = switcher.get(i)
                m += 1
            else:
                if len(lists) > 2:
                    for i in range(0, len(lists), 2):
                        # note definition for chords
                        noteObject = lists[i]
                        note = ET.SubElement(measure, "note")

                        # trying the chord thing out
                        if not chordPresent:
                            chordPresent = True
                        else:
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
                        string = ET.SubElement(technical, "string").text = str(int(noteObject.string) + 1)
                        fret = ET.SubElement(technical, "fret").text = str(noteObject.fret)
                else:
                    chordPresent = False
                    noteObject = lists[0]
                    note = ET.SubElement(measure, "note")
                    if noteObject.grace:
                        ET.SubElement(note, "grace")
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
                    string = ET.SubElement(technical, "string").text = str(int(noteObject.string) + 1)
                    fret = ET.SubElement(technical, "fret").text = noteObject.fret






    # methods for object to xml
    # for note in range(0, len(noteArrayMaker(transpose_list)[0]) - 1, 2):
        # print noteArrayMaker(transpose_list)[0][note].getType()
    startProgram(transpose_list)























    xmlstr = minidom.parseString(ET.tostring(score_partwise)).toprettyxml(indent="   ")

    
    tree.write(nameFile)

    with open(nameFile, "w") as f:
        f.write(xmlstr)