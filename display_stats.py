import argparse
import datetime
import os

import numpy as np
import pandas as pd

from aux_functions import plot_stat

# Command-line input setup
parser = argparse.ArgumentParser(description="Display GitHub Stats")
parser.add_argument(
    "--username", type=str, default="", help="Chart Studio (Plotly) username",
)

parser.add_argument(
    "--namespace", type=str, default="Shamir-Lab", help="namespace",
)

parser.add_argument(
    "--api_key",
    type=str,
    default="",
    help="Chart Studio (Plotly) API Key",
)
parser.add_argument(
    "--stat_folder",
    type=str,
    default="repo_stats/Shamir-Lab",
    help="Folder to the GitHub stat csvs",
)
parser.add_argument(
    "--display_type",
    type=str,
    default="offline",
    help="Display the plots",
    choices=["off", "offline", "online"],
)

parser.add_argument(
    "--start_date",
    type=str,
    default="2021-01-01",
    help="Start date",
)

parser.add_argument(
    "--end_date",
    type=str,
    default=str(datetime.datetime.now()),
    help="End date",
)


if __name__ == "__main__":
    args = parser.parse_args()
    # chart_studio.tools.set_credentials_file(
    #     username=args.username, api_key=args.api_key
    # )
    df_report=pd.DataFrame()

    # for stat_type in ("exposure", "commits"):
    
    folder = os.path.join(args.stat_folder, "exposure")
    try:
        os.makedirs(os.path.join(args.stat_folder, "reports"))
    except Exception as e:
        pass

    figures_folder=os.path.join(args.stat_folder,'plots')

    f = []
    _, _, files = os.walk(folder).__next__()

    print(folder)
    print(os.walk(folder).__next__())

    start_date = datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(args.end_date.split(' ')[0], "%Y-%m-%d").date()

    xs=[]
    ys_clones=[]
    ys_traffic=[]
    repo_names=[]
    for file in files:
        if file.endswith(".txt") and "_temp" not in file:
            print("Processing: ", file)
            path = folder + "/" + file
            clones_in_time_interval = []
            traffic_in_time_interval = []
            date_in_time_interval =[]
            df = pd.read_csv(path)
            date = df.Date
            clones = df.Clones
            traffic = df.Traffic
            start_i=-1
            for i, j in enumerate(range(len(date))):
                d = (
                    datetime.datetime.strptime(date[j], "%Y-%m-%d")
                    .date()
                )
                if d >= start_date and start_i == -1:
                    start_i=i
                    ## If you wish each curves to start a same "start_date", even if data collection was started in a later point in time, you can uncomment the following 4 lines.
                    # if d > start_date:
                    #     date_in_time_interval.append(start_date)
                    #     clones_in_time_interval.append(0)
                    #     traffic_in_time_interval.append(0)

                if d >= start_date and d <= end_date:
                    date_in_time_interval.append(d)
                    clones_in_time_interval.append(np.sum(np.asarray(clones[start_i: j + 1], dtype=int)))
                    traffic_in_time_interval.append(np.sum(np.asarray(traffic[start_i: j + 1], dtype=int)))


            df_report.loc[os.path.splitext(file)[0], "total_views"]=0 if len(traffic_in_time_interval) == 0 else traffic_in_time_interval[-1]
            df_report.loc[os.path.splitext(file)[0], "total_clones"]=0 if len(clones_in_time_interval) == 0 else clones_in_time_interval[-1]
            xs.append(date_in_time_interval)
            ys_clones.append(clones_in_time_interval)
            ys_traffic.append(traffic_in_time_interval)
            repo_names.append(file.split(".")[0])

    plot_stat(
        xs=xs,
        ys=ys_clones,
        repo_names=repo_names,
        title=args.namespace,
        data="Clones",
        type=args.display_type,
        figures_folder=figures_folder
    )
    plot_stat(
        xs=xs,
        ys=ys_traffic,
        repo_names=repo_names,
        title=args.namespace,
        data="Views",
        type=args.display_type,
        figures_folder=figures_folder
    )

    folder = os.path.join(args.stat_folder, "commits")

    f = []
    _, _, files = os.walk(folder).__next__()

    print(folder)
    print(os.walk(folder).__next__())

    for file in files:
        if file.endswith(".txt") and "_temp" not in file:
            print("Processing: ", file)
            path = folder + "/" + file
            df = pd.read_csv(path)
            df_report.loc[os.path.splitext(file)[0],"first_commit"]=df.Commits.iloc[-1]
            df_report.loc[os.path.splitext(file)[0],"last_commit"]=df.Commits.iloc[0]

    df_report.to_csv(os.path.join(args.stat_folder, "reports","report.tsv"), sep='\t')

    folder = os.path.join(args.stat_folder, "urls")

    f = []
    _, _, files = os.walk(folder).__next__()

    print(folder)
    print(os.walk(folder).__next__())

    for file in files:
        if file.endswith(".txt") and "_temp" not in file:
            print("Processing: ", file)
            path = folder + "/" + file
            df = pd.read_csv(path)
            df_report.loc[os.path.splitext(file)[0],"URL"]=df.URL.iloc[0]

    df_report.to_csv(os.path.join(args.stat_folder, "reports","report.tsv"), sep='\t')


