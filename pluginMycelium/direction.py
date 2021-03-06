'''
Copyright 2103 Lloyd Konneker
License: GPLv3
'''
import random

from pixmap.coord import Coord


class Direction(object):
  '''
  A direction a automata can move.
  Limited to 8 cardinal directions, to each adjacent pixel.
  
  Inconsequential orientation of axis: that x increases to right, y increases down.
  
  TODO: for Paterson's worms, only 6 directions.
  I.E. consider the grid triangularly connected.
  
  Responsibility:
  - know squirminess
  - tweak self: change self controlled by squirminess
  - fork self
  '''
  
  unitCoords = [Coord( 1,-1),  # NE
                Coord( 0,-1),  # N
                Coord(-1,-1),  # NW
                Coord(-1, 0),  # W
                Coord(-1, 1),  # SW
                Coord( 0, 1),  # S 
                Coord( 1, 1),  # SE
                Coord( 1, 0),  # E
                ]
  
  # Class attribute squirminess.  All automata have the same squirminess
  squirminess = None
  
  @classmethod
  def setSquirminess(cls, squirminess):
    '''
    Set class's squirminess (choices for turning) by dispatch on parameter.
    Static over life of program and automata.
    '''
    if squirminess == 0: # Relaxed, straight (no turn) is a choice
      result = [-1, 0, 1]
    elif squirminess == 1:
      result = [1, -1] # Curly, always turn, but slightly
    elif squirminess == 2:
      result = [-2, 0, 2] # Kinky, hard turn or straight
    elif squirminess == 3:
      result = [-1, 0, 1, 4]  # Plodding: relaxed or reverse
    elif squirminess == 4:
      result = [-4, -3, -2, -1, 0, 1, 2, 3]  # Unbiased: any direction (but not a None direction.)
    else:
      result = [-2, -1, 0]  # Circling, straight or left
      
    # [-2, -1, 0, 1, 2]
    Direction.squirminess = result
  
  
  
  def __init__(self, cardinal=None):
    if cardinal is None:
      # initialize randomly
      self.index=random.randint(0,7)
    else:
      assert cardinal >= 0 and cardinal <=7
      self.index = cardinal
      
  
  def tweak(self):
    ''' Change direction slightly, to next or previous. '''
    choice = random.choice(Direction.squirminess)
    self.index += choice
    self.index = self.index % 8 # modulo
    
    
  def unitCoordFor(self):
    ''' Direction's Coord, that can be added to another Coord. '''
    return Direction.unitCoords[self.index]
  
  
  def swathCoords(self):
    ''' 
    Sequence of Direction's Coord, for this pixel and pixels to the side. 
    '''
    right = Direction.unitCoords[(self.index + 2) % 8]
    left = Direction.unitCoords[(self.index - 2) % 8]
    return (Coord( 0,0), left, right )
  
  
  def setOpposite(self, other):
    ''' Set self opposite to other. '''
    self.index = other.index - 4
    self.index = self.index % 8
    
    
  def fork(self):
    ''' Two directions slightly left and right of self. '''
    leftIndex = (self.index - 1 ) % 8
    rightIndex = (self.index + 1 ) % 8
    return Direction(cardinal=leftIndex), Direction(cardinal=rightIndex)
  
  
  