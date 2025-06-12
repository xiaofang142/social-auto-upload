from flask import Blueprint, request, jsonify
from conf import BASE_DIR
from myUtils.postVideo import post_video_tencent, post_video_DouYin, post_video_ks, post_video_xhs

# 定义视频管理蓝图，设置URL前缀为/video
video_bp = Blueprint('video', __name__, url_prefix='/video')

@video_bp.route('/post', methods=['POST'])
def post_video():
    # 从JSON数据中提取fileList和accountList
    data = request.get_json()
    file_list = data.get('fileList', [])
    account_list = data.get('accountList', [])
    type = data.get('type')
    title = data.get('title')
    tags = data.get('tags')
    category = data.get('category')
    enableTimer = data.get('enableTimer')
    if category == 0:
        category = None

    videos_per_day = data.get('videosPerDay')
    daily_times = data.get('dailyTimes')
    start_days = data.get('startDays')
    
    match type:
        case 1:
            post_video_xhs(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times, start_days)
        case 2:
            post_video_tencent(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times, start_days)
        case 3:
            post_video_DouYin(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times, start_days)
        case 4:
            post_video_ks(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times, start_days)
    
    return jsonify({"code": 200, "msg": None, "data": None}), 200

@video_bp.route('/postBatch', methods=['POST'])
def post_video_batch():
    data_list = request.get_json()
    if not isinstance(data_list, list):
        return jsonify({"error": "Expected a JSON array"}), 400
    
    for data in data_list:
        file_list = data.get('fileList', [])
        account_list = data.get('accountList', [])
        type = data.get('type')
        title = data.get('title')
        tags = data.get('tags')
        category = data.get('category')
        enableTimer = data.get('enableTimer')
        if category == 0:
            category = None

        videos_per_day = data.get('videosPerDay')
        daily_times = data.get('dailyTimes')
        start_days = data.get('startDays')
        
        match type:
            case 2:
                post_video_tencent(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times, start_days)
            case 3:
                post_video_DouYin(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times, start_days)
            case 4:
                post_video_ks(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times, start_days)
    
    return jsonify({"code": 200, "msg": None, "data": None}), 200