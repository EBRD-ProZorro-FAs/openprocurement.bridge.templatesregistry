# -*- coding: utf-8 -*-
import os
import unittest
from copy import deepcopy
from mock import patch, MagicMock, call
from munch import munchify
from openprocurement.bridge.templatesregistry.handlers import (
    TemplateUploaderHandler
)

tender = {
    "procurementMethod": "limited",
    "status": "active.tendering",
    "id": "1" * 32,
    "documents": [
        {
            "hash": "md5:04951bc3f8e3fe51a37912dda2665f76",
            "format": "application/pkcs7-signature",
            "url": "https://public.docs.openprocurement.org/get/940de573f6d44e639c1b592672dec3c0?KeyID=52462340&Signature=Lvq2amp3b64NBAOGLEkax64WoprseL1cwPqRQ5g9KS2LNHb8XgqWkHDB0BA8UQyRSGCvsXNqJ9D7dNVi7Ne%2FCw%253D%253D",
            "title": "sign.p7s",
            "documentOf": "tender",
            "datePublished": "2020-05-08T12:29:57.154151+03:00",
            "dateModified": "2020-05-08T12:29:57.154185+03:00",
            "relatedItem": "b7bf55c6a01a4c8d9eb3b24053f7118b",
            "id": "42e3c31bfb0e4bdf80d42d57f75df019"
        },
        {
            "hash": "md5:00001bc3f8e3fe51a37912dda2665076",
            "format": "application/msword",
            "title": "paper0000001.docx",
            "documentOf": "tender",
            "documentType": "contractProforma",
            "templateId": "paper0000001",
            "datePublished": "2020-05-08T12:29:57.154151+03:00",
            "dateModified": "2020-05-08T12:29:57.154185+03:00",
            "relatedItem": "b7bf55c6a01a4c8d9eb3b24053f7118b",
            "id": "0003c31bfb0e4bdf80d42d57f75df000"
        }
    ]
}

date_older_contract_proforma = '2020-04-08T12:29:57.154185+03:00'
date_newer_contract_proforma = '2020-06-08T12:29:57.154185+03:00'
template_docs = [
    {
        "hash": "md5:00001bc3f8e3fe51a37912dda2665076",
        "format": "application/msword",
        "documentOf": "document",
        "documentType": "contractTemplate",
        "templateId": "paper0000001",
        "datePublished": "2020-05-08T12:29:57.154151+03:00",
        "dateModified": date_older_contract_proforma,
        "relatedItem": "0003c31bfb0e4bdf80d42d57f75df000",
        "id": "1" * 32
    },
    {
        "hash": "md5:00001bc3f8e3fe51a37912dda2665076",
        "format": "application/msword",
        "documentOf": "document",
        "documentType": "contractSchema",
        "templateId": "paper0000001",
        "datePublished": "2020-05-08T12:29:57.154151+03:00",
        "dateModified": date_older_contract_proforma,
        "relatedItem": "0003c31bfb0e4bdf80d42d57f75df000",
        "id": "2" * 32
    },
    {
        "hash": "md5:00001bc3f8e3fe51a37912dda2665076",
        "format": "application/msword",
        "documentOf": "document",
        "documentType": "contractForm",
        "templateId": "paper0000001",
        "datePublished": "2020-05-08T12:29:57.154151+03:00",
        "dateModified": date_older_contract_proforma,
        "relatedItem": "0003c31bfb0e4bdf80d42d57f75df000",
        "id": "3" * 32
    },
]


def prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls):
    template_downloader = MagicMock()

    factory = MagicMock()
    factory.get_template_downloader.return_value = template_downloader
    mocked_downloader_factory_cls.return_value = factory

    mocked_client = MagicMock()

    mocked_client_cls.return_value = mocked_client
    return mocked_client, template_downloader, factory


def prepare_template_downloader_result(mocked_td):
    template_info = {
        'template': 'template',
        'scheme': 'scheme',
        'form': 'form',
    }
    mocked_td.get_template_by_id.side_effect = [
        deepcopy(template_info),
    ]
    return template_info


dir_path = os.path.dirname(__file__)
registry_path = os.path.join(dir_path, 'registry')


class TestTemplateUploaderHandler(unittest.TestCase):
    config = {
        'worker_config':
            {
                'handler_templateUploader': {
                    'resources_api_token': 'resources_api_token',
                    'resources_api_version': 'resources_api_version',
                    'resources_api_server': 'resources_api_server',
                    'resource': 'resource',
                    'output_resource': 'output_resource',
                    'DS': {
                        'host_url': 'host_url',
                        'auth_ds': 'auth_ds',
                    },
                    'template_downloader': {
                        'type': 'registry_file',
                        'registry_path': registry_path,
                        'filename': 'registry.yaml'
                    }
                },
            },
        'public_resources_api_server': 'http://localhost:6543',
        'resources_api_token': 'resources_api_token',
        'resources_api_version': 'resources_api_version',
        'resources_api_server': 'resources_api_server',
        'resource': 'resource',
    }


    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.APIResourceClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.TemplateDownloaderFactory')
    def test_init(self, mocked_downloader_factory_cls, mocked_client_cls, _):
        mocked_client, _, factory = prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls)

        handler = TemplateUploaderHandler(self.config, 'cache_db')

        self.assertEquals(handler.cache_db, 'cache_db')
        self.assertEquals(handler.handler_config, self.config['worker_config']['handler_templateUploader'])
        self.assertEquals(handler.main_config, self.config)

        self.assertEqual(mocked_client_cls.call_count, 1)
        mocked_client_cls.assert_called_with(
            key=handler.handler_config.get('resources_api_token'),
            resource=handler.handler_config['resource'],
            host_url=handler.handler_config['resources_api_server'],
            api_version=handler.handler_config['resources_api_version'],
            ds_config=handler.handler_config.get('DS', {}),
        )

        self.assertEqual(mocked_downloader_factory_cls.call_count, 1)
        self.assertEqual(factory.get_template_downloader.call_count, 1)
        factory.get_template_downloader.assert_called_with(handler.handler_config['template_downloader'])

    @patch('openprocurement.bridge.templatesregistry.handlers.BytesIO')
    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.APIResourceClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.TemplateDownloaderFactory')
    def test_api_upload_document(self, mocked_downloader_factory_cls, mocked_client_cls, _, mocked_bytesio):
        mocked_client, template_downloader, _ = prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls)

        template_info = prepare_template_downloader_result(template_downloader)

        wrapped_file = 'wrappedfile'
        mocked_bytesio.return_value = wrapped_file

        handler = TemplateUploaderHandler(self.config, 'cache_db')
        handler.process_resource(tender)

        self.assertEqual(template_downloader.get_template_by_id.call_count, 1)

        cp_doc = handler.get_contract_proforma_documents(tender)[0]
        template_downloader.get_template_by_id.assert_called_with(cp_doc['templateId'])

        calls = [
            call(template_info['template']),
            call(template_info['scheme']),
            call(template_info['form']),
        ]
        mocked_bytesio.assert_has_calls(calls, any_order=True)

        self.assertEqual(mocked_client.upload_document.call_count, 3)
        doc = tender['documents'][1]
        additional_data = {
            'documentOf': 'document',
            'relatedItem': doc['id'],
        }

        calls = [
            call(wrapped_file, tender['id'], doc_type='contractTemplate', additional_doc_data=additional_data),
            call(wrapped_file, tender['id'], doc_type='contractSchema', additional_doc_data=additional_data),
            call(wrapped_file, tender['id'], doc_type='contractForm',additional_doc_data=additional_data),
        ]
        mocked_client.upload_document.assert_has_calls(calls, any_order=True)

        self.assertEqual(mocked_client.update_document.call_count, 0)

    @patch('openprocurement.bridge.templatesregistry.handlers.BytesIO')
    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.APIResourceClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.TemplateDownloaderFactory')
    def test_api_update_all_documents(self, mocked_downloader_factory_cls, mocked_client_cls, _, mocked_bytesio):
        mocked_client, template_downloader, _ = prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls)

        template_info = prepare_template_downloader_result(template_downloader)

        custom_tender = deepcopy(tender)
        custom_tender['documents'] += template_docs

        wrapped_file = 'wrappedfile'
        mocked_bytesio.return_value = wrapped_file

        handler = TemplateUploaderHandler(self.config, 'cache_db')
        handler.process_resource(custom_tender)

        self.assertEqual(template_downloader.get_template_by_id.call_count, 1)

        cp_doc = handler.get_contract_proforma_documents(tender)[0]
        template_downloader.get_template_by_id.assert_called_with(cp_doc['templateId'])

        calls = [
            call(template_info['template']),
            call(template_info['scheme']),
            call(template_info['form']),
        ]
        mocked_bytesio.assert_has_calls(calls, any_order=True)

        self.assertEqual(mocked_client.update_document.call_count, 3)
        doc = tender['documents'][1]
        additional_data = {
            'documentOf': 'document',
            'relatedItem': doc['id'],
        }
        calls = [
            call(wrapped_file, tender['id'], template_docs[0]['id'], doc_type='contractTemplate', additional_doc_data=additional_data),
            call(wrapped_file, tender['id'], template_docs[1]['id'], doc_type='contractSchema', additional_doc_data=additional_data),
            call(wrapped_file, tender['id'], template_docs[2]['id'], doc_type='contractForm',additional_doc_data=additional_data),
        ]
        mocked_client.update_document.assert_has_calls(calls, any_order=True)
        self.assertEqual(mocked_client.upload_document.call_count, 0)

    @patch('openprocurement.bridge.templatesregistry.handlers.BytesIO')
    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.APIResourceClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.TemplateDownloaderFactory')
    def test_api_update_one_old_template(self, mocked_downloader_factory_cls, mocked_client_cls, _, mocked_bytesio):
        mocked_client, template_downloader, _ = prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls)

        template_info = prepare_template_downloader_result(template_downloader)

        custom_tender = deepcopy(tender)
        custom_template_docs = deepcopy(template_docs)
        custom_template_docs[0]['dateModified'] = date_newer_contract_proforma
        custom_template_docs[1]['dateModified'] = date_newer_contract_proforma

        custom_tender['documents'] += custom_template_docs

        wrapped_file = 'wrappedfile'
        mocked_bytesio.return_value = wrapped_file

        handler = TemplateUploaderHandler(self.config, 'cache_db')
        handler.process_resource(custom_tender)

        self.assertEqual(template_downloader.get_template_by_id.call_count, 1)

        cp_doc = handler.get_contract_proforma_documents(tender)[0]
        template_downloader.get_template_by_id.assert_called_with(cp_doc['templateId'])

        mocked_bytesio.assert_called_once_with(template_info['form'])

        self.assertEqual(mocked_client.update_document.call_count, 1)
        doc = tender['documents'][1]
        additional_data = {
            'documentOf': 'document',
            'relatedItem': doc['id'],
        }
        mocked_client.update_document.assert_called_once_with(
            wrapped_file,
            tender['id'],
            template_docs[2]['id'],
            doc_type='contractForm',
            additional_doc_data=additional_data
        )
        self.assertEqual(mocked_client.upload_document.call_count, 0)

    @patch('openprocurement.bridge.templatesregistry.handlers.BytesIO')
    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.APIResourceClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.TemplateDownloaderFactory')
    def test_api_update_missed_file(self, mocked_downloader_factory_cls, mocked_client_cls, _, mocked_bytesio):
        mocked_client, template_downloader, _ = prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls)

        template_info = prepare_template_downloader_result(template_downloader)

        custom_tender = deepcopy(tender)
        custom_template_docs = deepcopy(template_docs)
        custom_template_docs.pop(1)
        custom_template_docs[0]['dateModified'] = date_newer_contract_proforma
        custom_template_docs[1]['dateModified'] = date_newer_contract_proforma
        custom_tender['documents'] += custom_template_docs

        wrapped_file = 'wrappedfile'
        mocked_bytesio.return_value = wrapped_file

        handler = TemplateUploaderHandler(self.config, 'cache_db')
        handler.process_resource(custom_tender)

        self.assertEqual(template_downloader.get_template_by_id.call_count, 1)

        cp_doc = handler.get_contract_proforma_documents(tender)[0]
        template_downloader.get_template_by_id.assert_called_with(cp_doc['templateId'])

        mocked_bytesio.assert_called_once_with(template_info['scheme'])

        self.assertEqual(mocked_client.upload_document.call_count, 1)
        doc = tender['documents'][1]
        additional_data = {
            'documentOf': 'document',
            'relatedItem': doc['id'],
        }
        mocked_client.upload_document.assert_called_once_with(
            wrapped_file,
            tender['id'],
            doc_type='contractSchema',
            additional_doc_data=additional_data
        )
        self.assertEqual(mocked_client.update_document.call_count, 0)

    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.APIResourceClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.TemplateDownloaderFactory')
    def test_api_update_for_old_contract_proforma(self, mocked_downloader_factory_cls, mocked_client_cls, _):
        mocked_client, template_downloader, _ = prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls)

        prepare_template_downloader_result(template_downloader)

        custom_tender = deepcopy(tender)
        custom_template_docs = deepcopy(template_docs)
        custom_template_docs[0]['dateModified'] = date_newer_contract_proforma
        custom_template_docs[1]['dateModified'] = date_newer_contract_proforma
        custom_template_docs[2]['dateModified'] = date_newer_contract_proforma
        custom_tender['documents'] += custom_template_docs

        handler = TemplateUploaderHandler(self.config, 'cache_db')
        handler.process_resource(custom_tender)

        self.assertEqual(template_downloader.get_template_by_id.call_count, 1)
        self.assertEqual(mocked_client.update_document.call_count, 0)
        self.assertEqual(mocked_client.upload_document.call_count, 0)

    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.APIResourceClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.TemplateDownloaderFactory')
    def test_get_contract_proforma_document(self, mocked_downloader_factory_cls, mocked_client_cls, _):
        mocked_client, template_downloader, _ = prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls)
        handler = TemplateUploaderHandler(self.config, 'cache_db')

        test_data = {
            'documents': [
                {
                    'field1': 'field1',
                    'documentType': 'notContractProforma'
                },
                {
                    'field2': 'field2',
                    'documentType': 'contractProforma'
                },
                {
                    'field3': 'field3',
                    'documentType': 'contractProforma'
                }
            ]
        }
        docs = handler.get_contract_proforma_documents(test_data)
        self.assertEqual(len(docs), 2)
        self.assertEqual(docs[0], test_data['documents'][1])
        self.assertEqual(docs[1], test_data['documents'][2])

    @patch('openprocurement.bridge.templatesregistry.handlers.BytesIO')
    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.APIResourceClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.TemplateDownloaderFactory')
    def test_upload_document_to_api(self, mocked_downloader_factory_cls, mocked_client_cls, _, mocked_bytesio):
        mocked_client, template_downloader, _ = prepare_mocks_handler_mocks(mocked_client_cls,
                                                                            mocked_downloader_factory_cls)
        handler = TemplateUploaderHandler(self.config, 'cache_db')

        doc = {
                'data': {
                    'id': 'someid',
                    'some': 'field'
                }
            }
        doc = munchify(doc)
        mocked_client.upload_document.return_value = deepcopy(doc)

        test_resource = {
            'id': 'resource_id'
        }
        test_doc = {
            'id': 'doc_id'
        }
        test_file = 'test_file'
        wrapped_file = 'wrappedfile'
        mocked_bytesio.return_value = wrapped_file

        handler._upload_document_to_api(test_resource, test_doc, test_file, 'test_doc_type')

        mocked_bytesio.assert_called_with(test_file)

        additional_data = {
            'documentOf': 'document',
            'relatedItem': test_doc['id'],
        }
        mocked_client.upload_document.assert_called_once_with(
            wrapped_file,
            test_resource['id'],
            doc_type='test_doc_type',
            additional_doc_data=additional_data
        )

    @patch('openprocurement.bridge.templatesregistry.handlers.BytesIO')
    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.APIResourceClient')
    @patch('openprocurement.bridge.templatesregistry.handlers.TemplateDownloaderFactory')
    def test_update_document_to_api(self, mocked_downloader_factory_cls, mocked_client_cls, _, mocked_bytesio):
        mocked_client, template_downloader, _ = prepare_mocks_handler_mocks(mocked_client_cls,
                                                                            mocked_downloader_factory_cls)
        handler = TemplateUploaderHandler(self.config, 'cache_db')

        doc = {
                'data': {
                    'id': 'someid',
                    'some': 'field'
                }
            }
        doc = munchify(doc)
        mocked_client.update_document.return_value = deepcopy(doc)

        test_resource = {
            'id': 'resource_id'
        }
        test_template_doc = {
            'id': 'template doc id'
        }
        test_cp_doc = {
            'id': 'contract proforma doc id'
        }
        test_file = 'test_file'

        wrapped_file = 'wrappedfile'
        mocked_bytesio.return_value = wrapped_file

        handler._update_document_in_api(test_resource, test_template_doc, test_cp_doc, test_file, 'test_doc_type')

        mocked_bytesio.assert_called_with(test_file)

        additional_data = {
            'documentOf': 'document',
            'relatedItem': test_cp_doc['id'],
        }
        mocked_client.update_document.assert_called_once_with(
            wrapped_file,
            test_resource['id'],
            test_template_doc['id'],
            doc_type='test_doc_type',
            additional_doc_data=additional_data
        )


def suite():
    suite = unittest.TestSuite()
    return suite


if __name__ == "__main__":
    unittest.main(defaultTest='suite')
