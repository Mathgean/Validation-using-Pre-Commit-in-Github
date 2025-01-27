# Pre-Commit Validation for AWS User Data in YAML Files

## Purpose
The purpose of this pre-commit validation is to ensure that AWS user data across multiple YAML files adheres to a predefined set of rules before being committed to GitHub. By enforcing strict validation, this process helps maintain data integrity, reduces errors, and ensures compliance with operational and organizational standards. This also saves time by identifying issues early in the development lifecycle.

## Features
- Dynamically validates multiple YAML files for AWS user data.
- Ensures compliance with various conditions defined in a separate configuration file.
- Restricts commits if validation fails, providing detailed error messages to guide corrections.
- Streamlines collaboration by enforcing consistent data quality.

## Validation Types

### Mandatory Field Validation
Ensures that all required fields specified in the condition file are present in the YAML files.

#### Example:
If `user_id` and `role` are mandatory, a YAML file without these fields will fail validation.
```yaml
# Invalid Example
user_name: "JohnDoe"
# Missing mandatory field 'user_id'
```

### Dependency Validation
Verifies that certain fields exist only if their dependent fields are present or have specific values.

#### Example:
If `married` is `true`, then `spouse` must also be provided.
```yaml
# Invalid Example
user_id: "12345"
married: true
# Missing dependent field 'spouse'
```

### Type Checking
Validates that field values match the expected data type (e.g., string, integer, boolean).

#### Example:
If `user_id` must be an integer, providing a string will fail validation.
```yaml
# Invalid Example
user_id: "abcd123" # Expected integer, but got a string.
```

### Length Validation
Ensures that string fields meet length constraints specified in the condition file (e.g., minimum and maximum lengths).

#### Example:
If `user_name` must be between 5 and 20 characters:
```yaml
# Invalid Example
user_name: "JD" # Too short, minimum is 5 characters.
```

### Allowed Value Validation
Ensures that fields have values from a predefined set of acceptable values.

#### Example:
If `role` must be one of `admin`, `editor`, or `viewer`:
```yaml
# Invalid Example
role: "guest" # Not in the allowed values list.
```

## Workflow Overview

### Condition File
A separate configuration file defines the validation rules for mandatory fields, dependencies, types, lengths, and allowed values.

### Pre-Commit Hook
A Git pre-commit hook integrates the validation logic into the commit process. It dynamically checks all relevant YAML files in the commit.

### Error Feedback
If any validation fails, the commit is blocked, and detailed error messages indicate the specific issues and files requiring attention.

---
