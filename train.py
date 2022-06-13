from joblib import dump, load
import os
from data_preprocess.preprocess import train_data_preprocess,data_type_list
# from prediction_models.train_svm import *
# from prediction_models.train_adaboost import *
# from prediction_models.train_rf import *
from prediction_models.train_xgboost import *

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/developer-churn-prediction')

# data preprocess here
repo_ids = os.environ.get('REPO_IDS', [8649239])
period_length = os.environ.get('PERIOD_LENGTH', 120)
churn_limit_weeks = os.environ.get('CHURN_LIMIT_WEEKS', 14)
time_threshold_days = os.environ.get('TIME_THRESHOLD_DAYS', 28)

for repo_id in repo_ids:
    # 训练部分所需的所有路径列表
    train_data_dir = './data_preprocess/train_data' # 全部模块都需要用相对路径哈
    prediction_data_dir = './data_preprocess/prediction_data'

    # 以下参数也需要设置
    overlap_ratio = 0.0  # 负样本采样区间重合度，默认不重合。取值范围[0,1)，重合度越高，负样本越多，但不一定模型更精确
    train_end_time = '2022-01-01'  # 用于训练模型的数据均选自该时间点以前（从仓库创建开始）
    data_type_count = len(data_type_list) # 训练特征种类数
    scoring = 'roc_auc'  # grid_search时需要使用的评估指标
    model_params_dir = './prediction_models/model_params'
    prediction_work_dir = './prediction_models'

    # 数据预处理并生成训练数据集
    new_time_threshold_days = train_data_preprocess(repo_id,train_data_dir,period_length,overlap_ratio,churn_limit_weeks,
                                                train_end_time,continue_running=True,time_threshold=time_threshold_days)
    # 参数time_threshold可以是整数（天数），此时返回的new_time_threshold_days等于传入的参数；也可以是(0,1)区间的小数，表示对应百分位数。
    # 如0.8表示使用所有开发者活动时间的第80百分位数作为时间阈值，此时返回的new_time_threshold_days等于具体的第80百分位数

    # 配置模型、训练 （grid_search_control grid search控制开关）、保存模型 使用 joblib.dump
    grid_search_control = False
    # train_svm(train_data_dir, repo_id, period_length, overlap_ratio, data_type_count, scoring, grid_search_control,
    #           model_params_dir, prediction_work_dir, save_dir='./prediction_models/svm_models',if_save=True)
    # train_adaboost(train_data_dir, repo_id, period_length, overlap_ratio, data_type_count, scoring, grid_search_control,
    #           model_params_dir, prediction_work_dir, save_dir='./prediction_models/adaboost_models', if_save=True)
    # train_rf(train_data_dir, repo_id, period_length, overlap_ratio, data_type_count, scoring, grid_search_control,
    #           model_params_dir, prediction_work_dir, save_dir='./prediction_models/rf_models', if_save=True)
    train_xgboost(train_data_dir, repo_id, period_length, overlap_ratio, data_type_count, scoring, grid_search_control,
              model_params_dir, prediction_work_dir, save_dir='./prediction_models/xgboost_models', if_save=True)

    # 遗留问题：预测有部分参数应该是从训练这里获取到的，比如period_length、churn_limit_weeks、time_threshold_days等，是否需要修改main.py中的部分参数获取来源，util.py的第12/13行也需要修改获取来源。
    # period_length: 获取数据的时间跨度，手动设置，训练和预测需要一致，目前可以是120或30，后续可以根据需要修改其他值
    # churn_limit_weeks: 流失期限，需要单独获取，不能从训练过程中获取；
    # time_threshold_days: 筛选开发者的阈值。训练集和测试集需要一致。可以手动设置，比如28天；也可以在训练时根据训练集的百分位数来决定。训练模型时会返回数据
    # 最终结果应该是运行train.py时可直接训练，并把模型保存到相应位置。运行main.py时可正常预测，会将结果输入到。