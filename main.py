from util import get_table

def test():
    recent_days = 30
    churn_search_repos_final = get_table('churn_search_repos_final', recent_days) # get_table 方法在 util.py 文件中, 需提前 from relative_path/util import get_table
    repo_issue = get_table('repo_issue', recent_days)
    repo_issue_comment = get_table('repo_issue_comment', recent_days)
    repo_pull = get_table('repo_pull', recent_days)
    repo_pull_merged = get_table('repo_pull_merged', recent_days)
    repo_review_comment = get_table('repo_review_comment', recent_days)

    print('churn_search_repos_final: {} records in total within {} days'.format(len(churn_search_repos_final), recent_days))
    print(churn_search_repos_final[0].keys())
    print(churn_search_repos_final[:2])
    print('\n')

    print('repo_issue: {} records in total within {} days'.format(len(repo_issue), recent_days))
    print(repo_issue[0].keys())
    print(repo_issue[:2])
    print('\n')
    print('repo_issue_comment: {} records in total within {} days'.format(len(repo_issue_comment), recent_days))
    print(repo_issue_comment[0].keys())
    print(repo_issue_comment[:2])
    print('\n')

    print('repo_pull: {} records in total within {} days'.format(len(repo_pull), recent_days))
    print(repo_pull[0].keys())
    print(repo_pull[:2])
    print('\n')
    print('repo_pull_merged: {} records in total within {} days'.format(len(repo_pull_merged), recent_days))
    print(repo_pull_merged[0].keys())
    print(repo_pull_merged[:2])
    print('\n')
    print('repo_review_comment: {} records in total within {} days'.format(len(repo_review_comment), recent_days))
    print(repo_review_comment[0].keys())
    print(repo_review_comment[:2])
    print('\n')

if __name__ == '__main__':
    test() # Only used to test whether the data transformation works well.
    
    # todo: Call the data preprocess here

    # todo: Call the model training here, should add a paras to control whether to re-train or not

    # todo: Call the model prediction periodically here

    # todo: Return the prediction result here

    