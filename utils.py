import xml.etree.ElementTree as ET


def validate_sdf_file(sdf_file):
    # check that the sdf file is valid xml

    try:
        root = ET.fromstring(sdf_file)
    except ET.ParseError:
        print(ET.ParseError)
        return False
    return True


def parse_gpt_output(output):
    """parse the output of the GPT model to get the sdf file
    he output is generally as follow

    Here is your file
    ```xml
    <sdf version="1.6">
    ....
    ...
    ```

    I added a few boxes and something something
    """
    # split the output by the first occurence of ```  or ```xml to get the sdf file
    split = output.split("```")
    sdf_file = split[1]
    # remove first line
    sdf_file = "\n".join(sdf_file.split("\n")[1:])
    explanation = split[2]
    # return the sdf file
    return sdf_file, explanation
