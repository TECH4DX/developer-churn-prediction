from data_preprocess.preprocess import prediction_data_preprocess, get_existed_prediction_data
from joblib import dump, load
from collections import Counter
import os
from get_open_search.util import id_login
import csv
import time
import json

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/developer-churn-prediction')

# data preprocess here
repo_ids = os.environ.get('REPO_IDS', [8649239])
period_length = os.environ.get('PERIOD_LENGTH', 120)
churn_limit_weeks = os.environ.get('CHURN_LIMIT_WEEKS', 14)
time_threshold_days = os.environ.get('TIME_THRESHOLD_DAYS', 28)

for repo_id in repo_ids:
    train_data_dir = './data_preprocess/train_data'
    prediction_data_dir = './data_preprocess/prediction_data'

    # 生成预测数据集，并返回
    user_id_list,input_data = prediction_data_preprocess(repo_id,train_data_dir,prediction_data_dir,
                                                         period_length,churn_limit_weeks,time_threshold_days)
    # print(user_id_list)
    # print(input_data)

    prediction_file = prediction_data_dir+'/repo_'+str(repo_id)+'/normalized_data'
    
    # 根据生成的预测数据集文件，直接返回数据
    user_id_list,input_data = get_existed_prediction_data(prediction_file)
    print(len(user_id_list))
    print(input_data.shape)

    # 加载训练好的模型，对input_data进行预测
    # model_path = './prediction_models/xgboost_models/2022-06-03_15-16-04xgboost_best_model_roc_auc-120-0.0.joblib'
    model_path = './prediction_models/xgboost_models/2022-06-13_02-26-47xgboost_model.joblib'
    # model_path = './prediction_models/rf_models/2022-06-03_15-11-48rf_best_model_roc_auc-120-0.0.joblib'
    # model_path = './prediction_models/adaboost_models/2022-06-03_15-15-13adaboost_best_model_roc_auc-120-0.0.joblib'
    # model_path = './prediction_models/svm_models/2022-06-03_15-06-53svm_best_model_roc_auc-120-0.0.joblib'
    
    model = load(model_path)
    y_pred = model.predict(input_data)

    # 后续可以删掉，目前是为了预测时可跳过预处理方便测试，所以从文件中加载Gitee中用户id和用户名称的映射。
    # if len(id_login) == 0:
    #     train_fake_path = './fake_data/train.json'
    #     predict_fake_path = './fake_data/predict.json'
    #     with open(train_fake_path, 'r') as f:
    #         id_login = json.load(f)['id_login']

    # 记录结果到./output/repoid_timestamp.csv中，分3列["user_id","username","pred"]，最后一行是预测结果为0或1的数量统计。
    with open('./output/' + str(repo_id) + '_' + str(int(time.time())) + ".csv","w") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["user_id","username","pred"])
        for i in range(len(user_id_list)):
            if user_id_list[i] in id_login.keys():
                writer.writerow([user_id_list[i], id_login[user_id_list[i]], y_pred[i]])
        counter = Counter(y_pred)
        writer.writerow(['Total: {}, 0: {}, 1: {}'.format((counter[0] + counter[1]), counter[0], counter[1])])

    