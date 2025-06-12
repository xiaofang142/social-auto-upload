from flask import Blueprint, request, jsonify, send_from_directory
from pathlib import Path
import uuid
import os
from db.sqlite import SQLiteDB


material_router = Blueprint('material', __name__, url_prefix='/material')
@material_router.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"code":400,"msg": "No file part in the request","data":None})

    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"code":400,"No selected file": "o file part in the request","data":None})
    # 获取表单中的自定义文件名（可选）
    custom_filename = request.form.get('filename', None)
    if custom_filename:
        filename = custom_filename + "." + file.filename.split('.')[-1]
    else:
        filename = file.filename

    category_id = request.form.get('category_id', None)
    if not category_id:
        return jsonify({"code":400,"msg": "category_id is empty","data":None})

    try:
        # 生成 UUID v1
        uuid_v1 = uuid.uuid1()
        BASE_DIR = Path(__file__).resolve().parent.parent

        # 构造文件名和路径
        final_filename = f"{uuid_v1}_{filename}"
        filepath = Path(BASE_DIR / "files" / f"{uuid_v1}_{filename}")
        # 保存文件
        file.save(filepath)

        with SQLiteDB() as db:
            insert_sql = "INSERT INTO file (filename, filesize, filepath,category_id) VALUES (?, ?, ?,?)"
            db.execute(insert_sql, (filename, round(float(os.path.getsize(filepath)) / (1024 * 1024),2), final_filename,category_id))
            db.commit()
        return jsonify({"code":200,"msg": "success","data":None})
    except Exception as e:
        return jsonify({"code":400,"msg": e,"data":None})
@material_router.route('/deleted', methods=['GET'])
def deleted():
    file_id = request.args.get('id')

    if not file_id or not file_id.isdigit():
        return jsonify({"code": 400,"msg": "Invalid or missing file ID", "data": None})

    try:
        # 获取数据库连接
        with SQLiteDB() as db:
            # 查询要删除的记录
            results = db.query("SELECT * FROM file WHERE id = ?", (file_id,))
            record = results[0]
            if not results:
                return jsonify({"code": 404, "msg": "File not found", "data": None})


            # 删除数据库记录
            db.execute("DELETE FROM file WHERE id = ?", (file_id,))
            db.commit()

        return jsonify({"code": 200,"msg": "ok", "data": { "id": record['id'],"filename": record['filename'] }})

    except Exception as e:
        return jsonify({ "code": 500,"msg": str(e), "data": None})
@material_router.route('/list', methods=['GET'])
def list():
    try:
        # 使用 with 自动管理数据库连接
        with SQLiteDB() as db:
            # 查询所有记录
            list = db.query("SELECT * FROM file")


        return jsonify({ "code": 200,"msg": "success", "data": list})
    except Exception as e:
        return jsonify({"code": 500, "msg": str("get file failed!"),"data": None })

@material_router.route('/preview', methods=['GET'])
def preview():
    # 获取 filename 参数
    filename = request.args.get('filename')

    if not filename:
        return {"error": "filename is required"}, 400

    # 防止路径穿越攻击
    if '..' in filename or filename.startswith('/'):
        return {"error": "Invalid filename"}, 400

    BASE_DIR = Path(__file__).resolve().parent.parent

    # 构造文件名和路径
    filepath = Path(BASE_DIR / "files" )

    # 返回文件
    return send_from_directory(filepath,filename)