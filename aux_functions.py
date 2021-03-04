import os
import plotly.graph_objects as go
import chart_studio.plotly as py
from plotly.subplots import make_subplots
import plotly
plotly.io.orca.config.executable="/usr/local/bin/orca"
import plotly.io._orca
import retrying
unwrapped = plotly.io._orca.request_image_with_retrying.__wrapped__
wrapped = retrying.retry(wait_random_min=1000)(unwrapped)
plotly.io._orca.request_image_with_retrying = wrapped

ORANGE = "#DD8047"
BLUE = "94B6D2"
GREEN = "#A5AB81"
YELLOW = "#D8B25C"

def plot_stat(xs, ys, repo_names, title="Shamir-Lab", data="Clones", type="offline"):

    try:
        os.makedirs("plots")
    except Exception as e:
        pass

    print("start start plotting...")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for x,y,repo_name in zip(xs, ys, repo_names):
        fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=repo_name,
            # color="darkred",
            line=dict(width=3),
            marker=dict(size=10),
        ),
        secondary_y=False,
    )


    fig.update_layout(
        title=f'{title} (n={len(repo_names)}); {data}',
        font=dict(color="#7f7f7f"),
        autosize=True,
        legend=dict(x=0, y=1, orientation="v"),
        margin=dict(l=0, r=0, t=40, b=30),
    )
    if type == "offline":
        # fig.write_image("summary.png")
        fig.write_html(f"plots/git_stat_{title}_{data}.html")
        print("saved summary!")
    elif type == "online":
        url = py.plot(fig, filename=repo_name, sharing="public")
        print(url)


def display_StatTheGit():
    with open("display.txt", "r") as file:
        for line in file:
            print(line, end="")
