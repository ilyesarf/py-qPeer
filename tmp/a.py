import random
x = [i for i in range(random.randint(1,5))]
def func():
  while True:
    try:
      if len(x) == 3:
        a = random.choice(x)
        print(a*10)
      else:
        raise Exception
    except Exception:
      print("Excepted")
      pass

func()

