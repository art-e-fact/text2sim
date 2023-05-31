# text2sim


## Usage


Generate an OpenAI API Key and export it as an `OPENAI_API_KEY` environment variable.

Install the requirements with

```
pip install -r requirements.txt
```

Update the prompt in `generate_sdf.py`

```
python generate_sdf.py
```

That's all, an sdf world file has now been generated and saved as world_file.sdf. You can try it in gazebo.

The generated worlds will use assets from [Gazebo Fuel](https://app.gazebosim.org/fuel/models)


## Running tests and environment validation


Install the additional requirements with

```
pip install -r requirements_dev.txt
```

Then:

```
python generate_sdf.py
pytest
```
