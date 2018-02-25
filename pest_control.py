from time import time

from colorama import Back, Fore, Style, init


class PestCase:
    """ Python Unit Testing Library
    Note: test functions must end in "test"

    Usage:
        from pest_control import PestCase
        class BasicTestCase(PestCase):
            def add_test(self):
                self.assertEquals(1+1, 2, "simple add test")
        
        if __name__ == "__main__":
            PestCase().main()
    """

    def __init__(self):
        init()  # Colorama init
        self.passing = True
        self.results = {}
        self.start = time()
        self.current = ''

    def main(self):
        """Runner function to find and run all tests"""

        functions = [fcn for fcn in dir(self) if fcn.endswith("test")]

        for fcn in functions:
            self.begin(fcn)
            try:
                getattr(self, fcn)()
            except Exception as e:
                self.catch(e, fcn)
        print(self)

    def begin(self, name):
        self.current = name

    def catch(self, e, name):
        """Catch an exception caused by a test and log it"""
        self.passing = False
        self.results[name] = {
            "msg": repr(e),
            "type": "Error",
            "result": False
        }

    def assertEquals(self, actual, expected, msg=""):
        """ Test if actual == expected """
        if actual != expected:
            self.passing = False
        self.results[self.current] = {
            "msg": msg,
            "type": "isEqual",
            "actual": actual,
            "expected": expected,
            "result": actual == expected
        }

    def assertTrue(self, val, msg):
        """ Test if val == True """
        if not val:
            self.passing = False

        self.results[self.current] = {
            "msg": msg,
            "type": "isTrue",
            "actual": val,
            "expected": True,
            "result": val
        }

    def assertFalse(self, val, msg):
        """ Test if val == False """
        if val:
            self.passing = False

        self.results[self.current] = {
            "msg": msg,
            "type": "isFalse",
            "actual": val,
            "expected": False,
            "result": not val
        }

    def __repr__(self):
        """ Determine Results of Tests """
        results = "\n"
        end = time()
        if self.passing:
            results += "%s%s  OK!  %s Completed in %fsec\n" % (
                Back.GREEN, Fore.BLACK, Style.RESET_ALL, end - self.start)
        else:
            results += "%s  FAILURE!  %s\n" % (Back.RED, Style.RESET_ALL)
            for test in self.results:
                if self.results[test]["result"]:
                    results += "%sSuccess!%s %s\n" % (
                        Fore.GREEN, Style.RESET_ALL, test)
                else:
                    if self.results[test]["type"] != "Error":
                        results += "%sFailure!%s %s:%s - Expected: %s, Got: %s\n" % (
                            Fore.RED, Style.RESET_ALL, test, self.results[test]["msg"], self.results[test]["expected"], self.results[test]["actual"])
                    else:
                        results += "%sFailure!%s %s:%s\n" % (
                            Fore.RED, Style.RESET_ALL, test, self.results[test]["msg"])
        return results
