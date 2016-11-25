# README

Add the csv to the ./data/ folder

Use example_preprocess to pickle a preprocessed version of the data:
e.g. `python example_preprocess.py plover_river_delta.csv plover_river_delta.pkl --cols 3 4`
This will save a file called `plover_river_delta.pkl` to the `preprocessed_data/` folder.

Subsequently, you can load the data as follows:
e.g. `python example_script.py plover_river_delta.pkl`
