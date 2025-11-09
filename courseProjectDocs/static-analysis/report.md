# Static Analysis and Code Smell Detection

## Tool used:

We used SonarQube as our static analysis tool to identify bugs, vulnerabilities, and code smells in our project repository.

## Key Findings:

Multiple files in the codebase exhibited high cognitive complexity, meaning certain functions were performing too many tasks within a single block of code. SonarQube reported several code smells related to maintainability and readability, primarily functions exceeding the recommended cognitive complexity limit of 15.

## Fix Summary:

1. rich_help.py: After running SonarQube on rich_help.py file, one of the issues it alerted on was for the function `to_help_message()`. The warning message was for a code smell, that its computational complexity was too high, meaning that the function was trying to do too many things at once. It reported a complexity of 21 where the maximum was 15. To fix this, the function was broken up into smaller more manageable functions which are easier to maintain.

2. sessions.py: When running SonarQube on sessions.py, a code smell was noted that indicated a high cognitive complexity within the `_compute_new_headers` function. The reported complexity was 23, which exceeds SonarQube suggestion of 15 or lower. This indicates that this particular function was doing too many things in one block, reducing readability and making it difficult to maintain and refactor when necessary. To reduce this complexity and make it more modular, some of its functionality was broken down into new functions. Namely, `_check_header_skip` now handles the logic pertaining to input handling on when headers needed to be ignored and `_process_cookie_header` now handles the logic pertaining to updating cookie jars. By doing these, `_compute_new_headers` has been simplified and slightly refactored for more generic variable usage.

3. argtypes.py: After running SonarQube, `parse_format_options()` was flagged with high cognitive complexity of 20 where was maximum was 15. To bring donw the complexity `parse_format_options()` was broken down into `_parse_option_token()` `_coerce_value()` `_ensure_defaults_shape()` helper functions. After re-running tests and SonarCloud, the cognitive-complexity warning cleared for this function.

## Group Contribution:

| Member   | Task                                              | 
| -------- | ------------------------------------------------- |
| Chris | Fixed the complexity issue in rich_help.py by splitting to_help_message() into multiple smaller helper functions for better readability and structure. |
|Dan | Resolved the high-complexity issue in sessions.py by modularizing logic in _compute_new_headers() into smaller dedicated functions. |
|Vinayaka | Fixed the complexity issue in argtypes.py by refactoring the parse_format_options() function into smaller, reusable helper functions. |
