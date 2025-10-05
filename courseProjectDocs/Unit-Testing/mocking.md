# Unit tests Mocking

## test_writer.py

- `TestWriteStreamWithColorsWin` is a class created to Mock the response of the `writer.py` file. This file is responsible for writing various messages to output files, the user may specify formatting in some instances. Specifically, this class tests the `write_stream_with_colors_win` function, which writes the information either directly to the output file or into a buffer first depending on if the output message has color formatting. We use the `unittest.mock` library to mock the API calls for file I/O so actual files don't need to be created for testing purposes. We keep track of which functions have been called, how many times they were called, and what parameters they were called with. 

## test_rich_utils.py

1. `test_render_as_string_monkeypatched()`
- This test mocks Rich’s Console class to verify that render_as_string() correctly calls print() and export_text() on the console and returns the expected mocked output.

2. `test_render_as_string_calls_theme_factory()`
- This test verifies that render_as_string() correctly invokes the _make_rich_color_theme()function from the rich_palette.py file when creating the Console which ensures that a custom Rich theme is applied during rendering.