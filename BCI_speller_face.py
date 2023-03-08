# --- Import packages ---
import psychopy
psychopyVersion = '2022.2.3'
psychopy.useVersion(psychopyVersion)
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, parallel
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import psychopy.iohub as io
from psychopy.hardware import keyboard

import numpy as np  # whole numpy lib is available, prepend 'np.'
#from numpy import (sin, cos, tan, log, log10, pi, average,
#                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import pandas as pd
import os  # handy system and path functions
import sys  # to get file system encoding
from glob import glob
from pathlib import Path

###############################################################################
testMode = True #'timingTest'  # options are True, False, or 'timingTest' (note the last has to be in quotes, but True and False should not be)
triggerMode = None  # options are parallel, usb, None

colourTheme = 'dark'
frameRate = 144  # should read this from the computer itself, but may not be reliable w multiple monitors

expName = 'BCI_speller'  # from the Builder filename that created this script
conditionList = 'levels_conditions.csv'
targetList = 'levels_targets.csv'
targetIdWidth = 120
targetIdHeight = 120
targetIdLineWidth = 20
targetIdOutline = '#FFD400'
targetIdFill = None
targetIdOpacity = 1.0
rowColHighlightStimList = 'levels_row_col.csv'
instructionImage = 'images/instructions.png'
breakInstr1Image = 'images/break_instructions_1.png'
breakInstr2Image = 'images/break_instructions_2.png'
endImage = 'images/all_finished.png'


if colourTheme == 'dark':
    matrixFile = 'images/letter_grid_6x6_darkmode.png'
    screenColour = [-1, -1, -1]
    textColour = [1, 1, 1]
else: #colourTheme == light
    matrixFile = 'images/letter_grid_6x6_lightmode.png'
    screenColour = [1.0, 1.0, 1.0]
    textColour = [0, 0, 0]

if testMode == True:
    targetsPerCond = 1
    highlightDuration = 1.5
    trialDuration = 0.150
    rowColHighlightDuration = 0.125
    rowColHighlightOnsetTime = 0.025 # delay between start of trial (draw matrix) and onset of rowColHighlight
    minBreakDurn = 5.0
    displayScreen = 1
    fullScreen = False
    mouseVis = True
elif testMode == 'timingTest':
    targetsPerCond = 15
    highlightDuration = 0.010
    trialDuration = 0.300
    rowColHighlightDuration = 0.200
    rowColHighlightOnsetTime = 0.100 # delay between start of trial (draw matrix) and onset of rowColHighlight
    displayScreen = 2
    fullScreen = True
    mouseVis = False
    rowColHighlightStimList = 'levels_row_col_timingTest.csv'
    conditionList = 'levels_conditions_timingTest.csv'
    matrixFile = 'images/letter_grid_6x6_timingTest.png'
else:
    targetsPerCond = 5
    highlightDuration = 3.0
    trialDuration = 0.500
    rowColHighlightDuration = 0.400
    rowColHighlightOnsetTime = 0.100 # delay between start of trial (draw matrix) and onset of rowColHighlight
    minBreakDurn = 60.0
    displayScreen = 2
    fullScreen = True
    mouseVis = False

#############################
# Initialize parallel port
# data is the value of the TTL trigger code you want to send
# here we initialize the port to 0, just in case
triggerCode = 0

if triggerMode == 'parallel':
    p_port = parallel.ParallelPort(address='0x4FF8')
    p_port.setData(triggerCode)
elif triggerMode == 'usb':
    import UniversalLibrary as UL
    board = 0
    port = UL.FIRSTPORTA
    direction = UL.DIGITALOUT
    UL.cbDConfigPort(board, port, direction)
    UL.cbDOut(board, port, triggerCode)
    
endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Store info about the experiment session
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
}

#####################################
# --- Show participant info dialog --
if testMode == False:
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
         
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

###########################
# Logging
#  Ensure that relative paths start from the same directory as this script
_thisDir = Path('./') # os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

logFileStem = str(_thisDir) + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
thisExp = data.ExperimentHandler(name=expName, version='',
                                extraInfo=expInfo, 
                                runtimeInfo=None,
                                # originPath='C:\\Users\\BCI\\Desktop\\Julias_honors\\stimuli\\BCI_speller_julia.py',
                                savePickle=False, 
                                saveWideText=True,
                                dataFileName=logFileStem)
# save a log file for detail verbose info
logFile = logging.LogFile(logFileStem + '.log', level=logging.EXP)


##########################
# --- Setup the Window ---
win = visual.Window(
    size=[1920, 1080], fullscr=fullScreen, 
    screen=displayScreen, 
    waitBlanking=True,
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=screenColour, colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='pix')
    
win.mouseVisible = mouseVis

# store frame rate of monitor if we can measure it
get_fr = win.getActualFrameRate()
if get_fr != None:
    frameRate = get_fr

frameDur = 1.0 / frameRate
expInfo['frameRate'] = frameRate

#############################
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

key_resp = keyboard.Keyboard()

# used below to check for empty responses
def checkEmpty(text):
    if text == " " or text == "":
        return True
    else:
        return False





###########################################################
# Initialize components for various routines

# --- Initialize components for Routine "instructions" ---
instructionScreen = visual.ImageStim(name='instructionScreen', 
                                    win=win,
                                    image=instructionImage, mask=None, anchor='center',
                                    ori=0.0, pos=(0, 0), size=(1280, 720),
                                    colorSpace='rgb', opacity=1.0,
                                    flipHoriz=False, flipVert=False,
                                    texRes=128.0, interpolate=True)

# Initialize spellerMatrix
spellerMatrix = visual.ImageStim(name='spellerMatrix', 
                                win=win,
                                image=matrixFile, 
                                mask=None, anchor='center',
                                pos=(0, 0), size=None,
                                colorSpace='rgb', 
                                opacity=1.0,
                                interpolate=False)

# --- Initialize components for target identification ---
targetIdentification = visual.ShapeStim(name='targetIdentification',
                                        vertices='circle',
                                        win=win, 
                                        size=(targetIdWidth, targetIdHeight), 
                                        pos=[0,0], anchor='center',
                                        lineWidth=targetIdLineWidth, 
                                        colorSpace='rgb',  
                                        lineColor=targetIdOutline, 
                                        fillColor=None, 
                                        opacity=targetIdOpacity, 
                                        interpolate=False)
# targetIdentification = visual.Rect(name='targetIdentification',
#                                         width=targetIdWidth, height=targetIdHeight,
#                                         win=win, 
#                                         pos=[0,0], anchor='center',
#                                         lineWidth=targetIdLineWidth, 
#                                         colorSpace='rgb',  
#                                         lineColor=targetIdOutline, 
#                                         fillColor=None, 
#                                         opacity=targetIdOpacity, 
#                                         interpolate=True)

# --- Initialize components for Routine "trial" ---
rowColHighlight = visual.ImageStim(name='rowColHighlight', 
                                    win=win,
                                    image='sin', mask=None, 
                                    ori=0.0, size=None,
                                    color=screenColour, colorSpace='rgb', opacity=1.0,
                                    flipHoriz=False, flipVert=False,
                                    texRes=128.0, interpolate=True, depth=-2.0)

# --- Initialize components for Routine "Counting" ---
askCount = visual.TextStim(name='askCount',
                            win=win, 
                            text='Please enter the number of times you counted the target letter highlighted. \nPress Enter once you have entered the number.',
                            font='Open Sans',
                            pos=(0, 100), height=30.0, wrapWidth=1080.0, ori=0.0, 
                            color=textColour, colorSpace='rgb', opacity=1.0, 
                            languageStyle='LTR',
                            depth=0.0);

countingPrompt = visual.TextBox2(win, name='countingPrompt',
                                text=None, font='Open Sans',
                                pos=(0, -100),     letterHeight=30.0,
                                size=(None, None), borderWidth=2.0,
                                color=textColour, colorSpace='rgb',
                                opacity=1.0,
                                bold=False, italic=False,
                                lineSpacing=1.0,
                                padding=0.0, alignment='center',
                                anchor='center',
                                fillColor=None, borderColor=None,
                                flipHoriz=False, flipVert=False, languageStyle='LTR',
                                editable=True,
                                autoLog=True,
                            )


# --- Initialize components for Routine "btwCondBreak" ---
breakInstr1 = visual.ImageStim(name='breakInstr1', 
                                win=win,
                                image=breakInstr1Image, mask=None, anchor='center',
                                ori=0.0, pos=(0, 0), size=(1280, 720),
                                colorSpace='rgb', opacity=1.0,
                                flipHoriz=False, flipVert=False,
                                texRes=128.0, interpolate=True
                                )

breakInstr2 = visual.ImageStim(name='breakInstr2', 
                                win=win,
                                image=breakInstr2Image, mask=None, anchor='center',
                                ori=0.0, pos=(0, 0), size=(1280, 720),
                                colorSpace='rgb', opacity=1.0,
                                flipHoriz=False, flipVert=False,
                                texRes=128.0, interpolate=True, depth=-2.0
                                )

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

########################
### START EXPERIMENT ###
########################

# --- Instructions ---
if testMode == False:
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # keep track of which components have finished
    instructionsComponents = [key_resp, instructionScreen]
    for thisComponent in instructionsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "instructions" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *instructionScreen* updates
        if instructionScreen.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructionScreen.frameNStart = frameN  # exact frame index
            instructionScreen.tStart = t  # local t and not account for scr refresh
            instructionScreen.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructionScreen, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instructionScreen.started')
            instructionScreen.setAutoDraw(True)
            
        # *key_resp* updates
        waitOnFlip = False
        
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.started')
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['space', 'enter'], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        
        for thisComponent in instructionsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    ## --- Ending Routine "instructions" ---
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    thisExp.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
    thisExp.nextEntry()
    # the Routine "instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()


#############
# Main loop #
#############

conditions = data.TrialHandler(nReps=1.0, method='random', 
                                extraInfo=expInfo, originPath=-1,
                                trialList=data.importConditions(conditionList),
                                seed=None, name='conditions')

thisExp.addLoop(conditions)  # add the loop to the experiment

for thisCondition in conditions:
    # currentLoop = conditions
    # send condition code to EEG amp
    if triggerMode == 'parallel':
        p_port.setData(int(thisCondition['conditionCode']))
    elif triggerMode == 'usb':    
        UL.cbDOut(board, port, int(thisCondition['conditionCode']))


    # preload images for this condition
    imgList = {}
    for imgFile in glob('images/' + thisCondition['highlightType'] + '/*.png'):
        imgName = imgFile.split('\\')[-1][:-4]
        imgList[imgName] = visual.ImageStim(win=win,
                                            image=imgFile,
                                            ori=0.0, 
                                            # pos=trial['img_pos'], 
                                            interpolate=True, 
                                            )    
        
        
    # randomize characters in matrix
    # we will not loop through all 36 positions though; targetCount below tracks and limits to 
    targets = data.TrialHandler(nReps=1.0, method='random', 
                                extraInfo=expInfo, originPath=-1,
                                trialList=data.importConditions(targetList),
                                seed=None, name='target')
    
    thisExp.addLoop(targets)  # add the loop to the experiment
    
    targetCount = 0
    for thisTarget in targets:
        
        # --- Prepare to start Routine "Highlight" ---
        continueRoutine = True
        routineForceEnded = False

        # update component parameters for each repeat
        targetIdentification.setPos(eval(thisTarget['matrixPosition']))
                    
        # keep track of which components have finished
        HighlightComponents = [spellerMatrix, targetIdentification]
        for thisComponent in HighlightComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "targetIdentification" ---
        while continueRoutine and routineTimer.getTime() < highlightDuration:
            if triggerMode == 'parallel':
                p_port.setData(0)
            elif triggerMode == 'usb':    
                UL.cbDOut(board, port, 0)
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *spellerMatrix* updates
            if spellerMatrix.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                spellerMatrix.frameNStart = frameN  # exact frame index
                spellerMatrix.tStart = t  # local t and not account for scr refresh
                spellerMatrix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(spellerMatrix, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'spellerMatrix.started')
                spellerMatrix.setAutoDraw(True)
                
            if spellerMatrix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > spellerMatrix.tStartRefresh + highlightDuration - frameTolerance:
                    # keep track of stop time/frame for later
                    spellerMatrix.tStop = t  # not accounting for scr refresh
                    spellerMatrix.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'spellerMatrix.stopped')
                    spellerMatrix.setAutoDraw(False)
            
            # *targetIdentification* updates
            if targetIdentification.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                targetIdentification.frameNStart = frameN  # exact frame index
                targetIdentification.tStart = t  # local t and not account for scr refresh
                targetIdentification.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(targetIdentification, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'targetIdentification.started')
                targetIdentification.setAutoDraw(True)
                
                # Send trigger code indicationg target location
                if triggerMode == 'parallel':
                    p_port.setData(thisTarget['targetCode'])
                elif triggerMode == 'usb':    
                    UL.cbDOut(board, port, int(thisCondition['targetCode']))

            if targetIdentification.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > targetIdentification.tStartRefresh + highlightDuration - frameTolerance:
                    # keep track of stop time/frame for later
                    targetIdentification.tStop = t  # not accounting for scr refresh
                    targetIdentification.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetIdentification.stopped')
                    targetIdentification.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in HighlightComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "targetIdentification" ---
        for thisComponent in HighlightComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(0 - highlightDuration)
        
        
        #################################################################
        # Start a block of row & columns highlights
        
        # cross row & column positions with highlight images
        rowColPositions = pd.read_csv(rowColHighlightStimList)
        highlightImages = pd.DataFrame(imgList.keys(), columns=['imageName'])
        highlightImages[['faceID', 'rowCol']] = highlightImages['imageName'].str.split('_', expand=True)
        trialList = highlightImages.merge(rowColPositions, how='outer')        
                
        # set up handler to look after randomisation of trials
        rowColHighlightTrials = data.TrialHandler(nReps=1.0, method='random', 
                                                extraInfo=expInfo, 
                                                originPath=-1,
                                                trialList=trialList.to_dict('records'),
                                                seed=None, 
                                                name='rowColHighlightTrials'
                                                )        
        
        thisExp.addLoop(rowColHighlightTrials)  # add the loop to the experiment
        
        # Loop over trials within the block
        for thisTrial in rowColHighlightTrials:
            # currentLoop = rowColHighlightTrials

            rowColHighlight = imgList[thisTrial['imageName']]
            rowColHighlight.pos = eval(thisTrial['position'])
            
            # --- Prepare to start Routine "trial" ---
            continueRoutine = True
            routineForceEnded = False
            
            # keep track of which components have finished
            trialComponents = [spellerMatrix, rowColHighlight]
            for thisComponent in trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "trial" ---
            while continueRoutine and routineTimer.getTime() < trialDuration:
                # reset par port
                if triggerMode == 'parallel':
                    p_port.setData(0)
                elif triggerMode == 'usb':    
                    UL.cbDOut(board, port, 0)
                    
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                
                # update/draw components on each frame                
                # *spellerMatrix* updates
                if spellerMatrix.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                    # keep track of start time/frame for later
                    spellerMatrix.frameNStart = frameN  # exact frame index
                    spellerMatrix.tStart = t  # local t and not account for scr refresh
                    spellerMatrix.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(spellerMatrix, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'spellerMatrix.started')
                    spellerMatrix.setAutoDraw(True)
                    
                if spellerMatrix.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > spellerMatrix.tStartRefresh + trialDuration - frameTolerance:
                        # keep track of stop time/frame for later
                        spellerMatrix.tStop = t  # not accounting for scr refresh
                        spellerMatrix.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'spellerMatrix.stopped')
                        spellerMatrix.setAutoDraw(False)
                
                # *rowColHighlight* updates
                if rowColHighlight.status == NOT_STARTED and tThisFlip >= rowColHighlightOnsetTime - frameTolerance:
                    # keep track of start time/frame for later
                    rowColHighlight.frameNStart = frameN  # exact frame index
                    rowColHighlight.tStart = t  # local t and not account for scr refresh
                    rowColHighlight.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(rowColHighlight, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'rowColHighlight.started')
                    rowColHighlight.setAutoDraw(True)
                    
                    # send code to EEG saying rowColHighlight occurred, and its location
                    if triggerMode == 'parallel':
                        p_port.setData(thisTrial['rowColCode'])
                    elif triggerMode == 'usb':    
                        UL.cbDOut(board, port, int(thisCondition['rowColCode']))
                        
                if rowColHighlight.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > rowColHighlight.tStartRefresh + rowColHighlightDuration - frameTolerance:
                        # keep track of stop time/frame for later
                        rowColHighlight.tStop = t  # not accounting for scr refresh
                        rowColHighlight.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'rowColHighlight.stopped')
                        rowColHighlight.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
                    break
                
                continueRoutine = False  # will revert to True if at least one component still running
                
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "trial" ---
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            if triggerMode == 'parallel':
                p_port.setData(0)
            elif triggerMode == 'usb':    
                UL.cbDOut(board, port, 0)                
            # if par_port_rowcol.status == STARTED:
            #     win.callOnFlip(par_port_rowcol.setData, int(0))
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if routineForceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(0 - trialDuration)
            thisExp.nextEntry()
            
        # completed 1.0 repeats of 'rowColHighlightTrials'
        
        
        # --- Prepare to start Routine "Counting" ---
        if testMode == False:
            continueRoutine = True
            routineForceEnded = False
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_2
            event.clearEvents('keyboard')
            
            countingPrompt.reset()
            
            # keep track of which components have finished
            CountingComponents = [askCount, countingPrompt]
            for thisComponent in CountingComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Counting" ---
            while continueRoutine:
               # get current time
               t = routineTimer.getTime()
               tThisFlip = win.getFutureFlipTime(clock=routineTimer)
               tThisFlipGlobal = win.getFutureFlipTime(clock=None)
               frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
               # update/draw components on each frame
               
               # *askCount* updates
               if askCount.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                   # keep track of start time/frame for later
                   askCount.frameNStart = frameN  # exact frame index
                   askCount.tStart = t  # local t and not account for scr refresh
                   askCount.tStartRefresh = tThisFlipGlobal  # on global time
                   win.timeOnFlip(askCount, 'tStartRefresh')  # time at next scr refresh
                   # add timestamp to datafile
                   thisExp.timestampOnFlip(win, 'askCount.started')
                   askCount.setAutoDraw(True)
               
               # *countingPrompt* updates
               if countingPrompt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                   # keep track of start time/frame for later
                   countingPrompt.frameNStart = frameN  # exact frame index
                   countingPrompt.tStart = t  # local t and not account for scr refresh
                   countingPrompt.tStartRefresh = tThisFlipGlobal  # on global time
                   win.timeOnFlip(countingPrompt, 'tStartRefresh')  # time at next scr refresh
                   # add timestamp to datafile
                   thisExp.timestampOnFlip(win, 'countingPrompt.started')
                   countingPrompt.setAutoDraw(True)
               
               # check for quit (typically the Esc key)
               if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                   core.quit()
               
               keys = event.getKeys()
               if 'return' in keys:
                   # do not show a new line break in the typed response
                   countingPrompt.text = countingPrompt.text[:-1]
                   # check if the response is empty and only allow the routine to end if something has been typed
                   continueRoutine = checkEmpty(countingPrompt.text)
                   # clear the keyboard keys and watch for a new response
                   event.clearEvents('keyboard')
               
               # check if all components have finished
               if not continueRoutine:  # a component has requested a forced-end of Routine
                   routineForceEnded = True
                   break
               continueRoutine = False  # will revert to True if at least one component still running
               for thisComponent in CountingComponents:
                   if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                       continueRoutine = True
                       break  # at least one component has not yet finished
               
               # refresh the screen
               if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                   win.flip()
           
            # --- Ending Routine "Counting" ---
            for thisComponent in CountingComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
                    
            targets.addData('countingPrompt.text', countingPrompt.text)
            
            # the Routine "Counting" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
        
        # check if we're done with targets for this condition
        targetCount += 1

        if targetCount == targetsPerCond:
            targets.finished = True
             
    # completed 1.0 repeats of 'target'
       
    
    #################################################
    # --- Prepare to start Routine "btwCondBreak" ---
    if testMode == False or testMode==True:
        continueRoutine = True
        routineForceEnded = False
        # update component parameters for each repeat
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # keep track of which components have finished
        btwCondBreakComponents = [key_resp, breakInstr1, breakInstr2]
        for thisComponent in btwCondBreakComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "btwCondBreak" ---
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
                    
            # *breakInstr1* updates
            if breakInstr1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                breakInstr1.frameNStart = frameN  # exact frame index
                breakInstr1.tStart = t  # local t and not account for scr refresh
                breakInstr1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(breakInstr1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'breakInstr1.started')
                breakInstr1.setAutoDraw(True)
                
            if breakInstr1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > breakInstr1.tStartRefresh + minBreakDurn - frameTolerance:
                    # keep track of stop time/frame for later
                    breakInstr1.tStop = t  # not accounting for scr refresh
                    breakInstr1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'breakInstr1.stopped')
                    breakInstr1.setAutoDraw(False)
            
            # *breakInstr2* updates
            if breakInstr2.status == NOT_STARTED and tThisFlip >= minBreakDurn - frameTolerance:
                # keep track of start time/frame for later
                breakInstr2.frameNStart = frameN  # exact frame index
                breakInstr2.tStart = t  # local t and not account for scr refresh
                breakInstr2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(breakInstr2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'breakInstr2.started')
                breakInstr2.setAutoDraw(True)
                
            # *key_resp* updates
            waitOnFlip = False
            if key_resp.status == NOT_STARTED and tThisFlip >= minBreakDurn - frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.started')
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in btwCondBreakComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        
        # --- Ending Routine "btwCondBreak" ---
        for thisComponent in btwCondBreakComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        conditions.addData('key_resp.keys',key_resp.keys)
        if key_resp.keys != None:  # we had a response
            conditions.addData('key_resp.rt', key_resp.rt)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-180.000000)
        thisExp.nextEntry()
    
# completed 1.0 repeats of 'conditions'


##########################
# --- End experiment --- #
##########################
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText('data/' + logFileStem + '.csv', delim='auto')
# thisExp.saveAsPickle(logFileStem)
logging.flush()
    
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()


