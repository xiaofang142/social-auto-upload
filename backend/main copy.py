
from flask_cors import CORS

from flask import Flask, request, jsonify, Response, render_template, send_from_directory





import os
from flask import Flask
from flask_cors import CORS
from backend.routes.file_router import file_router



# 初始化Flask应用
app = Flask(__name__)
CORS(app)
# 视图
app.register_blueprint(file_router)

if __name__ == '__main__':
    # 启动时初始化数据库
    from backend.db.createTable import init_database
    init_database()  # 执行数据库存在性检测和初始化
    app.run(debug=True)
