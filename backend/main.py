from flask_cors import CORS
from flask import Flask
from routes.material import material_router
from routes.category import category_router

active_queues = {}
app = Flask(__name__)
#跨域
CORS(app)
# 限制上传文件大小为160MB
app.config['MAX_CONTENT_LENGTH'] = 160 * 1024 * 1024
# 路由
app.register_blueprint(material_router)
app.register_blueprint(category_router)

if __name__ == '__main__':
    # 执行数据库存在性检测和初始化
    from db.init import init_database
    init_database()
    # 启动app
    app.run(host='0.0.0.0' ,port=5409,debug=True)