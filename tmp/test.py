from errors import *

def func(a=None):
  
  if a == None:
    a = int(input('a? '))
  
  if a == 5:
    print("Yes")
    return True
  elif a < 5:
    #print("No")
    raise Less
  elif a > 5:
    raise More
  else:
    return False



