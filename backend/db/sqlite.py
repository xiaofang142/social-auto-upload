import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Any

class SQLiteDB:
    def __init__(self):
        # path 当前文件的绝对路径
        BASE_DIR = Path(__file__).resolve().parent

        # 定义数据库路径（根据实际项目结构调整）
        db_path = Path(BASE_DIR) / "database.db"
        print(db_path)
        """
        初始化数据库连接
        :param db_path: 数据库文件路径（如 Path(BASE_DIR / "db" / "database.db")）
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def connect(self) -> None:
        """建立数据库连接"""
        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False,  # 允许跨线程使用（Flask多线程场景需要）
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self.cursor = self.conn.cursor()
        # 启用外键约束
        self.execute("PRAGMA foreign_keys = ON;")

    def execute(self, sql: str, params: tuple = ()) -> int:
        """
        执行非查询类SQL（增/删/改）
        :param sql: SQL语句（支持参数化）
        :param params: 参数元组
        :return: 受影响的行数
        """
        if not self.cursor:
            raise sqlite3.ProgrammingError("数据库未连接，请先调用connect()")
        
        try:
            self.cursor.execute(sql, params)
            return self.cursor.rowcount
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"SQL执行失败: {str(e)}") from e

    def query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        执行查询类SQL（查）
        :param sql: SQL语句（支持参数化）
        :param params: 参数元组
        :return: 结果列表（每条记录为字典，键为列名）
        """
        if not self.cursor:
            raise sqlite3.ProgrammingError("数据库未连接，请先调用connect()")
        
        try:
            self.cursor.execute(sql, params)
            # 获取列名
            columns = [desc[0] for desc in self.cursor.description]
            # 转换为字典列表
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            raise RuntimeError(f"SQL查询失败: {str(e)}") from e

    def commit(self) -> None:
        """提交事务"""
        if self.conn:
            self.conn.commit()

    def rollback(self) -> None:
        """回滚事务"""
        if self.conn:
            self.conn.rollback()

    def close(self) -> None:
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.cursor = None
        self.conn = None

    def __enter__(self) -> 'SQLiteDB':
        """上下文管理器：进入时自动连接"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """上下文管理器：退出时自动关闭"""
        self.close()

# 使用示例（在sau_backend.py或其他模块中调用）
if __name__ == "__main__":
    # 初始化数据库操作类
    with SQLiteDB() as db:
        # 插入示例
        # insert_sql = "INSERT INTO file_records (filename, filesize) VALUES (?, ?)"
        # affected_rows = db.execute(insert_sql, ("test.mp4", 1024.5))
        # db.commit()
        # print(f"插入成功，受影响行数: {affected_rows}")

        # 查询示例
        query_sql = "SELECT * FROM category WHERE status = ?"
        results = db.query(query_sql, (1,))
        print("查询结果:", results)