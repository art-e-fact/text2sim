from utils import validate_sdf_file


def test_is_valid_sdf():
    with open("outputs/world_file.sdf", "r") as f:
        assert validate_sdf_file(f.read()) is True
