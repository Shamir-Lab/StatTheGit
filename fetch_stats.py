from github import Github
import datetime
import csv
from collections import OrderedDict
from shutil import copy2
import os
from tqdm import tqdm
import argparse
from aux_functions import display_StatTheGit


# Command-line input setup
parser = argparse.ArgumentParser(
    description="StatTheGit - Maintain GitHub repository stats for more than 14 days"
)
parser.add_argument(
    "--git_token_file",
    type=str,
    default="access_token.txt",
    help="GitHub token to your profile",
)
parser.add_argument(
    "--username", type=str, default="hag007", help="GitHub Username",
)
parser.add_argument(
    "--namespace", type=str, default="Shamir-Lab", help="GitHub Namespace",
)
parser.add_argument(
    "--repo_names",
    type=str,
    default='all', # ['EMP', 'DOMINO', 'SCAPP', 'MONET', 'MSP_UHS', 'PRODIGY', 'EMP-benchmark',  'Logrank-Inaccuracies', 'Multi-Omics-Cancer-Benchmark','PlasClass', 'Recycler', 'NEMO','CT-FOCS', 'DOCKS','Karyotype-reconstruction','SPRINT', 'Sorting-Cancer-Karyotypes', 'FOCS', 'ADEPTUS-2.0','GENEPARK', 'Faucet', 'BARCODE']
    nargs="+",
    help="Name of repositories seperated by space. Leave it empty and all the repositories will be serviced",
)


if __name__ == "__main__":
    # Parse the command line
    display_StatTheGit()
    args = parser.parse_args()
    g = Github(open(args.git_token_file).read().strip())
    repo_names = []
    # Check the repositories
    if "all" not in args.repo_names:
        # repo_names.append(args.repo_names)
        repo_names = args.repo_names
        print(repo_names)
    else:
        for repo in g.get_user().get_repos():
            repo_full_name = repo._full_name.value
            if args.namespace == repo_full_name.split("/")[0]:
                repo_name = repo_full_name.split("/")[1]
                repo_names.append(repo_name)

    for repo_n in tqdm(repo_names):
        # Process each repository
        repo_str = args.namespace + "/" + repo_n
        print("Processing: ", repo_n)
        repo = g.get_repo(repo_str)

        # Get repository clones statistics
        clone_stat = repo.get_clones_traffic()
        clone_stat = clone_stat["clones"]

        # Get repository views statistics
        traffic_stat = repo.get_views_traffic()
        print(traffic_stat)
        traffic_stat = traffic_stat["views"]

        # Get repository commits statistics
        commit_stat = repo.get_commits()
        commits=[a.raw_data['commit']['author']['date'].split('T')[0].split(' ')[0] for a in list(commit_stat)]
        earliest_commit_date=commits[0]

        # Get URL
        repo_url = repo.html_url

        # The stats fetched from GitHub packaged has date missing where the clones/views are zero.
        # The following lines appends missing dates and orders them.

        if len(clone_stat) > 0 or True:
            print(clone_stat)
            print(traffic_stat)
            # Find the earliest date between the views and clones
            if len(traffic_stat) > 0:
                earliest_exposure_date=traffic_stat[0].timestamp.date()
                if len(clone_stat) > 0 and traffic_stat[0].timestamp.date() > clone_stat[0].timestamp.date():
                    earliest_exposure_date = clone_stat[0].timestamp.date()

            else:
                earliest_exposure_date=datetime.datetime.strptime("1970-01-01", '%Y-%m-%d').date()
            date_array = []
            clone_array = {}
            traffic_array = {}

            # Generate array of dates under consideration
            for d in range(14):
                latest_date = str(earliest_exposure_date + datetime.timedelta(days=d))
                # Assign zeros to clone and views statistics
                clone_array[latest_date] = 0
                traffic_array[latest_date] = 0

            # Populate the clone statistics for the available date.
            # For unavailable dates, the stat is already initialized to zero
            for c in clone_stat:
                clone_array[str(c.timestamp.date())] = c.uniques

            for v in traffic_stat:
                traffic_array[str(v.timestamp.date())] = v.uniques

            # Create the folder of username if it doesn't exists
            path_to_folder = "repo_stats/" + args.username
            if not os.path.exists(path_to_folder):
                os.makedirs(path_to_folder)

            exposure_csv_str = os.path.join("repo_stats", repo_str.split("/")[0], "exposure", repo_str.split("/")[1] + ".txt")
            exposure_csv_str_temp = os.path.join("repo_stats", repo_str.split("/")[0], "exposure", repo_str.split("/")[1] + "_temp.txt")
            commits_csv_str = os.path.join("repo_stats", repo_str.split("/")[0], "commits", repo_str.split("/")[1] + ".txt")
            commits_csv_str_temp = os.path.join("repo_stats", repo_str.split("/")[0], "commits", repo_str.split("/")[1] + "_temp.txt")
            url_csv_str = os.path.join("repo_stats", repo_str.split("/")[0], "urls", repo_str.split("/")[1] + ".txt")

            # Save the stat file as another temp file.
            if os.path.exists(exposure_csv_str):
                s = copy2(exposure_csv_str, exposure_csv_str_temp)
            if os.path.exists(commits_csv_str):
                s = copy2(commits_csv_str, commits_csv_str_temp)

            # Create CSV file.
            try:
                os.makedirs(os.path.dirname(exposure_csv_str))
            except:
                pass
            try:
                os.makedirs(os.path.dirname(commits_csv_str))
            except:
                pass
            try:
                os.makedirs(os.path.dirname(url_csv_str))
            except:
                pass

            exposure_csv_file = open(exposure_csv_str, "w")
            exposure_writer = csv.writer(exposure_csv_file)
            commits_csv_file = open(commits_csv_str, "w")
            commits_writer = csv.writer(commits_csv_file)

            # Define header of the CSV file
            exposure_writer.writerow(["Date", "Clones", "Traffic"])
            commits_writer.writerow(["Commits"])

            clone_array = OrderedDict(sorted(clone_array.items(), key=lambda t: t[0]))
            traffic_array = OrderedDict(sorted(traffic_array.items(), key=lambda t: t[0]))

            if os.path.exists(exposure_csv_str_temp):
                # copyfile(csv_str, csv_str_temp)
                cc = 1
                with open(exposure_csv_str_temp) as exposure_csv_file:
                    csv_reader = csv.reader(exposure_csv_file, delimiter=",")
                    line_count = 0
                    for row in csv_reader:
                        if line_count > 0:
                            datetime_obj = datetime.datetime.strptime(
                                row[0], "%Y-%m-%d"
                            ).date()
                            compare_date = datetime.datetime.strptime(
                                str(earliest_exposure_date), "%Y-%m-%d"
                            ).date()

                            if datetime_obj < compare_date or compare_date < datetime.datetime.strptime("1970-01-30", "%Y-%m-%d").date():
                                exposure_writer.writerow([row[0], row[1], row[2]])
                            else:
                                break
                        line_count += 1

            if os.path.exists(commits_csv_str_temp):
                # copyfile(csv_str, csv_str_temp)
                cc = 1
                with open(commits_csv_str_temp) as commits_csv_file:
                    csv_reader = csv.reader(commits_csv_file, delimiter=",")
                    line_count = 0
                    for row in csv_reader:
                        if line_count > 0:
                            datetime_obj = datetime.datetime.strptime(
                                row[0], "%Y-%m-%d"
                            ).date()
                            compare_date = datetime.datetime.strptime(
                                str(earliest_commit_date), "%Y-%m-%d"
                            ).date()

                            if datetime_obj < compare_date or compare_date < datetime.datetime.strptime("1970-01-30", "%Y-%m-%d").date():
                                commits_writer.writerow([row[0]])
                            else:
                                break
                        line_count += 1

            compare_date = datetime.datetime.strptime(str(earliest_exposure_date), "%Y-%m-%d").date()
            first_date= datetime.datetime.strptime("1970-01-30", "%Y-%m-%d").date()
            if compare_date>first_date or not os.path.exists(exposure_csv_str_temp):
                for (key_clone, value_clone), (key_traffic, value_traffic) in zip(
                    clone_array.items(), traffic_array.items()
                ):
                    exposure_writer.writerow([key_clone, value_clone, value_traffic])

                exposure_csv_file.close()

            for commit in commits:
                commits_writer.writerow([commit])

            commits_csv_file.close()

            exposure_csv_file = open(exposure_csv_str_temp, "w")
            exposure_writer = csv.writer(exposure_csv_file)
            exposure_writer.writerow(["Date", "Clones", "Traffic"])
            with open(exposure_csv_str) as exposure_csv_file:
                csv_reader = csv.reader(exposure_csv_file, delimiter=",")
                for row in csv_reader:
                    exposure_writer.writerow([row[0], row[1], row[2]])
            exposure_csv_file.close()

            commits_csv_file = open(commits_csv_str_temp, "w")
            commits_writer = csv.writer(commits_csv_file)
            commits_writer.writerow(["Commits"])
            with open(commits_csv_str) as commits_csv_file:
                csv_reader = csv.reader(commits_csv_file, delimiter=",")
                for row in csv_reader:
                    commits_writer.writerow([row[0]])
            commits_csv_file.close()

            url_csv_file = open(url_csv_str, "w")
            url_writer = csv.writer(url_csv_file)
            with open(url_csv_str) as url_csv_file:
                    url_writer.writerow(["URL"])
                    url_writer.writerow([repo_url])
            url_csv_file.close()

            # Remove temp file.
            os.remove(exposure_csv_str_temp)
            os.remove(commits_csv_str_temp)


