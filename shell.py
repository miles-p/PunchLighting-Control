import sacn
import os

universe_1 = [0] * 512
fixture_groups = [[]] * 100

sender = sacn.sACNsender(fps=30)  # provide an IP-Address to bind to if you want to send multicast packets from a specific interface
sender.start()  # start the sending thread
sender.activate_output(1)  # start sending out data in the 1st universe
sender[1].multicast = True  # set multicast to True

class DirectOperation:
    def AppendUni(fixtures, universe, level):
        for singleFixture in fixtures:
                universe[singleFixture-1] = level
                OutputManagement.SendPackets(universe)

class ErrorHandler:
    def RaiseError(text):
        print(text)

class OutputManagement:
    def SendPackets(data):
        sender[1].dmx_data = data
    def ThruHandler(inputString):
        if "thru" in inputString:
             location = inputString.find("thru")
             firstNum = int(inputString[:location])
             lastNum = int(inputString[location+4:])
             return list(range(firstNum,lastNum+1))
        else:
             return None

print("Punch Lighting - PC Control - V1")

while True:
    stepCount = 1
    cmd = input("> ").lower().split()
    #print(cmd)
    for items in cmd:
         if items == 'at':
              if cmd[stepCount-1].startswith("g"):
                   print(fixture_groups[int(cmd[stepCount-1][1:])])
                   selection = fixture_groups[int(cmd[stepCount-1][1:])]
              elif OutputManagement.ThruHandler(cmd[stepCount-1]) != None:
                   selection = OutputManagement.ThruHandler(cmd[stepCount-1])
              else:
                   print(cmd[stepCount-1])
                   selection = [int(cmd[stepCount-1])]
              DirectOperation.AppendUni(selection,universe_1,int(cmd[stepCount+1]))
              #print([int(cmd[stepCount])])
         if items == 'record':
              if cmd[stepCount].startswith("g") and OutputManagement.ThruHandler(cmd[stepCount+1]) != None:
                   #print(OutputManagement.ThruHandler(cmd[stepCount+1]))
                   fixture_groups[int(cmd[stepCount][1:])] = OutputManagement.ThruHandler(cmd[stepCount+1])
              elif cmd[stepCount].startswith("g"):
                   newFixtures = list(cmd[stepCount+1].split(","))
                   fixture_groups[int(cmd[stepCount][1:])] = [int(x) for x in newFixtures]
         if items == 'save':
              fileDest = input('Directory to save to:     ')
              showName = input('Show Name:         ')
              versionID = input('Which version to save as:          ')
              try:
                os.mkdir(fileDest+"/"+showName)
              except FileExistsError:
                print("")
              saveFile = open(fileDest+"/"+showName+"/"+"VERSION "+versionID+".plsf", "w")
              saveFile.write(','.join(str(e) for e in universe_1)+";\n")
              saveFile.write(','.join(str(e) for e in fixture_groups)+";\n")
              saveFile.close()
         if items == 'load':
              fileDest = input('Directory to load from:     ')
              showName = input('Show Name:         ')
              versionID = input('Which version to load:          ')
    stepCount = stepCount + 1