import tempfile
import requests_mock
from os.path import exists
from page_loader_project.page_loader import download, get_file_name


def test_name():
    assert get_file_name('https://ru.hexlet.io') == 'ru-hexlet-io.html'
    assert get_file_name('https://vk.com') == 'vk-com.html'


def test_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = download('https://ru.hexlet.io', tmpdir)
        assert path == tmpdir + '/ru-hexlet-io.html'


def test_download_html():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='data')
        with tempfile.TemporaryDirectory() as tmpdir:
            x = download('http://test.com', tmpdir)
            expected = open('page_loader_project/tests/fixtures/'
                            'expected.html').read()
            current = open(x).read()
            assert expected == current


def test_download_pics():
    with requests_mock.Mocker() as m:
        text = open('page_loader_project/tests/fixtures/pic.html').read()
        m.get('http://test.com/picture', text=text)
        pic = open('page_loader_project/tests/fixtures/some/beautiful/pic.png', 'rb').read()
        m.get('http://test.com/picture/some/beautiful/pic.png', content=pic)
        second_pic = open('page_loader_project/tests/fixtures/pic.jpg', 'rb').read()
        m.get('http://test.com/picture/pic.jpg', content=second_pic)
        expected_pic = open('page_loader_project/tests/fixtures/expected_pic.html', 'r').read()
        with tempfile.TemporaryDirectory() as tmpdirname:
            download('http://test.com/picture', tmpdirname)
            current = open(tmpdirname + '/test-com-picture.html').read()
            new_dir = tmpdirname + "/test-com-picture_files"
            new_file = new_dir + "/test-com-picture-some-beautiful-pic.png"
            new_file1 = new_dir + "/test-com-picture-pic.jpg"
            assert exists(new_dir)
            # assert exists(new_file)
            # assert exists(new_file1)
            assert expected_pic == current
