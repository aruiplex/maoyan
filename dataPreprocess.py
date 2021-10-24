import json
import os
import pandas as pd


movie_files = os.listdir("./movies/")
movies = []


for movie_file in movie_files:
    with open(f"./movies/{movie_file}") as fd:
        movie = json.load(fd)
        movies.append(movie)


with open("./top100_list_name") as fd:
    ranking = eval(fd.read())


def add_ranking():
    d = {x["name_zh"]: x for x in movies}
    for index, name in enumerate(ranking):
        try:
            d[name]["ranking"] = index
        except KeyError as e:
            print(f"{e} did not apparent in the movies details.")

    return d


movies_dict = add_ranking()


df = pd.DataFrame(movies)
# df.reset_index("name_zh") # reset the index from integer to name_zh

with open("MaoYanTop100.csv", "w") as fd:
    fd.write(df.to_csv())
