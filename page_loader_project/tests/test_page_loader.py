import tempfile
import requests_mock
from page_loader_project.page_loader import download, get_file_name


def test_name():
    assert get_file_name('https://ru.hexlet.io') == 'ru-hexlet-io.html'


def test_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = download('https://ru.hexlet.io', tmpdir)
        assert path == tmpdir + '/ru-hexlet-io.html'


def test_file():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='data')
        with tempfile.TemporaryDirectory() as tmpdir:
            x = download('http://test.com', tmpdir)
            expected = open('page_loader_project/tests/fixtures/'
                            'expected.html').read()
            current = open(x).read()
            assert expected == current
