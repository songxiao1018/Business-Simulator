# python
from flask import Flask, request, jsonify
import sqlite3
import time
import random
from contextlib import closing

app = Flask(__name__)


def server_init(db_path='db/server.db'):
    """
    Initialize the database and create the 'users' table if it does not exist.

    :param db_path: Path to the SQLite database file.
    """
    # Use a context manager to ensure the connection is properly closed even if an error occurs
    with closing(sqlite3.connect(db_path)) as root_conn:
        # Use the same context manager for the cursor to simplify the code
        with closing(root_conn.cursor()) as root_cursor:
            # Check if the table exists before creating it to avoid raising an exception
            root_cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            table_exists = root_cursor.fetchone()
            if not table_exists:
                create_users_table_query = '''
                    CREATE TABLE IF NOT EXISTS users
                    (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL, 
                        password TEXT NOT NULL, 
                        email TEXT
                    )
                '''
                root_cursor.execute(create_users_table_query)
                root_conn.commit()  # Commit the transaction only if a change was made (table created)

            # Check if the table exists before creating it to avoid raising an exception
            root_cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='chat';")
            table_exists = root_cursor.fetchone()
            if not table_exists:
                create_users_table_query = '''
                    CREATE TABLE IF NOT EXISTS chat
                    (
                        id TEXT NOT NULL,
                        message TEXT NOT NULL,
                        time TEXT NOT NULL
                    )
                '''
                root_cursor.execute(create_users_table_query)
                root_conn.commit()  # Commit the transaction only if a change was made (table created)

            # Check if the table exists before creating it to avoid raising an exception
            root_cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='beer_user';")
            table_exists = root_cursor.fetchone()
            if not table_exists:
                create_users_table_query = '''
                    CREATE TABLE IF NOT EXISTS beer_user
                    (
                        id TEXT NOT NULL,
                        group_id TEXT NOT NULL,
                        group_user TEXT NOT NULL,
                        is_start INT
                    )
                '''
                root_cursor.execute(create_users_table_query)
                root_conn.commit()

            # 啤酒制造商
            # Check if the table exists before creating it to avoid raising an exception
            root_cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='beer_data';")
            table_exists = root_cursor.fetchone()
            if not table_exists:
                create_users_table_query = '''
                    CREATE TABLE IF NOT EXISTS beer_data
                    (
                        time TEXT ,
                        id TEXT NOT NULL,
                        group_id TEXT NOT NULL,
                        group_user TEXT NOT NULL,
                        
                        week TEXT NOT NULL,  
                        DingHuoA INT,  
                        FaHuoA   INT, 
                        QianHuoA INT,
                        DingHuoB INT,  
                        FaHuoB   INT,  
                        QianHuoB INT,
                        
                        ChuQiKuCun INT,
                        
                        SongHuo INT,  
                        QianHuo INT,  
                        DingHuo INT,
                        
                        QiMoKuCun INT,
                        
                        BenQiLiRun INT
                    )
                '''
                root_cursor.execute(create_users_table_query)
                root_conn.commit()


@app.route('/connect_test', methods=['POST'])
def connect_test():
    return jsonify({"status": "连接成功！"}), 200


@app.route('/create_chat', methods=['POST'])
def create_chat():
    try:
        data = request.get_json()

        # 确保所需的字段存在
        if 'message' not in data or 'id' not in data:
            return jsonify({"status": "缺少必要参数"}), 400

        id = data['id']
        message = data['message']
        timestep = str(int(time.time()))

        with closing(sqlite3.connect('db/server.db')) as conn, closing(conn.cursor()) as c:
            chat = (id, message, timestep)
            c.execute("INSERT INTO chat (id, message, time) VALUES (?, ?, ?)", chat)
            conn.commit()

        return jsonify({"status": "成功发送消息！"}), 201

    except Exception as e:
        # 错误日志记录（生产环境中非常重要）
        app.logger.error(f"An error occurred while creating chat: {str(e)}")
        return jsonify({"status": "服务器错误！"}), 500


@app.route('/get_chat', methods=['POST'])
def get_chat():
    data = request.get_json()

    with closing(sqlite3.connect('db/server.db')) as conn, closing(conn.cursor()) as c:

        # 编写SQL查询语句，获取my_table表中最新的10条记录
        sql_query = """
        SELECT * FROM chat ORDER BY time DESC LIMIT 500;
        """

        # 执行查询
        c.execute(sql_query)

        # 获取所有查询结果
        last_ten_rows = c.fetchall()

        message_list = []  # 改为列表，更直观地表示消息列表

        for row in last_ten_rows:
            user_id = row[0]
            sql_query = """
            SELECT username FROM users WHERE id = ?;
            """

            # 确保c是有效的游标实例
            c.execute(sql_query, (user_id,))

            # 获取查询结果，增加错误处理
            username_result = c.fetchone()
            if username_result is None:
                print(f"Warning: No user found with ID {user_id}. Skipping this message.")
                continue  # 跳过此次循环，继续处理下一行

            username = username_result[0]

            # 直接将每条消息作为一个字典添加到列表中
            message_list.append({
                'name': username,
                'time': row[2],  # 确保这是时间戳字段的正确索引
                'message': row[1],
            })

        # 现在message_list包含了最后十行消息的详细信息

    return jsonify(message_list), 201


@app.route('/create_count', methods=['POST'])
def create_count():
    try:
        data = request.get_json()

        # 确保所需的字段存在
        if 'name' not in data or 'password' not in data or 'email' not in data:
            return jsonify({"status": "缺少必要参数！"}), 400

        username = data['name']
        password = data['password']
        email = data['email']

        with closing(sqlite3.connect('db/server.db')) as conn, closing(conn.cursor()) as c:

            # 仅需一次查询即可验证用户名是否存在
            # query = "SELECT * FROM users WHERE username = ? OR password = ?"
            query = " SELECT username FROM users WHERE username = ?;"
            c.execute(query, (username,))
            match = c.fetchone()

            if match:
                print(f"用户名 '{username}' 已存在。")
                return jsonify({'status': '用户名已存在！'}), 200
            else:
                print(f"用户名 '{username}' 不存在继续登录检查。")

                user = (username, password, email)
                c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", user)
                conn.commit()

                return jsonify({"status": "创建用户成功！"}), 201

    except Exception as e:
        # 错误日志记录（生产环境中非常重要）
        app.logger.error(f"An error occurred while creating user: {str(e)}")
        return jsonify({"status": "内部错误"}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username_to_check = data.get('name')
        password_to_check = data.get('password')

        if not username_to_check or not password_to_check:
            return jsonify({'status': '缺少必要参数', 'id': None}), 400

        with closing(sqlite3.connect('db/server.db')) as conn, closing(conn.cursor()) as c:
            # 仅需一次查询即可验证用户名和密码
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            c.execute(query, (username_to_check, password_to_check))
            match = c.fetchone()
            
            print(match)

            if match:
                print(f"用户名 '{username_to_check}' 存在且密码匹配。")
                return jsonify({'status': '登录成功', 'id': match[0]}), 200
            else:
                print(f"用户名 '{username_to_check}' 不存在或密码不匹配。")
                return jsonify({'status': '用户名或密码错误', 'id': None}), 401

    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        return jsonify({'status': '数据库错误', 'id': None}), 500
    except Exception as e:
        print(f"发生错误: {e}")
        return jsonify({'status': '内部错误', 'id': None}), 500


@app.route('/beer_login', methods=['POST'])
def beer_login():
    try:
        data = request.get_json()
        id = data.get('id')
        group_id = data.get('group_id')
        group_user = data.get('group_user')

        if not id or not group_id or not group_user:
            return jsonify({'status': '缺少必要参数', 'id': None}), 400

        with closing(sqlite3.connect('db/server.db')) as conn, closing(conn.cursor()) as c:
            # 仅需一次查询即可验证用户名和密码
            query = "SELECT * FROM beer_user WHERE group_id = ?"
            c.execute(query, (group_id,))
            match = c.fetchone()

            if match:
                print(f"该组 '{group_id}' 已存在。")
            else:
                print(f"该组 '{group_id}' 不存在。")

                id_init = str(int(random.random() * 1000000000))
                group_id_init = str(group_id)
                group_user_init_list = ['市场A', '市场B', '市场C', '市场D', '市场E', '市场F', '市场G', '市场H']

                for group_user_init in group_user_init_list:
                    DingHuo = 160
                    for i in range(1, 31):
                        week = str(i)

                        if i < 11:
                            DingHuo = 140 + int(random.random() * 10000000 % 20)
                        elif i < 21:
                            DingHuo = DingHuo + int(random.random() * 10000000 % 30) + 10
                        else:
                            DingHuo = DingHuo - int(random.random() * 10000000 % 30) - 10

                        if DingHuo <= 0:
                            DingHuo = 10

                        beer_data = (id_init, group_id_init, group_user_init, week, DingHuo)
                        c.execute("""INSERT INTO beer_data (id, group_id, group_user, week, DingHuo)  VALUES (?, ?, ?, ?, ?)""", beer_data)
                        conn.commit()

        with closing(sqlite3.connect('db/server.db')) as conn, closing(conn.cursor()) as c:
            # 仅需一次查询即可验证用户名和密码
            query = "SELECT * FROM beer_user WHERE group_id = ? AND group_user = ?"
            c.execute(query, (group_id, group_user))
            match = c.fetchone()

            if match:
                print(f"该组角色 '{group_user}' 已存在请重新选择。")
                return jsonify({'status': '角色已存在', 'id': match[0]}), 200
            else:
                print(f"该组角色 '{group_user}' 不存在正在创建。")

                with closing(sqlite3.connect('db/server.db')) as conn, closing(conn.cursor()) as c:
                    beer_user = (id, group_id, group_user)
                    c.execute("INSERT INTO beer_user (id, group_id, group_user) VALUES (?, ?, ?)", beer_user)
                    conn.commit()

                return jsonify({'status': '角色登录成功！', 'id': None}), 401

    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        return jsonify({'status': '数据库错误', 'id': None}), 500
    except Exception as e:
        print(f"发生错误: {e}")
        return jsonify({'status': '内部错误', 'id': None}), 500


@app.route('/beer_get_group_user', methods=['POST'])
def beer_get_group_user():
    data = request.get_json()
    get_id = data.get('id')
    get_group_id = data.get('group_id')
    get_group_user = data.get('group_user')

    with closing(sqlite3.connect('db/server.db')) as conn, closing(conn.cursor()) as c:

        # 编写SQL查询语句，获取my_table表中最新的10条记录
        sql_query = """
        SELECT * FROM beer_user DESC LIMIT 500;
        """

        # 执行查询
        c.execute(sql_query)

        # 获取所有查询结果
        last_ten_rows = c.fetchall()

        user_list = {
            'status': '查询失败',
            'timestep': str(time.time()), 
            'id': get_id,
            'group_id': get_group_id,
            'group_user': get_group_user,
            'users': 0,
            '工厂': ' ',
            '供应商A': ' ',
            '供应商B': ' ',
            '分销商A': ' ',
            '分销商B': ' ',
            '分销商C': ' ',
            '分销商D': ' ',
        }

        users = 0

        for row in last_ten_rows:
            user_id = row[0]
            group_id = row[1]
            group_user = row[2]

            print(f"user_id: {user_id}, group_id: {group_id}, group_user: {group_user}")

            if str(group_id) == str(get_group_id):
                user_list['status'] = '查询成功'

                sql_query = """
                SELECT username FROM users WHERE id = ?;
                """

                # 确保c是有效的游标实例
                c.execute(sql_query, (user_id,))

                # 获取查询结果，增加错误处理
                username_result = c.fetchone()

                if username_result is None:
                    print(f"Warning: No user found with ID {user_id}. Skipping this message.")
                    continue  # 跳过此次循环，继续处理下一行

                username = username_result[0]

                if group_user == '工厂':
                    user_list['工厂'] = username
                    users += 1
                elif group_user == '供应商A':
                    user_list['供应商A'] = username
                    users += 1
                elif group_user == '供应商B':
                    user_list['供应商B'] = username
                    users += 1
                elif group_user == '分销商A':
                    user_list['分销商A'] = username
                    users += 1
                elif group_user == '分销商B':
                    user_list['分销商B'] = username
                    users += 1
                elif group_user == '分销商C':
                    user_list['分销商C'] = username
                    users += 1
                elif group_user == '分销商D':
                    user_list['分销商D'] = username
                    users += 1
                else:
                    print(f"Warning: Unknown group_user '{group_user}'. Skipping this message.")
                    continue

        user_list['users'] = users
        if users == 7:
            # 初始化数据
            timestep = user_list['timestep']
            id = user_list['id']
            group_id = user_list['group_id']
            group_user = user_list['group_user']

            week = 0

            DingHuoA = 0
            FaHuoA   = 0
            QianHuoA = 0
            DingHuoB = 0
            FaHuoB   = 0
            QianHuoB = 0

            ChuQiKuCun = 0

            SongHuo = 0
            QianHuo = 0
            DingHuo = 0

            QiMoKuCun = 0

            BenQiLiRun = 0

            beer_data = (timestep, id, group_id, group_user, week, DingHuoA, FaHuoA, QianHuoA, DingHuoB, FaHuoB, QianHuoB, ChuQiKuCun, SongHuo, QianHuo, DingHuo, QiMoKuCun, BenQiLiRun)
            c.execute("""INSERT INTO 
                      beer_data (time, id, group_id, group_user, week, DingHuoA, FaHuoA, QianHuoA, DingHuoB, FaHuoB, QianHuoB, ChuQiKuCun, SongHuo, QianHuo, DingHuo, QiMoKuCun, BenQiLiRun)  
                      VALUES    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """, beer_data)
            conn.commit()

    return jsonify(user_list), 200


if __name__ == '__main__':
    server_init()
    app.run(host='0.0.0.0', debug=True, port="4000")  # 开启调试模式，实际部署时请关闭
