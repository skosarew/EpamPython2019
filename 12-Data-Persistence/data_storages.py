import json
import pickle
import psycopg2
import pymongo


class MyStorage:
    """
    Base class for different storage types.
    """
    @staticmethod
    def check_exec_serial(serialization, json_f, pickle_f):
        """
        Checks serialization type
        :param serialization:
        :param json_f: function for interaction with storage
        :param pickle_f: function for interaction with storage
        :return:
        """
        if serialization == 'json':
            return json_f()
        elif serialization == 'pickle':
            return pickle_f()
        else:
            raise Exception('unknown serialization parameter')

    def get(self, serialization, input_path):
        pass

    def set(self, inp_obj, serialization, out_f):
        pass


class FileStorage(MyStorage):
    def get(self, serialization, out_f):
        def json_f():
            with open(out_f, 'r') as f:
                data = json.load(f)
            return data

        def pickle_f():
            with open(out_f, 'rb') as f:
                data = pickle.load(f)
            return data

        return self.check_exec_serial(serialization, json_f, pickle_f)

    def set(self, inp_obj, serialization, out_f):
        def json_f():
            with open(out_f, 'w') as f:
                json.dump(inp_obj, f)

        def pickle_f():
            with open(out_f, 'wb') as f:
                pickle.dump(inp_obj, f)

        self.check_exec_serial(serialization, json_f, pickle_f)


class PostgresStorage(MyStorage):
    """
    Class creates connection with Postgres database and save data in out_table
    which contains one row.
    """
    def __init__(self, postgres_conn):
        self.postgres_conn = postgres_conn

    def get(self, serialization, out_table):
        conn = psycopg2.connect(**self.postgres_conn)

        def json_f():
            cur = conn.cursor()
            cur.execute(
                f"SELECT c_json from {out_table}")
            rows = cur.fetchone()[0]
            cur.close()
            conn.commit()
            conn.close()
            return rows

        def pickle_f():
            cur = conn.cursor()
            cur.execute(
                f"SELECT c_pickle from {out_table}")
            rows = cur.fetchone()[0]
            cur.close()
            conn.commit()
            conn.close()
            return pickle.loads(rows)

        return self.check_exec_serial(serialization, json_f, pickle_f)

    def set(self, inp_obj, serialization, out_table):
        conn = psycopg2.connect(**self.postgres_conn)

        def json_f():
            cur = conn.cursor()
            cur.execute(
                f"""CREATE TABLE if not exists {out_table} 
                (id INT GENERATED BY DEFAULT AS IDENTITY,
                 c_json json)
                """)
            cur.execute(f"DELETE FROM {out_table}")
            cur.execute(
                """INSERT INTO {1} (  c_json ) VALUES ( '{0}' ) """.format(
                    json.dumps(inp_obj), out_table))
            cur.close()
            conn.commit()
            conn.close()

        def pickle_f():
            cur = conn.cursor()
            cur.execute(f"""CREATE TABLE if not exists {out_table} 
                       (id INT GENERATED BY DEFAULT AS IDENTITY, c_pickle bytea)
                       """)
            cur.execute(f"DELETE FROM {out_table}")
            pickle_obj = pickle.dumps(inp_obj)
            cur.execute(f'''INSERT INTO {out_table}  (c_pickle) VALUES (%s)''',
                        (pickle_obj,))
            cur.close()
            conn.commit()
            conn.close()

        self.check_exec_serial(serialization, json_f, pickle_f)


class MongoStorage(MyStorage):
    """
    Class creates connection with Mongo database and save data in out_table
    which contains one row.
    """
    def __init__(self, mongo_connection):
        self.mongo_connection = mongo_connection
        self.my_database = mongo_connection.epam

    def get(self, serialization, out_table):
        def json_f():
            json_collection = self.my_database[out_table]
            unserial = list(json_collection.find())[0]['json_serial']
            return json.loads(unserial)

        def pickle_f():
            pickle_collection = self.my_database[out_table]
            unserial = list(pickle_collection.find())[0]['pickle_serial']
            return pickle.loads(unserial)

        return self.check_exec_serial(serialization, json_f, pickle_f)

    def set(self, inp_obj, serialization, out_table):
        def json_f():
            json_collection = self.my_database[out_table]
            json_collection.delete_one({})
            json_collection.insert_one(
                {"json_serial": json.dumps(inp_obj)})

        def pickle_f():
            pickle_collection = self.my_database[out_table]
            pickle_collection.delete_one({})
            pickle_collection.insert_one(
                {"pickle_serial": pickle.dumps(inp_obj)})

        self.check_exec_serial(serialization, json_f, pickle_f)
