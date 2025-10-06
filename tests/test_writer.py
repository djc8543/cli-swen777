import unittest
from unittest.mock import Mock
from httpie.output.writer import write_stream_with_colors_win

class TestWriteStreamWithColorsWin(unittest.TestCase):

    def setUp(self):
        self.mock_outfile = Mock()
        self.mock_outfile.encoding = 'utf-8'
        self.mock_outfile.buffer = Mock()

    #when writing color, it goes directly into the output file
    def test_color_chunk_text_write(self):
        stream = [b'\x1b[31mred']
        write_stream_with_colors_win(stream, self.mock_outfile, flush=False)

        self.mock_outfile.write.assert_called_once_with('\x1b[31mred')
        self.mock_outfile.buffer.write.assert_not_called()
        self.mock_outfile.flush.assert_not_called()

    #when writing in non color, it goes into a buffer first
    def test_non_color_chunk_buffer_write(self):
        stream = [b'plain']
        write_stream_with_colors_win(stream, self.mock_outfile, flush=False)

        self.mock_outfile.buffer.write.assert_called_once_with(b'plain')
        self.mock_outfile.write.assert_not_called()
        self.mock_outfile.flush.assert_not_called()

    def test_mixed_chunks(self):
        stream = [b'\x1b[31mred', b'plain']
        write_stream_with_colors_win(stream, self.mock_outfile, flush=False)

        self.mock_outfile.write.assert_called_once_with('\x1b[31mred')
        self.mock_outfile.buffer.write.assert_called_once_with(b'plain')
        self.mock_outfile.flush.assert_not_called()

    #regardless of type, always calls flush at the end
    def test_flush(self):
        stream = [b'\x1b[31mred', b'plain']
        write_stream_with_colors_win(stream, self.mock_outfile, flush=True)

        self.assertEqual(self.mock_outfile.flush.call_count, 2)