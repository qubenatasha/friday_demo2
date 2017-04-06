#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['FRIDAY_DEMO2_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['FRIDAY_DEMO2_MONGOALCHEMY_SERVER'] = ''
    os.environ['FRIDAY_DEMO2_MONGOALCHEMY_PORT'] = ''
    os.environ['FRIDAY_DEMO2_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.friday_demo2 import friday_demo2
    from qube.src.services.friday_demo2service import friday_demo2Service
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, friday_demo2ServiceError


class Testfriday_demo2Service(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.friday_demo2Service = friday_demo2Service(context)
        self.friday_demo2_api_model = self.createTestModelData()
        self.friday_demo2_data = self.setupDatabaseRecords(self.friday_demo2_api_model)
        self.friday_demo2_someoneelses = \
            self.setupDatabaseRecords(self.friday_demo2_api_model)
        self.friday_demo2_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.friday_demo2_someoneelses.save()
        self.friday_demo2_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.friday_demo2_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.friday_demo2_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, friday_demo2_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            friday_demo2_data = friday_demo2(name='test_record')
            for key in friday_demo2_api_model:
                friday_demo2_data.__setattr__(key, friday_demo2_api_model[key])

            friday_demo2_data.description = 'my short description'
            friday_demo2_data.tenantId = "23432523452345"
            friday_demo2_data.orgId = "987656789765670"
            friday_demo2_data.createdBy = "1009009009988"
            friday_demo2_data.modifiedBy = "1009009009988"
            friday_demo2_data.createDate = str(int(time.time()))
            friday_demo2_data.modifiedDate = str(int(time.time()))
            friday_demo2_data.save()
            return friday_demo2_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_friday_demo2(self, *args, **kwargs):
        result = self.friday_demo2Service.save(self.friday_demo2_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.friday_demo2_api_model['name'])
        friday_demo2.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_friday_demo2(self, *args, **kwargs):
        self.friday_demo2_api_model['name'] = 'modified for put'
        id_to_find = str(self.friday_demo2_data.mongo_id)
        result = self.friday_demo2Service.update(
            self.friday_demo2_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.friday_demo2_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_friday_demo2_description(self, *args, **kwargs):
        self.friday_demo2_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.friday_demo2_data.mongo_id)
        result = self.friday_demo2Service.update(
            self.friday_demo2_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.friday_demo2_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_friday_demo2_item(self, *args, **kwargs):
        id_to_find = str(self.friday_demo2_data.mongo_id)
        result = self.friday_demo2Service.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_friday_demo2_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(friday_demo2ServiceError):
            self.friday_demo2Service.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_friday_demo2_list(self, *args, **kwargs):
        result_collection = self.friday_demo2Service.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.friday_demo2_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.friday_demo2_data.mongo_id)
        with self.assertRaises(friday_demo2ServiceError) as ex:
            self.friday_demo2Service.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.friday_demo2_data.mongo_id)
        self.friday_demo2Service.auth_context.is_system_user = True
        self.friday_demo2Service.delete(id_to_delete)
        with self.assertRaises(friday_demo2ServiceError) as ex:
            self.friday_demo2Service.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.friday_demo2Service.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.friday_demo2_someoneelses.mongo_id)
        with self.assertRaises(friday_demo2ServiceError):
            self.friday_demo2Service.delete(id_to_delete)
