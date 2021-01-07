import importlib

class DB:
    '''数据库模块选择'''
    def __init__(self, db_module, db_name):
        self.__db_module = self.dynamic_import(db_module)
        self.__db_name = db_name

    '''动态导入模块'''
    def dynamic_import(self, module):
        return importlib.import_module(module)

    '''获取查询结果，返回[{key:value}]'''
    def select_data(self, sql):
        with self.__db_module.connect(self.__db_name) as conn:
            c = conn.cursor()
            cursor = c.execute(sql)
            col_name_list = [tuple[0] for tuple in cursor.description]
            res = map(lambda x: dict(zip(col_name_list, x)), list(cursor))
            return res

    '''插入数据'''
    def insert_data(self, table_name, data, sql):
        colum, value = '', ''
        for k,v in data.items():
            if v == None or v == '' or v == 'None' or k == 'id':
                continue
            colum += '%s,' % (k)
            if isinstance(v, int):
                value += '%d,' % (v)
            elif isinstance(v, str) :
                value += '"%s",' % (v)
            else:
                value += '"%s",' % (str(v))
        colum = colum[0:-1]
        value = value[0:-1]
        insert_sql = "insert into '%s' (%s) VALUES (%s)"
        with self.__db_module.connect(self.__db_name) as conn:
            c = conn.cursor()
            cursor = c.execute(insert_sql % (table_name, colum, value))
            conn.commit()
            return cursor.lastrowid

    def execute_sql(self, file):
        import re
        sqlist = []
        with open(file, encoding='utf-8', mode='r') as f:
            sqlist = f.read().split(';')[:-1]
        with self.__db_module.connect(self.__db_name) as conn:
            c = conn.cursor()
            for s in sqlist:
                s = re.sub(r'\n\s*', '', s)
                s = re.sub(r'\s+', ' ', s)
                s += ';'
                c.execute(s)
            conn.commit()

    def create_table(self, sql):
        with self.__db_module.connect(self.__db_name) as conn:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()

if __name__ == '__main__':
    db = DB('sqlite3', 'my_fund.db')
    db.execute_sql('./db.sql')