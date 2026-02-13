from fileops.deleter import FileDeleter
import os

def test_dry_test_does_not_actually_delete(tmp_path):
    deleter = FileDeleter(str(tmp_path), "example", dry_run = True)
    file_path  = os.path.join(str(tmp_path), "example.txt")
    with open(file_path, "w") as f:
        f.write("data")

    deleter.delete_files()

    assert os.path.exists(file_path)
    assert deleter.deleted_count==1



def test_force_actually_deletes(tmp_path):
    deleter = FileDeleter(str(tmp_path), "example", force = True)
    file_path  = os.path.join(str(tmp_path), "example.txt")
    with open(file_path, "w") as f:
        f.write("data")

    deleter.delete_files()

    assert not os.path.exists(file_path)
    assert deleter.deleted_count==1

    

def test_force_true_does_not_call_input(tmp_path, monkeypatch):
      deleter = FileDeleter(str(tmp_path), "example", force = True)
      file_path = os.path.join(str(tmp_path), "example.txt")
      with open(file_path, "w") as f:
          f.write("data")

      def mock_input(*args, **kwargs):
          raise AssertionError("input() should not be called")
      
      monkeypatch.setattr("builtins.input",mock_input)

      deleter.delete_files()

      assert not os.path.exists(file_path)
      assert deleter.deleted_count==1
