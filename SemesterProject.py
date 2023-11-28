#imports
import Draw
import random
import math

#variables I will use and never modify:

#coordinates of the textbox where user guesses
guessboxX = 590 
guessboxY = 250
guessboxWidth = 400
guessboxHeight = 60

#coordinates of scoreboard
scoreboardX = 500
scoreboardY = 10
scoreboardWidth = 200
scoreboardHeight = 60

#coordinates of error messages
errorX = 540
errorY = 180

#enter button coords
enterX = 710
enterY = 360
enterWidth = 100
enterHeight = 60

#undo button coords
undoX = 930
undoY = 315
undoWidth = 50
undoHeight = 25

#new game coords
newgameX = 10
newgameY = 10
newgameWidth = 150
newgameHeight = 60

def drawBoard(): 
    #background and aesthetics and button locations etc. 
    yellow = Draw.color(248,205,14) #color I like
    
    Draw.setBackground(Draw.BLUE)
    
    #new game button
    Draw.setColor(yellow)
    Draw.filledRect(newgameX, newgameY, newgameWidth, newgameHeight) 
    Draw.setColor(Draw.WHITE)
    Draw.setFontSize(23)    
    Draw.string("New Game", 25, 27) #numbers are coordinates where i want it to show up
    
    #enter button
    Draw.setColor(yellow)
    Draw.filledRect(enterX, enterY, enterWidth, enterHeight)
    Draw.setColor(Draw.WHITE)
    Draw.setFontSize(25)
    Draw.string("ENTER!", 716, 375)   #numbers are coordinates where i want it to show up 
    
    #backspace button
    Draw.setColor(yellow)
    Draw.filledRect(undoX, undoY, undoWidth, undoHeight)
    Draw.setColor(Draw.WHITE)
    Draw.setFontSize(15)
    Draw.string("UNDO", 933, 320) #numbers are coordinates where i want it to show up
    
    #text box
    Draw.setColor(Draw.YELLOW)
    Draw.rect(guessboxX, guessboxY, guessboxWidth, guessboxHeight)   
        
    #scoreboard
    Draw.setColor(Draw.YELLOW)
    Draw.rect(scoreboardX, scoreboardY, scoreboardWidth, scoreboardHeight) 
    Draw.setColor(Draw.WHITE)
    Draw.setFontSize(30)    
    Draw.string("Score = ", 510, 20) #numbers are coordinates where i want it to show up
    
    #extra stuff:
    Draw.setFontFamily("Courier New")
    Draw.setColor(Draw.WHITE)
    Draw.setFontSize(50)
    Draw.setFontBold(True)
    Draw.string("Temira's Spelling     !", 180, 600) #numbers are coordinates where i want it to show up
    Draw.picture("spelling-bee-logo.gif", 695, 530)  #numbers are coordinates where i want it to show up

def loadDict():
    #create a dictionary from the file of words that are actually useful to me
    file = open("popular.txt") #open text file (this is based on the official scrabble dictionary)
    solutionWords = {} #build a dictionary of words
    for line in file: 
        line = line[:-1] #don't include the /n part
        if len(line) > 3 and "s" not in line: #remove all words that are less than 3 characters or have an S
            solutionWords[line.upper()] = 1 #put it into the dictionary
    file.close() #close text file! important to do!
    
    return solutionWords #return the dictionary of the solution words
    
def buildCandidates(x):
    #build a list of candidate words (ie words that we can base a board off of)
    candidates = [] 
    for word in x:
        seen = {} #monitor unique characters in the word
        for char in word:
            if char in seen:
                seen[char] += 1
            else:
                seen[char] = 1
        if len(seen) == 7: #if the word has exactly 7 unique characters
            candidates += [word] #it can be a word that is the basis for a board
            
    return candidates #return the list of 7 unique-character words

def allIn(word, gameword): 
    #this function determines if a word can count as a valid solution
    for letter in word:
        if letter in gameword:
            pass
        else: #if any character from the guess word is not in the longer word, it can't be a valid solution
            return False 
        
    return True

def getSolutions(gameword, dictionary):
    #create a list of solutions based on the specific candidate word being used
    solutions = [] 
    for word in dictionary:
        if allIn(word, gameword) == True:
            solutions += [word] #if it returns True from allIn then it must be a valid solution and will be added to the solution list
    
    return solutions #return the full list of solution words that are possible solutions to the candidate word
    
def mostPopular(g): 
    #function to find most frequently occuring letter in solution list to put it in the middle of the board
    popularity = {}
    #make dictionary
    for i in g:
        for k in i:
            if k in popularity:
                popularity[k] += 1
            else:
                popularity[k] = 1            
    
    bestLetter = ""
    bestData = 0
    #go through dictionary
    for j in popularity:
        #if a frequency is higher than best recorded frequency
        if popularity[j] > bestData:
            #replace it and update best recorded frequency
            bestLetter = j
            bestData = popularity[j]
    #return the most frequently ocurring letter to be the middle letter       
    return bestLetter

def fillLayout(candidate, popular): 
    #this function fills the layout given the candidate word and the most popular letters
    yellow = Draw.color(248,205,14)
    letters = []
    for i in candidate: #this makes a list of all the letters in the candidate word
        if i not in letters:
            if i != popular: #don't include the most popular letter becasue that will be in the middle already
                letters += i            

    random.shuffle(letters) #randomize the location of the letters
    
    #layout
    #these are the coordinates of the vertices of the polygons and the letters 
    #inside the polygons and the coordinates to print the letters
    layout = [
        [330,248,270,248,240,300,270,352,330,352,360,300, popular, 285, 275],
        [330,128,270,128,240,180,270,232,330,232,360,180, letters[0], 285, 155],
        [430,188,370,188,340,240,370,292,430,292,460,240, letters[1], 385, 215],
        [430,308,370,308,340,360,370,412,430,412,460,360, letters[2], 385, 335],
        [330,368,270,368,240,420,270,472,330,472,360,420, letters[3], 285, 395],
        [230,188,170,188,140,240,170,292,230,292,260,240, letters[4], 185, 335],
        [230,308,170,308,140,360,170,412,230,412,260,360, letters[5], 185, 215]
            ] 
    
    for row in range(len(layout)): #draw the polygons
        slice1 = layout[row][:12] #first 12 numbers in the layout list are coords of the 6 corner points of the polygons
        Draw.setColor(yellow)
        Draw.filledPolygon(slice1) #draws the ploygons
        slice1 = "" #resets the slice to do the next one        
            
    for i in range(len(layout)): #draw the letters at the correct coordinates
        slice2 = (layout[i][12:]) #remaining letters in the layout list are the letters to fill out and coordinates to put them in
        #make it a tuple bc need it to not be in a list but to preserve the types (string and int)
        a, b, c = slice2 #saves the 3 values I need
        Draw.setColor(Draw.BLACK)
        Draw.setFontFamily("Times New Roman")
        Draw.setFontSize(50)
        Draw.string(a, b, c) #draws the letter in the coordinates listed in the "layout" list
        slice2 = "" #resets the slice    
    
    return letters #return the letters so that we can determine which is where then updating the string of the user's guess

def coverGuess(): #this function helps get rid of redundancy (because we hate redundancy)
    #this covers up the last guess when they update their guess or submit it by pressing enter
    Draw.setColor(Draw.BLUE) 
    Draw.filledRect(guessboxX, guessboxY, guessboxWidth, guessboxHeight) 
    Draw.setColor(Draw.YELLOW)
    Draw.rect(guessboxX, guessboxY, guessboxWidth, guessboxHeight)    

def letter(currentGuess): #also a frequently utilized function that needs to exist or else redundancy
    #this types an updated new guess whenever they click a letter button or undo
    coverGuess() #call the coverGuess function to clear the old guess and make room for updated guess
    Draw.setColor(Draw.WHITE)
    Draw.setFontSize(20)
    Draw.string(currentGuess, 605, 260) #this is within the textbox coordinates    

def cover():
    #this function covers up the previous error message
    Draw.setColor(Draw.BLUE) 
    Draw.filledRect(530, 170, 500, 50) #necessary location to cover the error message    

def preError():
    #this function covers up the last error message and prepares to write a new error message
    cover() 
    Draw.setColor(Draw.WHITE)
    Draw.setFontSize(30) 

def playGame(can, sol, pop):
    Draw.clear()
    drawBoard()
    
    li = fillLayout(can, pop) #fill the layout using the random word and the most popular letter in that word
    
    wordsUsed = {} #initialize a dictionary of words they guessed correctly
    currentGuess = "" #initialize a string of their current guess (until they press enter)
    score = 0 #initalize a score of zero with each new game
    while True: #repeat always 
        
        if getClick() == True: #if the user clicks
            ans = yesClick() #uses coordinates of click to determine which button is clicked
            if ans == "centerLetter" and len(currentGuess) <= 19: #dont want the word to be longer than 19 and go off the edge
                currentGuess += pop
                letter(currentGuess)                
            elif ans == "top" and len(currentGuess) <= 19: #these buttons update the guess with the letter clicked on by user
                currentGuess += li[0]
                letter(currentGuess)
            elif ans == "topRight" and len(currentGuess) <= 19:
                currentGuess += li[1]
                letter(currentGuess)
            elif ans == "bottomRight" and len(currentGuess) <= 19:
                currentGuess += li[2]
                letter(currentGuess)
            elif ans == "bottom" and len(currentGuess) <= 19:
                currentGuess += li[3]
                letter(currentGuess)
            elif ans == "bottomLeft" and len(currentGuess) <= 19:
                currentGuess += li[4]
                letter(currentGuess)
            elif ans == "topLeft" and len(currentGuess) <= 19:
                currentGuess += li[5]
                letter(currentGuess)                           
            elif ans == "New Game":  
                return #start a new game!!
            elif ans == "undo" and len(currentGuess) >= 0: #this removes the last letter from the guess
                currentGuess = currentGuess[:-1]
                letter(currentGuess)
            elif ans == "enter": #if they press enter
                if currentGuess in wordsUsed: #if it isnt a valid word, give it the correct error message
                    preError()                    
                    Draw.string("You already got that one!", errorX, errorY)
                elif pop not in currentGuess:
                    preError()                    
                    Draw.string("You must include the letter " + str(pop), 
                                errorX, errorY) 
                elif len(str(currentGuess)) <= 3:
                    preError()                    
                    Draw.string("Guess must be longer than 3 letters!", 
                                errorX, errorY)   
                elif currentGuess not in sol:
                    preError()                   
                    Draw.string("Not a valid word, try again!", errorX, errorY)                    
                elif pop in currentGuess and currentGuess in sol and \
                     currentGuess not in wordsUsed: #if it is a valid word
                    if li[0] not in currentGuess: #ie it doesn't use every single letter (not a "pangram")
                        cover()
                        score += len(str(currentGuess)) #update the score                        
                    elif li[1] not in currentGuess:
                        cover()
                        score += len(str(currentGuess)) #update the score                        
                    elif li[2] not in currentGuess:
                        cover()
                        score += len(str(currentGuess)) #update the score                        
                    elif li[3] not in currentGuess:
                        cover()
                        score += len(str(currentGuess)) #update the score                        
                    elif li[4] not in currentGuess:
                        cover()
                        score += len(str(currentGuess)) #update the score                        
                    elif li[5] not in currentGuess:
                        cover()
                        score += len(str(currentGuess)) #update the score
                    else: #it uses every single letter at least once and is therefore a "pangram"
                        score += 50
                        preError()
                        Draw.string("Pangram Bonus!", errorX, errorY)
                        
                    wordsUsed[currentGuess] = 1 #add this word to the wordsUsed dictionary so words can't be reused
                                            
                currentGuess = "" #reset the guess string
                coverGuess()                
                Draw.setColor(Draw.BLUE)
                Draw.filledRect(scoreboardX, scoreboardY, scoreboardWidth, scoreboardHeight)            
                Draw.setColor(Draw.YELLOW)
                Draw.rect(scoreboardX, scoreboardY, scoreboardWidth, scoreboardHeight) #cover the old scoreboard and replace with the new one
                Draw.setColor(Draw.WHITE)
                Draw.setFontSize(30)
                Draw.string("Score = " + str(score), 510, 20) #show the updated score
            elif ans == "secretGame": #if they press the secret button, do the secret game
                secretGame()            
                
    Draw.show()

def getClick(): #determines if the user clicks
    if Draw.mousePressed():
        return True
        
def yesClick():
    #determine what they clicked and return it to the playGame function
    x = Draw.mouseX() #get the coordinates of the user's click
    y = Draw.mouseY()    
    
    radius = 60
    #this is the radius of the inscribed circles to the polygons that are acting as buttons
    
    #center letter
    #if the click is within a distance of 60 (the radius) from the center point (ie they click within the polygon)
    if math.sqrt((x - 300)**2 + (y - 300)**2) <= radius: #300 is the x coord and 300 is the y coord of the center of the polygon
        return "centerLetter"  
    
    #if they click within the new game button:
    if x > newgameX and x < (newgameX+newgameWidth) and y > newgameY and y < (newgameY+newgameHeight): #these are the bounds of the new game button
        return "New Game"
    #if they click the undo button:
    if x > undoX and x < (undoX+undoWidth) and y > undoY and y < (undoY+undoHeight): #these are the bounds of the undo button
        return "undo"
    #if they click within the bounds of the enter button:
    if x > enterX and x < (enterX+enterWidth) and y > enterY and y < (enterY+enterHeight): #these are the bounds of the enter button
        return "enter"
    
    #if they click a letter that isnt the center letter:
    #use distance formula to determine if they are within the shape
    if math.sqrt((x - 300)**2 + (y - 180)**2) <= radius: #the numbers here correspond to the center point of the polygon
        return "top" #300 is the x coord and 180 is the y coord
    
    if math.sqrt((x - 400)**2 + (y - 240)**2) <= radius: #the numbers here correspond to the center point of the polygon
        return "topRight" #400 is the x coord and 240 is the y coord
    
    if math.sqrt((x - 400)**2 + (y - 360)**2) <= radius: #the numbers here correspond to the center point of the polygon
        return "bottomRight" #400 is the x coord and 360 is the y coord
    
    if math.sqrt((x - 300)**2 + (y - 420)**2) <= radius: #the numbers here correspond to the center point of the polygon
        return "bottom" #300 is the x coord and 420 is the y coord
    
    if math.sqrt((x - 200)**2 + (y - 360)**2) <= radius: #the numbers here correspond to the center point of the polygon
        return "bottomLeft" #200 is the x coord and 360 is the y coord
    
    if math.sqrt((x - 200)**2 + (y - 240)**2) <= radius: #the numbers here correspond to the center point of the polygon
        return "topLeft" #200 is the x coord and 240 is the y coord
    
    if x > 1080 and x < 1100 and y > 0 and y < 20: #easter egg hidden button! numbers = location of hidden button
        return "secretGame" #these are the bounds of the secret button
   
def secretGame(): #Bonus! Easter egg!!!
    #secret game function causes the secret game to appear and calls the functions to make it work!
    
    Draw.clear() #clear to set up for new game!
    while True:
        #wait for the user to type in a number and press enter
        Draw.setBackground(Draw.YELLOW)
        Draw.setColor(Draw.BLUE)
        Draw.setFontSize(40)
        Draw.setFontBold(True)
        Draw.string("Secret Feature! Hack the NYT Spelling Bee!", 60, 80) #numbers are coordinates where i want it to show up
        Draw.setFontSize(20)
        Draw.string("Type the middle letter:", 70, 140) #numbers are coordinates where i want it to show up
        Draw.setFontSize(10)
        Draw.string("(then press enter)", 70, 170) #numbers are coordinates where i want it to show up
        mid = getTextString(275, 140, 15, 25, 20, 1) #this gets the middle letter of the puzzle
        Draw.string("Type the other 6 letters:", 70, 180)
        Draw.setFontSize(10) #dont need to reset the font size cuz it gets reset within the getTextString function
        Draw.string("(then press enter)", 70, 210)        
        around = getTextString(280, 180, 70, 25, 20, 6) #this gets the other letters in the puzzle
        #Display the number elsewhere on the canvas
        Draw.clear()
        answer = formList(mid, around) #this forms an answer list based on what the user inputs as the puzzle
        newlines(answer) #this prints the list of answers to the display
        Draw.show()

def getTextString(x, y, wide, high, fontSize, maxChars): 
    #not my code, this was given to me by Professor Broder and used with his permission
    ans = ""
    
    # Draw the rectangle where the user will type in the number
    Draw.setColor(Draw.WHITE)            
    Draw.filledRect(x, y, wide, high)
    Draw.show()
    
    done = False
    while not done:  # while the user hasn't pressed enter
        if Draw.hasNextKeyTyped():
            # get the next key, and process it accordingly
            newKey = Draw.nextKeyTyped()
            if newKey == "Return":  # return means they're done
                done = True
            elif newKey == "BackSpace": # backspace allows them to undo
                if len(ans) > 0:
                    ans = ans[0:len(ans)-1]
            elif len(ans) < maxChars:
                if newKey.lower() in "abcdefghijklmnopqrstuvwxyz":
                    ans += newKey
                
            Draw.setFontSize(fontSize) # redraw the rectangle with 
            Draw.setColor(Draw.WHITE) # the current number.          
            Draw.filledRect(x, y, wide, high)
            Draw.setColor(Draw.BLUE)
            Draw.string(ans, x, y)
        Draw.show()
    
    return ans

def formList(center, around): 
    #forms a list of words based on what the user inputted in the text boxes
    yes = []
    center = center.upper() #put it all in uppercase so if they input lowercase it will still work
    around = around.upper()
    gameWord = center+around
    almost = (getSolutions(gameWord, loadDict())) #plug into the function that gets possible words that can be made from it
    for i in almost:
        if center in i: #ensure that all solutions include the center letter
            yes += [i]
        else:
            pass #otherwise, don't include it as a solution
    
    return yes #return the list of words that can be made that must include the middle letter

def newlines(li):
    WPL = 10 #=words per line
    #invented this function so only 10 words would appear on a line so it doesnt go off the edge
    Draw.string("Solution words:", 20, 250)
    if len(li) <= WPL: #print on one line if there are only 10 answers
        Draw.string(li, 20, 300)
    else:
        for i in range(len(li)//WPL): #if exactly divisibly by 10 then print on however many lines it takes
            Draw.string(li[(i*WPL):((i+1)*WPL)], 20, 300+(i*50)) #space of 50 between each line of answers
        if len(li)%WPL != 0: #print the leftover words if it doesnt divide perfectly
            Draw.string(li[-(len(li)%WPL):], 20, 300+((len(li)//WPL)*50)) 
    
def main():
    #set the canvas and call the functions in the right order to make it work
    Draw.setCanvasSize(1100, 750) #size of my game
    
    while True:
        #print(len(buildCandidates(loadDict()))) #how many possible games there are (2426 possible games)
        word = buildCandidates(loadDict()) #this builds the list of "pangrams"
        gameWord = random.choice(word) #randomizes to ensure random game board each time
        #print(gameWord) #what candidate word was selected
        listy = getSolutions(gameWord, loadDict()) #gets all the actual solutions given the word we are using
        playGame(gameWord, listy, mostPopular(listy)) #play the game! 
        #the input is the selected candidate word, the list of words that can be made from that candidate word, and the most frequently occuring letter in that list

main()
