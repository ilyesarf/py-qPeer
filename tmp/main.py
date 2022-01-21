from test import func
from errors import *
import clt


def main(x=None):
  if x == None:
    func()
  else:
    func(x)
#x = 2
while True:
  try:
    main()
    break
  except Less:
    clt.send( "Less")
  except More:
    clt.send("More")
  except Exception as e:
    clt.send("Error")
    print(e)
  except KeyboardInterrupt:
    print("Leaving...")
    break

