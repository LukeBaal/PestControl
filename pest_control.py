import errno
import os
import re
import sys
from time import sleep, time

from colorama import Back, Fore, Style, init


# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def save_open_w(path):
    mkdir_p(os.path.dirname(path))
    return open(path, "w")


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
        self.time = 0
        self.passing = True
        self.results = {}
        self.passed = {}
        self.start_times = {}
        self.current = ''

    def main(self):
        """Runner function to find and run all tests"""

        functions = [fcn for fcn in dir(self) if re.compile(
            "[Tt]est").search(fcn) != None]

        for fcn in functions:
            self.begin(fcn)
            try:
                getattr(self, fcn)()
            except Exception as e:
                self.catch(e, fcn)
        self.time = time() - self.start

        # Generate results in Junit XML Schema for use with CI services
        self.get_results_xml()

        print(self)
        if not self.passing:
            sys.exit(1)

    def begin(self, name):
        """Run This function before beginning a test function"""
        self.current = name
        self.results[name] = []
        self.passed[name] = True
        self.start_times[name] = time()

    def catch(self, e, name):
        """Catch an exception caused by a test and log it"""
        self.passing = False
        self.passed[self.current] = False
        self.results[name].append({
            "msg": repr(e),
            "type": "Error",
            "end": time(),
            "result": False
        })

    def assertEquals(self, actual, expected, msg=""):
        """ Test if actual == expected """
        if actual != expected:
            self.passing = False
            self.passed[self.current] = False
        self.results[self.current].append({
            "msg": msg,
            "type": "isEqual",
            "end": time(),
            "actual": actual,
            "expected": expected,
            "result": actual == expected
        })

    def assertTrue(self, val, msg):
        """ Test if val == True """
        if not val:
            self.passing = False
            self.passed[self.current] = False

        self.results[self.current].append({
            "msg": msg,
            "type": "isTrue",
            "end": time(),
            "actual": val,
            "expected": True,
            "result": val
        })

    def assertFalse(self, val, msg):
        """ Test if val == False """
        if val:
            self.passing = False
            self.passed[self.current] = False

        self.results[self.current].append({
            "msg": msg,
            "type": "isFalse",
            "end": time(),
            "actual": val,
            "expected": False,
            "result": not val
        })

    def failures_xml(self):
        failures = ""
        for fcn in self.results:
            for test in self.results[fcn]:
                if not test["result"]:
                    failures += "\t\t\t<failure message=\"%s\"></failure>\n" % (
                        test["msg"])
        return failures

    def results_xml(self):
        testcases = "\t\t<testcase classname=\"%s\" time=\"%f\">\n%s\n\t\t</testcase>\n" % (
            self.__class__.__name__, self.time, self.failures_xml())
        return testcases

    def get_results_xml(self):
        out = save_open_w(os.getcwd()+"/test-reports/results.xml")
        # num_tests = len(self.passed)
        num_errors = 0
        if len([test["type"] for fcn in self.results for test in self.results[fcn] if test["type"] == "Error"]) > 0:
            num_errors = 1
        if self.passed:
            num_failures = 0
        else:
            num_failures = 1
        # num_failures = len([test["type"] for fcn in self.results for test in self.results[fcn]
        #                     if test["type"] != "Error" and not test["result"]])
        out.write("<testsuites name=\"PestCase Tests\">\n\t<testsuite name=\"testsuite\" tests=\"%d\" errors=\"%d\" failures=\"%d\" time=\"%f\">\n%s\t</testsuite>\n</testsuites>" %
                  (1, num_errors, num_failures, self.time, self.results_xml()))
        out.close()

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
                            results += "%c── %sSuccess!%s %s\n" % (c,
                                                                   Fore.GREEN, Style.RESET_ALL, test["msg"])
                        else:
                            if test["type"] != "Error":
                                results += "%c── %sFailure!%s %s - Expected: %s, Got: %s\n" % (c,
                                                                                               Fore.RED, Style.RESET_ALL, test["msg"], test["expected"], test["actual"])
                            else:
                                results += "%c── %sError!%s %s\n" % (c,
                                                                     Fore.RED, Style.RESET_ALL, test["msg"])
        return results
