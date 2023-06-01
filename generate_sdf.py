# Generate sdf files from the dataset of gazebo fuel based on user input parsed by ChatGPT

# Import libraries
import json
import requests
import openai
import os

from utils import validate_sdf_file, parse_gpt_output

# Set OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")


user_input = "A warehouse with wood pallets and boxes"

FUEL_URL = "https://fuel.gazebosim.org/1.0/"


def query_dataset(keyword):
    # query the dataset at `FUEL_URL` with requests
    response = requests.get(FUEL_URL + "models?q=" + keyword)
    # return the json response
    return response.json()


def format_dataset(dataset):
    """
      format the dataset into a list of strings
      This is an example entry
    {
      "createdAt": "2023-02-15T18:41:41Z",
      "updatedAt": "2023-05-13T15:41:41Z",
      "name": "shelf",
      "owner": "Kavya",
      "description": "simple shelf to use in warehouse worlds",
      "likes": 1,
      "downloads": 51,
      "filesize": 2102876,
      "upload_date": "2023-02-15T18:41:40Z",
      "modify_date": "2023-02-16T02:11:48Z",
      "license_id": 5,
      "license_name": "Creative Commons Attribution Non Commercial 4.0 International",
      "license_url": "http://creativecommons.org/licenses/by-nc/4.0/",
      "license_image": "https://i.creativecommons.org/l/by-nc/4.0/88x31.png",
      "permission": 1,
      "url_name": "",
      "private": false,
      "tags": [
        "warehouse",
        "shelf"
      ],
      "categories": [
        "Architecture"
      ]
    }
    """
    formatted_dataset = []
    for entry in dataset:
        extracted = {
            "name": entry["name"],
            "owner": entry["owner"],
            "description": entry["description"],
            "tags": entry.get("tags", []) + entry.get("categories", []),
        }
        formatted_dataset.append(extracted)
    return formatted_dataset


def generate_prompt(user_input, dataset):
    prompt = f"{user_input}. Please only use assets available in the list below: {dataset}, and refer to their uri in the format `https://fuel.gazebosim.org/1.0/[model_owner]/models/[model_name]`, making sure to replace the `model_owner` and `model_name` variables. Do not create assets from primitives"
    return prompt


def generate_sdf(user_input, dataset):
    # uses openai ChatGPT to generate sdf files from the dataset based on user input

    prompt = generate_prompt(user_input, dataset)
    print(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Hello! You are GazeboGPT, a tool to generate a Gazebo .sdf world file from the user prompt. If dimensions are not specified by the user, just assume 10mx10m. As for object, just generate a reasonable amount to get a total of 5 objects. Do not ask additional questions, and just output the best xml sdf output that seems to match. It can be followed by a short description of what was generated.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    result = ""
    for choice in response.choices:
        print(choice.message.content)
        result += choice.message.content
    sdf_file = result
    # return the sdf file
    return sdf_file


if __name__ == "__main__":
    # query the fuel dataset
    dataset = query_dataset(user_input)
    with open("outputs/fuel_response.json", "w+") as json_file:
        json.dump(dataset, json_file)
    # with open("fuel_response.json") as json_file:
    #    dataset = json.load(json_file)
    # format the dataset
    dataset = format_dataset(dataset)
    # generate sdf files
    gpt_response = generate_sdf(user_input, dataset)
    # parse the sdf files
    sdf_file, explanation = parse_gpt_output(gpt_response)
    # check that the sdf file is vald xml
    valid = validate_sdf_file(sdf_file)
    # save the sdf file
    with open("outputs/world_file.sdf", "w") as f:
        f.write(sdf_file)
    # print the response
    print(explanation)
