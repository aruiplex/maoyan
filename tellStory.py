import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import OrderedDict
from scipy.optimize import curve_fit
import seaborn as sns


class AnalysisMaoYan():

    def __init__(self) -> None:
        self.df = pd.read_csv("MaoYanTop100.csv")
        self.df_clean = self.df.loc[self.df["money"] != -1]
        plt.rc('font', family='Sarasa Gothic CL')
        # sns.set_theme(style="darkgrid")

    # def clean_df(self):

    def actors_rank_all(self):
        actor_times = {}
        for actors in self.df["actors"]:
            for actor in eval(actors):
                if actor in actor_times:
                    actor_times[actor] += 1
                else:
                    actor_times[actor] = 1
        return OrderedDict(sorted(actor_times.items(), key=lambda i: i[1], reverse=True))

    def sub(self, m0: dict, m1: dict):
        """subtruct two dict, ignore m1 unique element. This will change m1.

        Args:
            m0 (dict)
            m1 (dict)
        """
        for i in m0:
            if i in m1:
                m0[i] -= m1[i]

    def actors_rank_major(self):

        actor_times = {}
        for actors in self.df["actors"]:
            for actor in eval(actors)[:5]:
                if actor in actor_times:
                    actor_times[actor] += 1
                else:
                    actor_times[actor] = 1

        self.sub(actor_times, self.directors_rank())

        return OrderedDict(sorted(actor_times.items(), key=lambda i: i[1], reverse=True))

    def directors_rank(self):
        directors_times = {}
        for directors in self.df["director"]:
            if directors in directors_times:
                directors_times[directors] += 1
            else:
                directors_times[directors] = 1
        return OrderedDict(sorted(directors_times.items(), key=lambda i: i[1], reverse=True))

    def category_rank(self):
        category_times = {}
        for categorys_movies in self.df["categorys"]:
            for category in eval(categorys_movies):
                if category in category_times:
                    category_times[category] += 1
                else:
                    category_times[category] = 1
        return sorted(category_times.items(), key=lambda i: i[1], reverse=True)

    def duration_distrubtion(self):
        durations = np.array(sorted([int(x[:-2])
                             for x in self.df["duration"]]))

        return durations

    def good_time(self):
        months = [x[5:7] for x in self.df["date"]]
        years = [x[:4] for x in self.df["date"]]
        return months, years

    def rate_num_distrubtion(self):
        rate_num = [x for x in self.df["rate_num"]]
        return rate_num

    def plot_types_pie(self):
        a = np.array(self.category_rank())
        x = list(a[:, 0])
        y = np.array(a[:, 1], dtype=int)
        colors = ['yellowgreen', 'red', 'gold', 'lightskyblue', 'white', 'lightcoral',
                  'blue', 'pink', 'darkgreen', 'yellow', 'grey', 'violet', 'magenta', 'cyan']
        porcent = 100.*y/y.sum()
        patches, texts = plt.pie(y, colors=colors, startangle=90, radius=1.2)
        labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(x, porcent)]
        patches, labels, dummy = zip(*sorted(zip(patches, labels, y),
                                             key=lambda x: x[2],
                                             reverse=True))
        # plt.rc('font', family='Sarasa Gothic CL')
        plt.legend(patches, labels, bbox_to_anchor=(-0.1, 1))

        print(labels)
        plt.show()

    def plot_money_rate(self):
        vs = np.array([self.df_clean["money"], self.df_clean["rate"]],
                      dtype=(float, int)).T
        vs = np.sort(vs)
        # income
        x = vs[:, 1]
        # rate
        y = vs[:, 0]
        fig, ax = plt.subplots()

        params = np.polyfit(x, y, 2)
        xp = np.linspace(x.min(), x.max(), 20)
        yp = np.polyval(params, xp)
        plt.plot(xp, yp, 'k', alpha=0.8, linewidth=1)
        # plt.xticks(x, np.exp(x))
        ax.scatter(x, y, marker="o", alpha=0.5)

        ax.set(xlabel='Income (¥)', ylabel='Rating',
               title='The relationship between movies income against rating.')
        ax.grid()
        plt.show()

    def plot_money_rate_avg(self):
        vs = np.array([self.df_clean["rate"], self.df_clean["money"]]).T
        l = {}
        for x in vs:
            if x[0] in l:
                l[x[0]].append(x[1])
            else:
                l[x[0]] = [x[1]]

        for i in l:
            l[i] = np.average(l[i])

        print(l)
        vs = np.array(list(l.items()))
        vs = np.sort(vs)
        x = vs[:, 1]
        y = vs[:, 0]

        fig, ax = plt.subplots()

        params = np.polyfit(x, y, 2)
        xp = np.linspace(x.min(), x.max(), 20)
        yp = np.polyval(params, xp)
        plt.plot(xp, yp, 'k', alpha=0.8, linewidth=1)
        # plt.xticks(x, np.exp(x))
        ax.scatter(x, y, marker="o", alpha=0.5)
        sig = np.std(y - np.polyval(params, x))
        plt.fill_between(xp, yp - sig, yp + sig,
                         color='k', alpha=0.2)
        ax.set(xlabel='Income (¥)', ylabel='Rating',
               title='The relationship between movies income against rating.')
        ax.grid()
        plt.show()

    def income_director(self):
        # vs = dict self.df_clean["director"], self.df_clean["money"]
        vs = {}
        for index, i in self.df_clean.iterrows():
            if i["director"] in vs:
                vs[i["director"]].append(i["money"])
            else:
                vs[i["director"]] = [i["money"]]

        for i in vs:
            vs[i] = np.average(vs[i])

        vs = [[x[0], int(x[1])] for x in vs.items()]
        vs = sorted(vs, key=lambda x: x[1])
        vs = np.array(vs)
        x = vs[:, 0]
        y = vs[:, 1].astype(float)

        fig, ax = plt.subplots()
        # plt.xticks(x, np.exp(x))
        ax.scatter(x, y, marker="o", alpha=0.5)
        ax.set(xlabel='Director', ylabel='Income (¥)',
               title='movies income against director.')
        ax.grid()
        fig.autofmt_xdate()
        plt.show()
        print(vs)

    def plot_type_director(self):
        vs = {}
        for index, i in self.df.iterrows():
            if i["director"] in vs:
                vs[i["director"]].extend(eval(i["categorys"]))
            else:
                vs[i["director"]] = eval(i["categorys"])

        vs = [[x[0], x[1]] for x in vs.items()]
        vs = sorted(vs, key=lambda x: len(x[1]), reverse=True)[:9]
        print(vs)
        fig1, axs = plt.subplots(3, 3)

        for i, ax in zip(vs, axs.ravel()):
            name = i[0]
            types = i[1]
            d = {}
            for t in types:
                if t in d:
                    d[t] += 1
                else:
                    d[t] = 1
            v = np.array(list(d.items()))
            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            labels = v[:, 0]
            sizes = v[:, 1]
            # only "explode" the 2nd slice (i.e. 'Hogs')
            # explode = (0, 0.1, 0, 0)

            ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                   shadow=True, startangle=90)
            ax.set_title(name)
            # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.axis('equal')

        plt.show()


a = AnalysisMaoYan()
a.plot_type_director()
# print(a.df_clean)


def plot_his(x, y):
    num_bins = 10
    weight_bins = np.zeros(num_bins)
    interval = (x.max()-x.min())/num_bins
    for i in x:
        index = int((i - x.min()) // interval)
        weight_bins[index] += 1

    fig, ax = plt.subplots()

    # the histogram of the data
    n, bins, patches = ax.hist(x, num_bins, density=True)

    # add a 'best fit' line
    y = weight_bins
    # ax.plot(x, y, '--')
    ax.set_xlabel('rate number')
    ax.set_ylabel('number of rate number')
    # ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.show()
