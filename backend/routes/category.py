from flask import Blueprint, request, jsonify, send_from_directory
from db.sqlite import SQLiteDB


category_router = Blueprint('category', __name__, url_prefix='/category')
# 增加查询category 列表 新增 删除api
@category_router.route('list', methods=['GET'])
def list():
    # 从数据库查询
    results = []
    with SQLiteDB() as db:
        query_sql = "SELECT * FROM category WHERE status = ?"
        results = db.query(query_sql, (1,))
    return jsonify({"code":200,"msg": "success","data":results})
@category_router.route('/add', methods=['POST'])
def add():
    # 接收name 
    data = request.get_json()

    # 从JSON数据中提取fileList和accountList
    name = data.get('name','')
    # 为空的话返回错误
    if not name :
        return jsonify({"code":400,"msg": "name is empty","data":None})
    # 判断是否已经存在
    with SQLiteDB() as db:
        query_sql = "SELECT * FROM category WHERE name = ?"
        results = db.query(query_sql, (name,))
        if results:
            return jsonify({"code":400,"msg": "name already exists","data":None})
    with SQLiteDB() as db:
        insert_sql = "INSERT INTO category (name,status) VALUES (?,?)"
        db.execute(insert_sql, (name,1))
        db.commit()
    return jsonify({"code":200,"msg": "success","data":None})
@category_router.route('/delete', methods=['POST'])
def delete():
    # 接收id
    id = int(request.args.get('id'))
    with SQLiteDB() as db:
        delete_sql = "DELETE FROM category WHERE id = ?"
        db.execute(delete_sql, (id,))
        db.commit()
    return jsonify({"code":200,"msg": "success","data":None})
