from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re

def validate_aadhar(value: str) -> None:
    """
    Validate Aadhar number format
    Args:
        value: Aadhar number to validate
    Raises:
        ValidationError: If Aadhar number is invalid
    """
    if not re.match(r'^\d{12}$', value):
        raise ValidationError('Aadhar number must be 12 digits')

def validate_abha(value: str) -> None:
    """
    Validate ABHA ID format
    Args:
        value: ABHA ID to validate
    Raises:
        ValidationError: If ABHA ID is invalid
    """
    if not re.match(r'^\d{14}$', value):
        raise ValidationError('ABHA ID must be 14 digits')

# Common validators
ZIPCODE_VALIDATOR = RegexValidator(
    r'^\d{6}$',
    'Enter a valid zipcode'
)

MOBILE_NUMBER_VALIDATOR = RegexValidator(
    r'^\d{10}$',
    'Enter a valid 10-digit mobile number'
)

OTP_VALIDATOR = RegexValidator(
    r'^\d{6}$',
    'Enter a valid 6-digit OTP'
) 