import os
from organizer import FileOrganizer

def test_txt_file_goes_to_plaintext(tmp_path):
    organizer = FileOrganizer(str(tmp_path), configFile = "config.json")
    file_path = os.path.join(tmp_path, "example.txt")

    with open(file_path, "w") as f:
        f.write("data")

    organizer.run()
    new_path = os.path.join(tmp_path, "PLAINTEXT", "example.txt")
    assert os.path.exists(new_path)



def test_unrecognized_file_goes_to_other(tmp_path):
    organizer = FileOrganizer(str(tmp_path), configFile = "config.json")
    file_path = os.path.join(str(tmp_path), "example.abc")

    with open(file_path, "w") as f:
        f.write("data")

    organizer.run()
    new_path = os.path.join(tmp_path, "OTHER", "example.abc")
    assert os.path.exists(new_path)


def test_file_without_extension_goes_to_other(tmp_path):
    organizer = FileOrganizer(str(tmp_path), configFile = "config.json")
    file_path = os.path.join(str(tmp_path), "example")

    with open(file_path, "w") as f:
        f.write("data")

    organizer.run()
    new_path = os.path.join(tmp_path, "OTHER", "example")
    assert os.path.exists(new_path)