# README

Add the csv to the ./data/ folder

Use **pickle_csv.py** to pickle a preprocessed version of the data:
e.g. `python pickle_cv.py plover_river_delta.csv plover_river_delta.pkl`
This will save a file called `plover_river_delta.pkl` to the `preprocessed_data/` folder.

Subsequently, you can load the data as is done in **example_script.py**:
e.g. `python example_script.py plover_river_delta.pkl`

Have a look at **main** in **example_script.py** to see how you might work with the loaded data, use interpolation, etc.
