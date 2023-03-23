import sacn # Packages for whatever
import os # This one creates folders and interacts with the host system

universe_1 = [0] * 512 # Initialise the universe
fixture_groups = [[]] * 100 # And the fixture groups

sender = sacn.sACNsender(fps=30)  # provide an IP-Address to bind to if you want to send multicast packets from a specific interface
sender.start()  # start the sending thread
sender.activate_output(1)  # start sending out data in the 1st universe
sender[1].multicast = True  # set multicast to True

class DirectOperation: # This class does some useful stuff, like directly appending the fixture values
    def AppendUni(fixtures, universe, level):
        for singleFixture in fixtures: # Take each fixture and put it to the level
                universe[singleFixture-1] = level # Fucking 0-indexing
                OutputManagement.SendPackets(universe) # BLAST OFF

class ErrorHandler: # If you can't unpack what this means, you have noodles for brains.
    def RaiseError(text):
        print(text)

class OutputManagement:
    def SendPackets(data): # Send Packets blasts the sACN data out to to universe
        sender[1].dmx_data = data
    def ThruHandler(inputString): # This probably doesn't belong here, but using the Thru function is pretty useful
        if "thru" in inputString: # If you find Thru in a term
             location = inputString.find("thru") # Get the location
             firstNum = int(inputString[:location]) # Get the first number
             lastNum = int(inputString[location+4:]) # And the last
             return list(range(firstNum,lastNum+1)) # Return the range of numbers
        else:
             return None # Return None if it's not there (most likely)

print("Punch Lighting - PC Control - V1") # Just for shits and gigs, but whatever.

while True: # Main loop that does stuff
    stepCount = 1 # Python doesn't have an incremental counter and I want to die
    cmd = input("> ").lower().split() # Carry the input into a list that I can term-unpack
    for items in cmd: # Unpack by term
         if items == 'at': # If you use the hot-word 'at'
              if cmd[stepCount-1].startswith("g"): # Looks for use of groups
                   selection = fixture_groups[int(cmd[stepCount-1][1:])] # Return selection to be operated on
              elif OutputManagement.ThruHandler(cmd[stepCount-1]) != None: # Or if there's a thru command
                   selection = OutputManagement.ThruHandler(cmd[stepCount-1]) # Return selection to be operated on
              else: # It's probably as simple as you think it is
                   selection = [int(cmd[stepCount-1])] # Selection was one fixture
              DirectOperation.AppendUni(selection,universe_1,int(cmd[stepCount+1])) # Make the operation with the 'selection' variable
         if items == 'record': # If you use the hot-word 'record'
              if cmd[stepCount].startswith("g") and OutputManagement.ThruHandler(cmd[stepCount+1]) != None: # Group record with Thru
                   fixture_groups[int(cmd[stepCount][1:])] = OutputManagement.ThruHandler(cmd[stepCount+1]) # User is trying to record a group using a Thru selection
              elif cmd[stepCount].startswith("g") and OutputManagement.ThruHandler(cmd[stepCount+1]) == None: # Just a group recording using single fix, or comma notation
                   newFixtures = list(cmd[stepCount+1].split(",")) # Split the input up by comma delimited notation
                   fixture_groups[int(cmd[stepCount][1:])] = [int(x) for x in newFixtures] # Update the group
         if items == 'save': # If you use the hot-word 'save'
              fileDest = input('Directory to save to:     ') # Some basic input collection
              showName = input('Show Name:         ') # Show Name
              versionID = input('Which version to save as:          ') # Show Version
              try: # Try and make folder, but it may already exist...
                os.mkdir(fileDest+"/"+showName)
              except FileExistsError: # It already exists
                print() # Do nothing
              saveFile = open(fileDest+"/"+showName+"/"+"VERSION "+versionID+".plsf", "w") # Save the file with all of this information
              saveFile.write(','.join(str(e) for e in universe_1)+";\n") # Write in the universes
              saveFile.write(','.join(str(e) for e in fixture_groups)+";\n") # Write in the fixture groups
              saveFile.close() # Close the file
         if items == 'load': # Load the file with the save data
              fileDest = input('Directory to load from:     ') # Directory load
              showName = input('Show Name:         ') # Show Name
              versionID = input('Which version to load:          ') # Version to load
    stepCount = stepCount + 1 # Increment step counter