#Imports the unittest module for creating and running tests
import unittest

#Imports the Stack class from the main module
from main import Stack

#Creates the test class that inherits from unittest.TestCase
class TestStack(unittest.TestCase):
    #Defines the test case for testing push and pop operations
    def test_push_pop(self):
        #Creates the instance of the Stack class
        stack = Stack()

        #Pushes two values onto the stack
        stack.push(1)
        stack.push(2)
        
        #Checks if the top element popped is 2
        self.assertEqual(stack.pop(), 2)
        #Checks if the next top element popped is 1
        self.assertEqual(stack.pop(), 1)
        #Checks if the stack is empty after popping all elements
        self.assertTrue(stack.is_empty())

    #Defines the test case for testing the is_empty method
    def test_is_empty(self):
        #Creates the instance of the Stack class
        stack = Stack()
        
        #Checks if the stack is initially empty
        self.assertTrue(stack.is_empty())

        #Pushes a value onto the stack
        stack.push(1)
        #Checks if the stack is not empty after pushing
        self.assertFalse(stack.is_empty())

#Checks if the script is being run directly (not imported as a module)
if __name__ == '__main__':
    #Runs the tests using the unittest framework
    unittest.main()


#Seeing OK in the terminal means that both of the test cases (test_push_pop and test_is_empty) passed without any issues. 
#This is a good outcome, indicating that the Stack implementation appears to be working correctly according to the test cases that I defined.