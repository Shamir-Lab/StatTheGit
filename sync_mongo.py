from github import Github
import pandas as pd
from pymongo import MongoClient
import json
from tqdm import tqdm
import os
import argparse
from pandas.errors import EmptyDataError
import datetime
import dateutil.parser 
def get_initialized_coll(db_name, coll_name, db_url='rack-shamir3.cs.tau.ac.il', db_port=27017): # 'rack-shamir3.cs.tau.ac.il'
    """ Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    client = MongoClient(db_url, db_port)
    print(client.server_info())
    db = client[db_name]
    coll = db[coll_name]
    coll.delete_many({})
    return coll


def insert_records(csv_path, repo_n):
    try:
        data = pd.read_csv(csv_path).rename(columns={"Date" : "date", "Clones" : "clones", "Traffic" : "traffic"})
        data.loc[:,"repository"]=repo_n
        data.loc[:,"date"]=data.loc[:,"date"].apply(lambda a:  dateutil.parser.isoparse(a)) # For python > 3.7 : datetime.datetime.fromisoformat(a))
        payload = data.to_dict('records') # json.loads(data.to_json(orient='records'))
        coll.insert_many(payload)
    except EmptyDataError as e:
        print(f'The file {csv_path} is empty. Skipping...')
   

if __name__=="__main__":


    # Command-line input setup
    parser = argparse.ArgumentParser(
        description="sync StatTheGit with statistics collection in Mongo"
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
       # Command-line input setup

    parser.add_argument(
        "--db_url", type=str, default='rack-shamir3.cs.tau.ac.il', help="db_url",
    )

    parser.add_argument(
        "--db_port", type=int, default=27017, help="db_port",
    )

    parser.add_argument(
        "--db_name", type=str, default='executions', help="db_name",
    )

    parser.add_argument(
        "--collection_name", type=str, default="git", help="collection_name",
    )

    parser.add_argument(
        "--package_names",
        type=str,
        default=['domino', 'plasclass', 'scapp'],
        nargs="+",
        help="Name of repositories seperated by space. Leave it empty and all the repositories will be serviced",
    )


    args = parser.parse_args()
 
    
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

    db_url = args.db_url
    db_port = args.db_port
    db_name = args.db_name
    collection_name = args.collection_name

    coll=get_initialized_coll(db_name, collection_name, db_url=db_url, db_port=db_port) # 'rack-shamir3.cs.tau.ac.il'

    for repo_n in tqdm(repo_names):
        # Process each repository
        repo_str = args.namespace + "/" + repo_n

        exposure_csv_str = os.path.join("repo_stats", repo_str.split("/")[0], "exposure", repo_str.split("/")[1] + ".txt")
        print(f'import repo {repo_n} statistics from {exposure_csv_str} to mongo')
        insert_records(exposure_csv_str, repo_n)

