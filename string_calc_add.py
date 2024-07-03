import re
import unittest


def add(numbers):
    if not numbers:
        return 0

    delimiter = ",|\n"
    if numbers.startswith("//"):
        # Check for custom delimiters
        parts = numbers.split("\n", 1)
        delimiter_part = parts[0][2:]

        # Support for multiple delimiters
        if delimiter_part.startswith('[') and delimiter_part.endswith(']'):
            delimiter_part = delimiter_part[1:-1]
            delimiters = delimiter_part.split('][')
            delimiter = '|'.join(re.escape(d) for d in delimiters)
            print(delimiter_part," --", delimiters, " --", delimiter)
        else:
            delimiter = re.escape(delimiter_part)

        numbers = parts[1]

    # Splitting numbers by delimiters
    number_list = re.split(delimiter, numbers)
    num_list = [int(num) for num in number_list if num and int(num) <= 1000]

    # Checking for negative numbers
    negatives = [num for num in num_list if num < 0]
    if negatives:
        raise ValueError(f"negative numbers not allowed {','.join(map(str, negatives))}")

    return sum(num_list)


# Test cases are below
class TestStringCalculator(unittest.TestCase):

    def test_empty_string(self):
        self.assertEqual(add(""), 0)

    def test_single_number(self):
        self.assertEqual(add("1"), 1)

    def test_two_numbers(self):
        self.assertEqual(add("1,5"), 6)

    def test_multiple_numbers(self):
        self.assertEqual(add("1,2,3,4"), 10)

    def test_newline_delimiters(self):
        self.assertEqual(add("1\n2,3"), 6)

    def test_custom_delimiter(self):
        self.assertEqual(add("//;\n1;2"), 3)

    def test_ignore_large_numbers(self):
        self.assertEqual(add("2,1001"), 2)

    def test_custom_delimiter_any_length(self):
        self.assertEqual(add("//[***]\n1***2***3"), 6)

    def test_multiple_custom_delimiters(self):
        self.assertEqual(add("//[*][%]\n1*2%3"), 6)

    def test_multiple_custom_delimiters_any_length(self):
        self.assertEqual(add("//[**][%%]\n1**2%%3"), 6)

    def test_negative_numbers(self):
        with self.assertRaises(ValueError) as context:
            add("1,-2,3")
        self.assertIn("negative numbers not allowed -2", str(context.exception))

    def test_multiple_negative_numbers(self):
        with self.assertRaises(ValueError) as context:
            add("1,-2,3,-4")
        self.assertIn("negative numbers not allowed -2,-4", str(context.exception))


if __name__ == "__main__":
    unittest.main()
