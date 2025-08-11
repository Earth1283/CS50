from utils import validate
def testValidate():
    assert validate("hello", ["hello", "goodbye"], False) == True
    assert validate("goodbye", ["1", "2", "3"], False) == False