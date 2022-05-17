from open_search import get_index_content
import data_transformation


def get_table(table_name, recent_days):
    if table_name == 'churn_search_repos_final':
        # Get the related data from OpenSeaerch
        churn_search_repos_final = get_index_content('gitee_repo-raw', recent_days, ["data.full_name", "data.id", "data.created_at"])
        # Raw data schema transformation
        churn_search_repos_final = data_transformation.churn_search_repos_final_format(churn_search_repos_final)

        return churn_search_repos_final

    elif table_name == 'repo_issue' or table_name == 'repo_issue_comment':
        repo_issue_and_repo_issue_comment = get_index_content('gitee_issues-raw', recent_days, ["data.repository.id", "data.id", "data.number", "data.created_at", "data.user.id", "data.issue_state", "data.comments_data.id", "data.comments_data.created_at", "data.comments_data.user.id"])  # author_association，该字段可暂时不使用，但我这里要留个位置。
        repo_issue, repo_issue_comment = data_transformation.repo_issue_and_repo_issue_comment_format(repo_issue_and_repo_issue_comment)

        if table_name == 'repo_issue':
            return repo_issue
        else:
            return repo_issue_comment

    elif table_name == 'repo_pull' or table_name == 'repo_pull_merged' or table_name == 'repo_review_comment':
        repo_pull_and_repo_pull_merged_and_repo_review_comment = get_index_content('gitee_pulls-raw', recent_days, ["data.base.repo.id", "data.id", "data.number", "data.created_at", "data.merged_at", "data.state", "data.user.id", "data.review_comments_data.id", "data.review_comments_data.created_at", "data.review_comments_data.user.id"])
        repo_pull, repo_pull_merged, repo_review_comment = data_transformation.repo_pull_and_repo_pull_merged_and_repo_review_comment_format(repo_pull_and_repo_pull_merged_and_repo_review_comment)

        if table_name == 'repo_pull':
            return repo_pull
        elif table_name == 'repo_pull_merged':
            return repo_pull_merged
        else:
            return repo_review_comment
    
    # repo_review = # Gitee里似乎没有review数据，暂时放弃这部分数据，模型训练时也可以先剔除这部分数据
    # repo_commit # 在OpenSearch中未找到，暂时不使用
    # repo_commit_comment # 在OpenSearch中未找到，暂时不使用
    # repo_star # 模型训练和预测暂时不需要repo_star数据
    # repo_fork # 模型训练和预测暂时不需要repo_fork数据
    # user_data # user_data的数据暂时和模型无关，但通过此表可以将user_id对应到具体的用户login

    return None

if __name__ == '__main__':
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