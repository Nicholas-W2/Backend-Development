import unittest
from validate_password import validate_password  # Replace 'your_module' with the correct module name

class TestPasswordValidator(unittest.TestCase):

    def test_valid_password(self):
        """Test a valid password that meets all criteria."""
        password = "Valid1@Password"
        self.assertTrue(validate_password(password))

    def test_too_short_password(self):
        """Test a password that's too short (less than 8 characters)."""
        password = "Short1@"
        self.assertFalse(validate_password(password))

    def test_missing_uppercase(self):
        """Test a password without an uppercase letter."""
        password = "lowercase1@"
        self.assertFalse(validate_password(password))

    def test_missing_lowercase(self):
        """Test a password without a lowercase letter."""
        password = "UPPERCASE1@"
        self.assertFalse(validate_password(password))

    def test_missing_digit(self):
        """Test a password without a digit."""
        password = "NoDigit@A"
        self.assertFalse(validate_password(password))

    def test_missing_special_char(self):
        """Test a password without a special character."""
        password = "NoSpecialChar1A"
        self.assertFalse(validate_password(password))

    def test_only_special_characters(self):
        """Test a password with only special characters (should fail)."""
        password = "@#$%^&*"
        self.assertFalse(validate_password(password))

    def test_only_digits(self):
        """Test a password with only digits (should fail)."""
        password = "12345678"
        self.assertFalse(validate_password(password))

    def test_only_lowercase_letters(self):
        """Test a password with only lowercase letters (should fail)."""
        password = "abcdefg"
        self.assertFalse(validate_password(password))

    def test_only_uppercase_letters(self):
        """Test a password with only uppercase letters (should fail)."""
        password = "ABCDEFG"
        self.assertFalse(validate_password(password))

if __name__ == '__main__':
    unittest.main()

