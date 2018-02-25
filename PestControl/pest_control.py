import re
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
        self.start = time()
        self.passing = True
        self.results = {}
        self.passed = {}
        self.current = ''

    def main(self):
        """Runner function to find and run all tests"""

        functions = [fcn for fcn in dir(self) if re.compile("[Tt]est").search(fcn) != None]

        for fcn in functions:
            self.begin(fcn)
            try:
                getattr(self, fcn)()
            except Exception as e:
                self.catch(e, fcn)
        print(self)

    def begin(self, name):
        self.current = name
        self.results[name] = []
        self.passed[name] = True

    def catch(self, e, name):
        """Catch an exception caused by a test and log it"""
        self.passing = False
        self.passed[self.current] = False
        self.results[name].append({
            "msg": repr(e),
            "type": "Error",
            "result": False
        })

    def assertEquals(self, actual, expected, msg=""):
        """ Test if actual == expected """
        start = time()
        if actual != expected:
            self.passing = False
            self.passed[self.current] = False
        self.results[self.current].append({
            "msg": msg,
            "type": "isEqual",
            "time": time() - start,
            "actual": actual,
            "expected": expected,
            "result": actual == expected
        })

    def assertTrue(self, val, msg):
        """ Test if val == True """
        start = time()
        if not val:
            self.passing = False
            self.passed[self.current] = False

        self.results[self.current].append({
            "msg": msg,
            "type": "isTrue",
            "time": time() - start,
            "actual": val,
            "expected": True,
            "result": val
        })

    def assertFalse(self, val, msg):
        """ Test if val == False """
        start = time()
        if val:
            self.passing = False
            self.passed[self.current] = False

        self.results[self.current].append({
            "msg": msg,
            "type": "isFalse",
            "time": time() - start,
            "actual": val,
            "expected": False,
            "result": not val
        })

    def __repr__(self):
        """ Determine Results of Tests """
        results = "\n"
        if self.passing:
            results += "%s%s  OK! %d tests completed in %fsec  %s\n" % (
                Back.GREEN, Fore.BLACK, len(self.passed), time() - self.start, Style.RESET_ALL)
        else:
            results += "%s  FAILURE! %d tests completed in %fsec  %s\n" % (
                Back.RED, len(self.passed), time() - self.start, Style.RESET_ALL)
            for fcn in self.results:
                if self.passed[fcn]:
                    results += "%sSuccess!%s %s\n" % (
                        Fore.GREEN, Style.RESET_ALL, fcn)
                else:
                    results += "%sFailure!%s %s\n" % (
                        Fore.RED, Style.RESET_ALL, fcn)
                    for index, test in enumerate(self.results[fcn]):
                        c = '├'
                        if len(self.results[fcn]) == index + 1:
                            c = '└'
                        if test["result"]:
                            results += "%c── %sSuccess!%s in %fsec %s\n" % (c,
                                                                            Fore.GREEN, Style.RESET_ALL, test["time"], test["msg"])
                        else:
                            if test["type"] != "Error":
                                results += "%c── %sFailure!%s in %fsec %s - Expected: %s, Got: %s\n" % (c,
                                                                                                        Fore.RED, Style.RESET_ALL, test["time"], test["msg"], test["expected"], test["actual"])
                            else:
                                results += "%c── %sFailure!%s in %fsec %s\n" % (c,
                                                                                Fore.RED, Style.RESET_ALL, test["time"], test["msg"])
        return results
