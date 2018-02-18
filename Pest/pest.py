from colorama import init, Fore, Back, Style
from time import time
from math import floor

# Initialize colorama (for windows support)
init()

class Pest:
  def __init__(self):
    self.passing = True
    self.results = []
    self.start = time()

  """ Test if actual == expected """
  def assertEquals(self, actual, expected, name):
    if actual != expected:
      self.passing = False
    self.results.append({
      "name": name,
      "type": "isEqual",
      "actual": actual,
      "expected": expected,
      "result": actual == expected
    })

  """ Test if val == True """
  def assertTrue(self, val, name):
    if not val:
      self.passing = False

    self.results.append({
      "name": name,
      "type":"isTrue",
      "actual": val,
      "expected": True,
      "result": val
    })

  """ Test if val == False """
  def assertFalse(self, val, name):
    if val:
      self.passing = False
    
    self.results.append({
      "name": name,
      "type": "isFalse",
      "actual": val,
      "expected": False,
      "result": not val
    })

  """ Determine Results of Tests """
  def run(self):
    end = time()
    # bar_width = 20
    print("")
    if self.passing:
      print("%s  OK!  %s Completed in %fsec" %(Back.GREEN, Style.RESET_ALL, end - self.start))
      # print("%s%*s%s %sOK!%s Completed in %fsec" %(Back.GREEN, bar_width, '', Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL, end - self.start))
    else:
      # passed = 0
      # for test in self.results:
      #   if test["result"]:
      #     passed += 1      
      # passed = floor(passed/len(self.results) * bar_width)
      # print("%s%*s%s%*s%s %s" %(Back.GREEN, passed, '', Back.RED, bar_width - passed, '', Style.RESET_ALL, "Failure!"))
      print("%s  FAILURE!  %s" %(Back.RED, Style.RESET_ALL))
      for test in self.results:
        if test["result"]:
          print("%sSuccess!%s %s" %(Fore.GREEN, Style.RESET_ALL, test["name"]))
        else:
          print("%sFailure!%s %s - Expected: %s, Got: %s" %(Fore.RED, Style.RESET_ALL, test["name"], test["expected"], test["actual"]))                    
