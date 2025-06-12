from flask import Blueprint, request, jsonify, Response
from queue import Queue
import threading
from conf import BASE_DIR
import sqlite3
from myUtils.login import get_tencent_cookie, douyin_cookie_gen, get_ks_cookie, xiaohongshu_cookie_gen

# 定义账号管理蓝图，设置URL前缀为/account
account_bp = Blueprint('account', __name__, url_prefix='/account')

@account_bp.route('/delete', methods=['GET'])
def delete_account():
    # ... existing code ...（保留原delete_account函数的完整实现）

@account_bp.route('/login')
def login():
    # ... existing code ...（保留原login函数的完整实现）

def sse_stream(status_queue):
    # ... existing code ...（保留原sse_stream函数的完整实现）

def run_async_function(type, id, status_queue):
    # ... existing code ...（保留原run_async_function函数的完整实现）