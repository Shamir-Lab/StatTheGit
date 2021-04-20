# StatTheGit4TAU Python Code to Maintain Statistics for GitHub Repositories in TAU's bioinformatic groups

## What is StatTheGit
StatTheGit4TAU is a python based tool to fetch, maintain and display GitHub clone and views statistics. 

This project was forked from [StatTheGit](https://medium.com/@aqeel.anwar/maintaining-github-stats-for-more-than-14-days-31653bd1d7e1?sk=0d4a7e0c1b21df8a6e715719109dcecc) repo.

A detailed documentation of the original one and can be found [here](https://medium.com/@aqeel.anwar/maintaining-github-stats-for-more-than-14-days-31653bd1d7e1?sk=0d4a7e0c1b21df8a6e715719109dcecc)

## How to use StatTheGit:

### Clone the repository
```
git clone https://github.com/Shamir-Lab/StatTheGit
```

### Install required packages
```
cd StatTheGit
pip install -r requirements.txt
```

### Fetch the stats
```
python fetch_stats.py --git_token_file <GitToken> --username <GitHub Username> --repo_names <Repository name>
```

#### Options/flags:
* `--git_token_file` A file that contains GitHub personal access token
* `--username` The Github username
* `--namespace` The Github namespace in which projects reside. can also be identical to username
* `--repo_names` Lastest date to include for clones and views
* end_date


Running fetch_stats.py will create a folder `repo_stats/<-namespace->`. The view and clone stats for the mentioned repositories will be fetched from the GitHub profile and saved as a csv file. If the csv files for the repository already exists the code appends the fetched data to existing stats taking care of issues such as duplicate stats, missing dates etc.

**Note that Github saves only statistics of the last 14 days. To avoid loss of information, you need to run `fetch_stats.py` at least every 14 days (e.g. by using a cronjob). We recommend to run `fetch_stats.py` every 3-4 days, to avoid a scenario in which statistics were not collected due to a server fault (e.g. server was down).**    

```
# Generic
|-- repo_stats
|    |-- <namespace>
|    |    |-- <repository 1>.txt
|    |    |-- <repository 2>.txt
|    |    |-- <repository 3>.txt


# Example
|-- repo_stats
|    |-- Shamir-Lab
|    |    |-- DOMINO.txt
|    |    |-- SCAPP.txt
```

### Display the stats
The original StatTheGit can be used to create and update online graphs which can then be displayed on your personal website [like this](http://www.aqeel-anwar.com/#GitHubStat).

This functionality exists in this project, **but was never tested**

#### Offline graphs and reports:
You can generate a summarizing table in a csv format, and a plots that tracks (unique) views and clones through time.

#### Options/flags:
* `--stat_folder` Folder to the GitHub stat csvs
* `--display_type` Plot display functionality: could be **off** for no plots at all (generates table report only), **offline** for a static html-based plotly figure, and **online** for online html that can be embedded in an existing website using Plotly. **This functionality Was never been tested for StatTheGit4TAU**
* `--start_date` Ealiest date to include for clones and views
* `--end_date` Lastest date to include for clones and views
* end_date


```
python display_stats.py --stat_folder repo_stats --display_type 'offline' --start_date --end_date "2021-01-01" --end_date "2021-02-01" 
```

Running the above command will generate one interactive graph per repository displaying the views and clones statistics.

#### Online Graphs:
Plotly is being used to plot the Github graphs. In order to create the graphs online, and have it displayed on your website, chart studio account needs to be created [Details here](https://medium.com/@aqeel.anwar/maintaining-github-stats-for-more-than-14-days-31653bd1d7e1?sk=0d4a7e0c1b21df8a6e715719109dcecc). Once you have the API key you can use the following commands to create online graphs that can then be shared on websites.
```
python display_stats.py --stat_folder repo_stats --display_type 'online' --username <plotly-username> --api_key <plotly-api-key
```
