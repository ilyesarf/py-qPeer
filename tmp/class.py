import random

class Test:
  def __init__(self, msg, state):
    self.msg = msg
    self.state = state
  def func(self):
    def junk():
      return self.msg
    #return 'Hey'
    if self.state == 1:
      return junk()
    else:
      return 'No'

state = random.randint(0,1)
msg = input("Msg? ")
test = Test(msg, state)

print(test.func())
