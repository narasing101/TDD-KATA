require 'minitest/autorun'

class StringCalculator
  class NegativeNumberError < StandardError; end

  def add(numbers)
    return 0 if numbers.empty?

    delimiter = ",|\n"
    if numbers.start_with?("//")
      parts = numbers.split("\n", 2)
      delimiter_part = parts[0][2..-1]

      if delimiter_part.start_with?('[') && delimiter_part.end_with?(']')
        delimiters = delimiter_part[1..-2].split('][')
        delimiter = delimiters.map { |d| Regexp.escape(d) }.join('|')
      else
        delimiter = Regexp.escape(delimiter_part)
      end

      numbers = parts[1]
    end

    number_list = numbers.split(/#{delimiter}/).map(&:to_i).reject { |n| n > 1000 }
    negatives = number_list.select { |n| n < 0 }

    if negatives.any?
      raise NegativeNumberError, "negative numbers not allowed: #{negatives.join(', ')}"
    end

    number_list.reduce(0, :+)
  end
end

class TestStringCalculator < Minitest::Test
  def setup
    @calculator = StringCalculator.new
  end

  def test_empty_string
    assert_equal 0, @calculator.add("")
  end

  def test_single_number
    assert_equal 1, @calculator.add("1")
  end

  def test_two_numbers
    assert_equal 6, @calculator.add("1,5")
  end

  def test_multiple_numbers
    assert_equal 10, @calculator.add("1,2,3,4")
  end

  def test_newline_delimiters
    assert_equal 6, @calculator.add("1\n2,3")
  end

  def test_custom_delimiter
    assert_equal 3, @calculator.add("//;\n1;2")
  end

  def test_ignore_large_numbers
    assert_equal 2, @calculator.add("2,1001")
  end

  def test_custom_delimiter_any_length
    assert_equal 6, @calculator.add("//[***]\n1***2***3")
  end

  def test_multiple_custom_delimiters
    assert_equal 6, @calculator.add("//[*][%]\n1*2%3")
  end

  def test_multiple_custom_delimiters_any_length
    assert_equal 6, @calculator.add("//[**][%%]\n1**2%%3")
  end

  def test_negative_numbers
    assert_raises(StringCalculator::NegativeNumberError) { @calculator.add("1,-2,3") }
  end

  def test_multiple_negative_numbers
    assert_raises(StringCalculator::NegativeNumberError) { @calculator.add("1,-2,3,-4") }
  end
end
