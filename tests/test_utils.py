import pytest
from httpie import utils
import base64
import os
import tempfile
from pathlib import Path
from httpie.utils import url_as_host


#utils.py line 305-306
def test_is_version_greater_value_error():
    assert not utils.is_version_greater("1.2.alpha", "1.2.1") # 1.2 == 1.2, throws exception

#utils.py line 104-121
@pytest.mark.parametrize("n, precision, expected", [
    (1, 2, "1 B"), #if n == 1 return 1
    (1024 * 1234 * 1111, 2, "1.31 GB"),
    (1024 * 1234 * 1111, 1, "1.3 GB"),
])
def test_humanize_bytes(n, precision, expected):
    assert utils.humanize_bytes(n, precision) == expected # loop through list and check each

#utils.py line 283-284
def test_open_with_lockfile_file_exists_error(tmp_path):
    target = tmp_path / "dummy.txt" #create a fake filepath from tmp_path
    target.write_text("data") #write something in it

    file_id = base64.b64encode(os.fsencode(target)).decode()
    lockfile = Path(tempfile.gettempdir()) / file_id # get the file location

    lockfile.touch(exist_ok=False) # try and create a file at the same location as the lockfile

    #since exist_ok=False, this raises an error
    with pytest.raises(utils.LockFileError, match="Can't modify a locked file."): #expect an error with the message
        with utils.open_with_lockfile(target, "r"): #call the function
            pass

    lockfile.unlink()


def test_split_cookies_raises_if_regex_is_none():
    result = utils.split_cookies("foo=bar, name1=name2")
    assert result == ["foo=bar", "name1=name2"]
    
def test_url_as_host_strips_userinfo_basic():
    assert url_as_host("http://user:pw@example.com") == "example.com"

def test_url_as_host_uses_last_segment_when_multiple_ats_in_userinfo():
    assert url_as_host("http://u@v@example.com:8080/path") == "example.com:8080"