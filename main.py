from data_preprocess.preprocess import prediction_data_preprocess, get_existed_prediction_data
from joblib import dump, load
from collections import Counter
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/developer-churn-prediction')

# todo: Call the model training here, should add a paras to control whether to re-train or not

# data preprocess here
repo_ids = os.environ.get('REPO_IDS', [8649239])
period_length = os.environ.get('PEIROD_LENGTH', 120)
churn_limit_weeks = os.environ.get('CHURN_LIMIT_WEEKS', 14)
time_threshold_days = os.environ.get('TIME_THRESHOLD_DAYS', 28)

for repo_id in repo_ids:
    # model prediction periodically here
    train_data_dir = './data_preprocess/train_data'
    prediction_data_dir = './data_preprocess/prediction_data'

    # 生成预测数据集，并返回
    user_id_list,input_data = prediction_data_preprocess(repo_id,train_data_dir,prediction_data_dir,
                                                         period_length,churn_limit_weeks,time_threshold_days)
    print(user_id_list)
    print(input_data)

    prediction_file = prediction_data_dir+'/repo_'+str(repo_id)+'/normalized_data'
    # 根据生成的预测数据集文件，直接返回数据
    user_id_list,input_data = get_existed_prediction_data(prediction_file)
    print(len(user_id_list))
    print(input_data.shape)

    # 加载训练好的模型，对input_data进行预测
    # model_path = './prediction_models/xgboost_models/2022-06-03_15-16-04xgboost_best_model_roc_auc-120-0.0.joblib'
    model_path = './prediction_models/xgboost_models/2022-06-03_15-16-04xgboost_best_model_roc_auc-120-0.0.joblib'
    # model_path = './prediction_models/rf_models/2022-06-03_15-11-48rf_best_model_roc_auc-120-0.0.joblib'
    # model_path = './prediction_models/adaboost_models/2022-06-03_15-15-13adaboost_best_model_roc_auc-120-0.0.joblib'
    # model_path = './prediction_models/svm_models/2022-06-03_15-06-53svm_best_model_roc_auc-120-0.0.joblib'
    model = load(model_path)
    y_pred = model.predict(input_data)

    # Return the prediction result here
    for i in range(len(user_id_list)):
        print(user_id_list[i],'\t\t',y_pred[i])
    print(Counter(y_pred))

    