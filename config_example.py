# -*- coding: utf-8 -*-
'''
Create Date: 2023/08/03
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.1
'''

# line bot info
line_bot_api = 'your_line_bot_api'
handler = 'your_handler'

# AWS要知道大家是誰，需要類似身份帳號密碼的亂數
client_aws_access_key_id = "your_client_aws_access_key_id"
client_aws_secret_access_key = "your_client_aws_secret_access_key"
client_aws_session_token="your_client_aws_session_token"

# 模型在AWS的位置
model_arn="your_model_arn"

# 存放消費者上傳照片的桶子名
client_bucket_name="your_client_bucket_name"
client_region_name="your_client_region_name"
