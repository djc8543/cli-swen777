# Unit tests Mocking

## Summary

Eight new unit tests have been added, while two previous unit tests have been included in this document for mocking purposes. This update encompasses missed coverage in `output/writer.py`, `output/ui/rich_utils.py`, and `compat.py`. Collectively, we have covered an additional 23 statements, as well as added additional edge case logic tests for statements that had basic coverage. The team's mocking strategy came down to a combination of file familiarity, prior mocking examples, and attempting to address more areas of lower than desired coverage. We utilized a variety of different mocking libraries and tools depending on the tests being performed, including manual mocking, `unittest.mock's MagicMock`, `unittest.mock's patch`, and `MokeyPatch`. Below is a more detailed view of the coverage improvement on a per-file basis:

|**File**|**Rationale**|**Missing Statements Before**|**Missing Statements After**|**Coverage Before**|**Coverage After**|
|---|---|--:|--:|--:|--:|
|output/writer.py|Mockable|13|5|83%|93%|
|output/ui/rich_utils.py|Mockable|18|5|0%|72%|
|compat.py|Mockable|24|22|57%|61%|

To reproduce these results, follow the steps found in [this testing instructions file](/courseProjectCode/Metrics/Readme.md). This will run all tests and generate a report that will verify the information above. For quick comparison, you can compare results between the [initial coverage report](/courseProjectDocs/Setup/Statement_coverage_report.png), the [unit testing coverage report](/courseProjectDocs/Unit-Testing/updated_coverage_report.png), and the [mocking testing coverage report](/courseProjectDocs/Unit-Testing/mocking_coverage_report.png). Please see below for more information on all mocked unit tests added or detailed with this update.


## test_writer.py

- `TestWriteStreamWithColorsWin` is a class created to Mock the response of the `writer.py` file. This file is responsible for writing various messages to output files, the user may specify formatting in some instances. Specifically, this class tests the `write_stream_with_colors_win` function, which writes the information either directly to the output file or into a buffer first depending on if the output message has color formatting. We use the `unittest.mock` library to mock the API calls for file I/O so actual files don't need to be created for testing purposes. We keep track of which functions have been called, how many times they were called, and what parameters they were called with.

1. `test_color_chunk_text_write()`
    - This test verifies that colorized output is decoded, written directly to the text stream, and does not write to the binary buffer or trigger a flush.

2. `test_non_color_chunk_buffer_write()`
    - This test verifies that non-colorized output is decoded, written directly to the binary buffer, and does not write to the text stream or trigger a flush.

3. `test_mixed_chunks()`
    - This test verifies that colorized and non-colorized output is decoded, then written to the proper data handler. Colorized output is sent to the text stream while non-colorized output is sent to the binary buffer. Neither process should trigger a flush.

4. `test_flush()`
    - This test verifies that, regargless of data format, the output stream is correctly flushed post processing.

## test_rich_utils.py

5. `test_render_as_string_monkeypatched()`
    - This test mocks Rich’s Console class to verify that render_as_string() correctly calls print() and export_text() on the console and returns the expected mocked output.

6. `test_render_as_string_calls_theme_factory()`
    - This test verifies that render_as_string() correctly invokes the _make_rich_color_theme()function from the rich_palette.py file when creating the Console which ensures that a custom Rich theme is applied during rendering.

## test_compat.py

7. `def test_get_dist_name()`
    - This test verifies that get_dist_name extracts the package name from a plugin entry point. This is done by checking that both an entry point with a .dist and an entry point with only a value can still have their package name extracted. Monkeypatch is utilized to mock a metadata function and return a lambda containing a faked value. This test was created for the first unit testing section and has been reused due to its mocking.

8. `def test_get_dist_name_package_not_found()`
    - This test verifies that get_dist_name gracefully handles instances where no package name is found from a plugin entry point. MagicMock is used to create a faked plugin entry point. Patch is used to replace a metadata function so that the test raises a PackageNotFoundError for get_dist_name.

9. `test_default_certs_load()`
    - This test validates that default certifications are loaded when no CA certificates are found. This is done by manually mocking an SSL context with an empty certificate list, checking for its CA certificates, and ensuring the default certificates are loaded when no CA certificates are found. This test was created for the first unit testing section and has been reused due to its mocking.

10. `test_default_certs_load_skipped()`
    - This test validates that default certifications are not loaded if a CA certificate is found. This is done using MagicMock to create a fake ssl context that contains a fake certificate. When the certificates are retrieved, the test checks that load_default_certs was not called.