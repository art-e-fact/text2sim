from utils import parse_gpt_output, validate_sdf_file


def test_parse_gpt_output():
    non_tagged_output = ("Here is your file\n"
    "\n"
    "```\n"
    "<?xml version=\"1.0\" ?>\n"
    "<sdf version=\"1.6\">\n"
    "</sdf>\n"
    "```\n"
    "\n"
    "I added a few boxes and something something")
    print(non_tagged_output)
    sdf_file, explanation = parse_gpt_output(non_tagged_output)
    print(sdf_file)
    assert validate_sdf_file(sdf_file) == True

    tagged_output = ("Here is your file\n"
    "\n"
    "```xml\n"
    "<?xml version=\"1.0\" ?>\n"
    "<sdf version=\"1.6\">\n"
    "</sdf>\n"
    "```\n"
    "\n"
    "I added a few boxes and something something")
    sdf_file, explanation = parse_gpt_output(tagged_output)
    assert validate_sdf_file(sdf_file) == True


