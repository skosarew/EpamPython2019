import unittest
from structure import FileStorage, PostgresStorage, MongoStorage
import os
import pymongo

def get_data():
    data = {}
    data['people'] = []
    data['people'].append({
        'name': 'Scott',
        'website': 'stackabuse.com',
        'from': 'Nebraska'
    })
    data['people'].append({
        'name': 'Larry',
        'website': 'google.com',
        'from': 'Michigan'
    })
    data['people'].append({
        'name': 'Tim',
        'website': 'apple.com',
        'from': 'Alabama'
    })
    return data


class TestStorage(unittest.TestCase):
    data = get_data()

    def test_file_set(self):
        fstorage = FileStorage()
        ofile_path = 'json_file_10.txt'
        fstorage.set(self.data, 'json', ofile_path)
        self.assertTrue(os.path.exists(ofile_path))

    def test_file_get(self):
        fstorage = FileStorage()
        ofile_path = 'json_file_10.txt'
        data_file_json = fstorage.get('json', ofile_path)
        self.assertEqual(data_file_json, self.data)

    def test_postgres_set(self):
        postgres_conn = dict(database="bulldog", user="bulldog", password="",
                             host="127.0.0.1", port="5432")
        postgres_storage = PostgresStorage(postgres_conn)
        out_table = 'json_table'
        postgres_storage.set(self.data, 'json', out_table)
        data_postgres_json = postgres_storage.get('json', out_table)
        self.assertEqual(data_postgres_json, self.data)

    def test_mongo(self):
        my_client = pymongo.MongoClient(
            'mongodb+srv://bulldog:888@testcluster-blu3u.mongodb.net/test?retryWrites'
            '=true&w=majority')
        mongo_storage = MongoStorage(my_client)
        out_table = 'json_mongo'
        mongo_storage.set(self.data, 'json', out_table)
        data_mongo_json = mongo_storage.get('json', out_table)
        self.assertEqual(data_mongo_json, self.data)



