from Pest.pest import Pest
from Game.simple import *

if __name__ == "__main__":
  p = Pest()

  p.assertEquals(add(1, 1), 2, "add test")
  p.assertTrue(isEven(2), "isEven even test")
  p.assertFalse(isEven(3), "isEven odd test")

  p.run()

