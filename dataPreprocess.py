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
    for index, name in enumerate(ranking):
        for m in movies:
            if m["name_zh"] == name:
                m["ranking"] = index 
                break

add_ranking()

df = pd.DataFrame(movies)

with open("MaoYanTop100.csv", "w") as fd:
    fd.write(df.to_csv())
