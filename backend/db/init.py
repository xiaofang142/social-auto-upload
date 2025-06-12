import sqlite3
from pathlib import Path

def init_database():
    # 获取根目录 判断 database.db 是否存在
    BASE_DIR = Path(__file__).resolve().parent

    # 定义数据库路径（根据实际项目结构调整）
    db_path = Path(BASE_DIR) / "database.db"
    
    # 检测数据库文件是否存在
    if not db_path.exists():
        print("检测到数据库不存在，开始初始化...")
        # 创建数据库连接（会自动创建文件）
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 创建文件记录表（示例表结构，根据实际需求调整）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                filesize REAL,  MB为单位
                file_path TEXT NOT NULL,
                create_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建其他业务表（如用户信息表等，根据实际需求添加）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,  -- 平台类型（如douyin/tencent等）
                cookie TEXT NOT NULL,
                userName TEXT,
                status INTEGER DEFAULT 1  -- 添加默认值（1:有效 0:失效）
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                status INTEGER）
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ 数据库初始化完成")
    else:
        print("ℹ️ 数据库已存在，无需初始化")

if __name__ == "__main__":
    init_database()