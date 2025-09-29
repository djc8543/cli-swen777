# Unit Testing Report

## Summary

Fifteen new unit tests have been added, encompassing missed coverage in utils.py, plugins/base.py, output/ui/palette.py, output/ui/man_pages.py, and compat.py. This addition has improved overall code coverage by 1% and covered an additional 23 statements. The team decided to focus on these files due to their lower overall coverage compared or uncovered edge cases, then determined which tests to implement based on their potential impacts to the system. Below is a more detailed view of the coverage improvement on a per-file basis:

|**File**|**Rationale**|**Missing Statements Before**|**Missing Statements After**|**Coverage Before**|**Coverage After**|
|---|---|--:|--:|--:|--:|
|utils.py|Uncovered edge cases|4|4|97%|97%|
|plugins/base.py|Uncovered edge cases|3|3|92%|92%|
|output/ui/palette.py|Uncovered edge cases|6|6|92%|92%|
|output/ui/man_pages.py|Low coverage|16|0|0%|100%|
|compat.py|Low coverage|31|24|45%|57%|

To reproduce these results, follow the steps found in [this testing instructions file](/courseProjectCode/Metrics/README.md). This will run all tests and generate a report that will verify the information above. For quick comparison, you can compare results from the [old coverage report](/courseProjectDocs/Setup/Statement_coverage_report.png) against the [new coverage report](/courseProjectDocs/Unit-Testing/updated_coverage_report.png). Please see below for detailed information for all fifteen new unit tests included with this update.

## test_utils.py

1. `test_is_version_greater_value_error()`
    -  The function is_version_greater(a, b) determines if version a > b. It loops over the versions and finds each '.', from there is attempts to convert the string to a number. If it fails to convert to a number, it stops at the last '.' and then does the comparison. When it does fail to convert, it throws an exception, this exception is never tested.

2. `test_humanize_bytes()`
    - The function humanize_bytes(n, precision) takes in a number of bytes along with a decimal precision value and converts the number into a human readable value, such as MB, GB, TB, ... This function is never tested since it is never called inside of the HTTPIE repo, however, the function itself is public, meaning that it can be called. HTTPIE has a plugin tool, meaning that this function can be used by developers and needs to be tested.

3. `test_open_with_lockfile_file_exists_error()`
    - The function open_with_lockfile(file, args**) attepts to open the specified file with the appropriate args, these arguments being all types of file operations (r, w). Before opening the file, it checks to see if the file is in a locked state, meaning that the file is open in another location. When it does detect a lock, it throws an exception, this exception is never tested.

## test_plugins_cli.py

4. `test_auth_plugin_get_auth_raises()`
    - The function get_auth(username, password) is found within the AuthPlugin class. This class is not implemented directly inside of HTTPIE but it does provide an interface which can be implemented by external plugin systems. Since the functions inside of AuthPlugin are not implemented, they all throw a NotImplementedError, this error throwing is never tested.

## test_output.py

5. `test_colorstring_or_styled_generic_color()`
    - The class ColorString is used as a decorator for UI output seen by the user. The user may set what this styling property is. Once the color is styled it becomes a _StyledGenericColor, when combined with a base value such as BOLD, the list of decorated properties on that color extends, this logic is never tested.

## test_man_pages.py

6. `test_is_available_short_circuits()`
    - This test verifies that when NO_MAN_PAGES is set to True, the is_available() function immediately returns False without calling the man command and entering the subprocess try block.

7. `test_is_available_success_returncode_zero()`
    - This test simulates a successful man 1 http execution by mocking subprocess.run to return a 0 exit code, which ensures that is_availabe is correctly returing true.

8. `test_is_available_not_found_nonzero()`
    - This test mocks subprocess.run to return a non-zero exit code, which mimicks the case where there is no manual page which is present in the program. It ensures that is_available is correctly returing False.

9. `test_is_available_exception_path()`
    - This test forces subprocess.run to raise an OSError which tests the exception block returns False if theres any exception.

10. `test_display_for_calls_man_with_env_streams()`
    - This test ensures that display_for calls the system man command with the correct arguments and correctly routes output and error streams to the provided Environment.

## test_compat.py

11. `test_cached_property_conflicts()`
    - This test verifies that a cached_property of a class cannot be reused with a different name inside of a new class. This is done by intentionally creating a conflict and verifying that the expected TypeError is thrown.

12. `test_cached_values()`
    - This test validates that cached property values are only computed once, not being recalculated upon each method call. This is done by checking that the value method has only been called once after accessing the data twice.

13. `test_find_entry_points_formats()`
    - This test verifies that find_entry_points supports modern and legacy plugin formats. This is done by checking both a modern object and a legacy dictionary for their entry points.

14. `test_get_dist_name()`
    - This test verifies that get_dist_name extracts the package name from a plugin entry point. This is done by checking that both an entry point with a .dist and an entry point with only a value can still have their package name extracted.

15. `test_default_certs_load()`
    - This test validates that default certifications are loaded when no CA certificates are found. This is done by mocking an SSL context with an empty certificate list, checking for its CA certificates, and ensuring the default certificates are loaded when no CA certificates are found.