#!/usr/bin/env python
#
# Python script for solving 3D tic tac toe programming question from Defcon CTF Quals 2014
#
# Jennifer Newton - May 2014
#
#
#
import socket
import time
import re

# Determined the position of each play location in the buffer received
# Compiled indices of positions just by playing an X there and determining its index in the buffer received
# 0,0,0  ->  25 
# 0,0,1  ->  119
# 0,0,2  ->  213
# 0,1,0  ->  53
# 0,1,1  ->  147
# 0,1,2  ->  241
# 0,2,0  ->  81
# 0,2,1  ->  175
# 0,2,2  ->  269
# 1,0,0  ->  29
# 1,1,0  ->  57
# 1,1,2  ->  245
# 1,2,0  ->  85
# 1,2,1  ->  179
# 1,2,2  ->  273
# 1,0,1  ->  123
# 1,0,2  ->  217
# 1,1,1  ->  151
# 2,0,0  ->  33
# 2,0,1  ->  127
# 2,0,2  ->  221
# 2,1,0  ->  61
# 2,1,1  ->  155
# 2,1,2  ->  249
# 2,2,0  ->  89
# 2,2,1	 ->  183
# 2,2,2  ->  277

# Map all indices to their formatted position string 
indices = {25:"0,0,0",119:"0,0,1",213:"0,0,2",53:"0,1,0",147:"0,1,1",241:"0,1,2",81:"0,2,0",175:"0,2,1",
  269:"0,2,2",29:"1,0,0",57:"1,1,0",245:"1,1,2",85:"1,2,0",179:"1,2,1",273:"1,2,2",123:"1,0,1",217:"1,0,2",
  151:"1,1,1",33:"2,0,0",127:"2,0,1",221:"2,0,2",61:"2,1,0",155:"2,1,1",249:"2,1,2",89:"2,2,0",183:"2,2,1",277:"2,2,2"}

# List of prioritized locations to play if no blocks or lines can be made (will play corners first)
randomList = [25,213,33,221,81,89,277,269,119,53,147,241,175,29,57,245,85,179,273,123,217,127,61,155,249,183]

# Creation of line list
# Consider top plane
linelist = []
linelist.append([213,217,221])
linelist.append([241,245,249])
linelist.append([269,273,277])
linelist.append([213,241,269])
linelist.append([217,245,273])
linelist.append([221,249,277])

# Bottom plane
linelist.append([25,29,33])
linelist.append([53,57,61])
linelist.append([81,85,89])
linelist.append([25,53,81])
linelist.append([29,57,85])
linelist.append([33,61,89])

# Left plane (two lines already covered by top/bottom plane)
linelist.append([25,119,213])
linelist.append([53,147,241])
linelist.append([81,175,269])
linelist.append([119,147,175])

# Right plane (two lines already covered by top/bottom plane)
linelist.append([221,127,33])
linelist.append([249,155,61])
linelist.append([277,183,89])
linelist.append([127,155,183])

# Front plane (only center lines not covered by other planes)
linelist.append([175,179,183])
linelist.append([273,179,85])

# Back plane (only center lines not covered by other planes)
linelist.append([217,123,29])
linelist.append([119,123,127])

# Diagonals 
linelist.append([213,151,89])  # mid
linelist.append([269,151,33]) 
linelist.append([89,151,25])   
linelist.append([221,151,81]) 

linelist.append([269,179,89])  # front
linelist.append([277,179,81])

linelist.append([213,245,277]) # top
linelist.append([221,245,269])

linelist.append([25,147,269])  # left
linelist.append([213,147,81])

linelist.append([277,155,33])
linelist.append([221,155,89])  # right

linelist.append([25,57,89])    # bottom
linelist.append([81,57,33])

linelist.append([25,123,221])  # back
linelist.append([213,123,33])

# Open connection 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("3dttt_87277cd86e7cc53d2671888c417f62aa.2014.shallweplayaga.me",1234))

# Receive and print initial game board
data = s.recv(10000)
print data

# Outer loop (enters at the beginning of each new game)
while (True):

  # Play center first
  s.send ("1,1,1\n")

  # Print updated board
  data = s.recv(10000)
  print data

  # Makes one of two second moves that will set up a fork they can't block
  # Checks first spot to ensure that wasn't the one played by the opponent
  if list(data)[245] != 'O':
    s.send ("1,1,2\n")
    print "sending 1"
  else:
    s.send ("0,0,1\n")
    print "sending 2"  

  # Print updated board
  data = s.recv(10000)
  print data

  # Flag that controls exit of the turn-based loop for starting new games
  playAgain = False
  while (playAgain == False):

    turnPlayed = False
    while (turnPlayed == False):

      # Loops through line list looking for a block (highest priority)
      for i in range (0,40):

        # Counts for 'O's (bad) and 'X's (good)
        badcount = 0
        goodcount = 0

	# Checks each position in the line list, increments corresponding count if an X or O is found
        for k in range (0,3):
          if list(data)[linelist[i][k]] == 'O':
            badcount = badcount + 1
          else:
            if list(data)[linelist[i][k]] == 'X':
              goodcount = goodcount + 1

        # Checks for block condition
        if badcount == 2 and goodcount == 0:
          for j in range (0,3):
            # Makes the play at the appropriate location and prints updated board
            if list(data)[linelist[i][j]] != 'O':
              s.send(indices[linelist[i][j]]+'\n')
              data = s.recv(10000)
              turnPlayed = True
              print data

      # If no block is found, loops through line list looking to make a line
      if turnPlayed == False: 
        for q in range (0,40):
          badcount = 0
          goodcount = 0
          for k in range (0,3):
            if list(data)[linelist[q][k]] == 'O':
              badcount = badcount + 1
            else:
              if list(data)[linelist[q][k]] == 'X':
                goodcount = goodcount + 1
          
          # Checks for ability to make a line
          if goodcount == 2 and badcount == 0:
            for l in range (0,3):
              # Makes the play at the appropriate location and prints updated board
              if list(data)[linelist[q][l]] != 'X':
                s.send(indices[linelist[q][l]]+'\n')
                data = s.recv(10000)
                print data
                turnPlayed = True

      # If no block or line is possible, will play a move from the not so random randomList
      if (turnPlayed == False):
        # Take action, prioritize corners
        for i in range (0,len(randomList)):
          if (list(data)[randomList[i]] != 'X' and list(data)[randomList[i]] != 'O'):
            s.send(indices[randomList[i]]+'\n')
            data = s.recv(10000)
            print data
            turnPlayed = True

    # Sets the flag to exit the turn loop and start a new game
    if "play again" in data:
       playAgain = True
       print "Playing again!"  










