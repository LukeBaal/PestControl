# Pest Control

A Python Test Control (Pest Control) Library

## Usage


example:
'''python
from pest_control import PestCase
class BasicTestCase(PestCase):
    def add_test(self):
        self.assertEquals(1+1, 2, "simple add test")

if __name__ == "__main__":
    PestCase().main()
'''
