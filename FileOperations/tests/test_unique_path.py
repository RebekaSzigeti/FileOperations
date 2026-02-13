from fileops.organizer import FileOrganizer


def test_get_unique_path_returns_same_if_not_exists(tmp_path):
    organizer = FileOrganizer(str(tmp_path), configFile = "config.json")
    file_path = tmp_path / "example.txt"
    result = organizer.get_unique_path(str(file_path))
    assert result == str(file_path)



def test_get_unique_path_adds_suffix_if_exists(tmp_path):
    organizer = FileOrganizer(str(tmp_path), configFile = "config.json")
    file_path = tmp_path / "example.txt"
    file_path.write_text("data")
    result = organizer.get_unique_path(str(file_path))
    assert result.endswith("example_1.txt")




def test_get_unique_path_increments_properly(tmp_path):
    organizer = FileOrganizer(str(tmp_path), configFile = "config.json")
    file_path = tmp_path / "example.txt"
    file_path.write_text("data")
    (tmp_path / "example_1.txt").write_text("data")
    result = organizer.get_unique_path(str(file_path))
    assert result.endswith("example_2.txt")



 


