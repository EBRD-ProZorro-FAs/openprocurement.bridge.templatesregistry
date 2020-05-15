# -*- coding: utf-8 -*-
import  os
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
    ],
    "mainProcurementCategory": "goods",
    "description": "Папір ксероксний",
    "title": "ДК 021:2015 \"30190000-7 - Офісне устаткування та приладдя різне\" (бумага) \n",
    "contracts": [{
        "status": "active",
        "documents": [{
                "hash": "md5:72235e60d423cb5849b533452666c004",
                "format": "application/pdf",
                "url": "https://public.docs.openprocurement.org/get/c68710ecd6f342b2bd00c9b4656a1139?KeyID=52462340&Signature=mfTkzSa0BgoSJ9fA68UiDg2nnVJcgAV2xJv4l5pZRnc%252BNpdo9BQQBqDu7So9aRzQHmsYowaNY2Oc%252B0Z95%2F50Dw%253D%253D",
                "title": "261.pdf",
                "documentOf": "tender",
                "datePublished": "2020-05-08T12:31:24.305298+03:00",
                "documentType": "contractSigned",
                "dateModified": "2020-05-08T12:31:24.305331+03:00",
                "id": "8211ab77ca374f8d9c5c658ae9507eb7"
            },
            {
                "hash": "md5:9bb0fd7e1a2fdb43970259ecd07a1f57",
                "format": "application/pkcs7-signature",
                "url": "https://public.docs.openprocurement.org/get/1464959a023642d6b8a0003a5e49dc5f?KeyID=52462340&Signature=q2rFidgIzD%252BcNY%252BD90ZdAwQJtX%252BTwmMxgpFy7DZamO%2FaK9Ju2RkcUISvdHXIeoSXHvpP7qkudMDyYVSYvRNCBw%253D%253D",
                "title": "sign.p7s",
                "documentOf": "tender",
                "datePublished": "2020-05-08T12:32:19.752444+03:00",
                "dateModified": "2020-05-08T12:32:19.752480+03:00",
                "id": "6a34ac288afc49769ed92c218b004c40"
            }
        ],
        "items": [{
            "description": "Бумага",
            "classification": {
                "scheme": "ДК021",
                "description": "Офісне устаткування та приладдя різне",
                "id": "30190000-7"
            },
            "deliveryAddress": {
                "postalCode": "27100",
                "countryName": "Україна",
                "streetAddress": "пров. Лікарняний 1 ",
                "region": "Кіровоградська область",
                "locality": "м. Новоукараїнка"
            },
            "deliveryDate": {
                "startDate": "2020-05-08T00:00:00+03:00",
                "endDate": "2020-05-12T00:00:00+03:00"
            },
            "id": "9ea3449772ff47289b1168edf8b4dd59",
            "unit": {
                "code": "NMP",
                "name": "пачок",
                "value": {
                    "currency": "UAH",
                    "amount": 0,
                    "valueAddedTaxIncluded": False
                }
            },
            "quantity": 25
        }],
        "suppliers": [{
            "scale": "mid",
            "contactPoint": {
                "name": "Демянович М.М",
                "telephone": "+380661401133"
            },
            "identifier": {
                "scheme": "UA-EDR",
                "id": "2920707533",
                "legalName": "ДЕМЯНОВИЧ МИКОЛА МИКОЛАЙОВИЧ"
            },
            "name": "ДЕМЯНОВИЧ МИКОЛА МИКОЛАЙОВИЧ",
            "address": {
                "postalCode": "27100",
                "countryName": "Україна",
                "streetAddress": "ВУЛИЦЯ ЛОМОНОСОВА будинок 7",
                "region": "Кіровоградська область",
                "locality": "місто Новоукраїнка"
            }
        }],
        "contractNumber": "261",
        "period": {
            "startDate": "2020-05-08T00:00:00+03:00",
            "endDate": "2020-12-31T00:00:00+02:00"
        },
        "dateSigned": "2020-05-08T12:30:00+03:00",
        "value": {
            "currency": "UAH",
            "amount": 2500,
            "amountNet": 2500,
            "valueAddedTaxIncluded": False
        },
        "date": "2020-05-08T12:32:42.392747+03:00",
        "awardID": "2b9532b89cb34a6fa60629ba57528e0d",
        "id": "6d0ba74771bd4b4493e2d56e31af9055",
        "contractID": "UA-2020-05-08-002276-b-b1"
    }],
    "items": [{
        "description": "Бумага",
        "classification": {
            "scheme": "ДК021",
            "description": "Офісне устаткування та приладдя різне",
            "id": "30190000-7"
        },
        "deliveryAddress": {
            "postalCode": "27100",
            "countryName": "Україна",
            "streetAddress": "пров. Лікарняний 1 ",
            "region": "Кіровоградська область",
            "locality": "м. Новоукараїнка"
        },
        "deliveryDate": {
            "startDate": "2020-05-08T00:00:00+03:00",
            "endDate": "2020-05-12T00:00:00+03:00"
        },
        "id": "9ea3449772ff47289b1168edf8b4dd59",
        "unit": {
            "code": "NMP",
            "name": "пачок"
        },
        "quantity": 25
    }],
    "procurementMethodType": "reporting",
    "value": {
        "currency": "UAH",
        "amount": 2500,
        "valueAddedTaxIncluded": False
    },
    "id": "b7bf55c6a01a4c8d9eb3b24053f7118b",
    "procuringEntity": {
        "contactPoint": {
            "telephone": "+380664376747",
            "name": "Валентина Колпак",
            "email": "centr_novoukr_buh@ukr.net"
        },
        "identifier": {
            "scheme": "UA-EDR",
            "id": "36734786",
            "legalName": "Комунальне некомерційне підприємство \"Центр первинної медико-санітарної допомоги\" Новоукраїнської районної ради"
        },
        "name": "Комунальне некомерційне підприємство \"Центр первинної медико-санітарної допомоги\" Новоукраїнської районної ради",
        "kind": "general",
        "address": {
            "postalCode": "27100",
            "countryName": "Україна",
            "streetAddress": "пров. Лікарняний, буд. 1",
            "region": "Кіровоградська область",
            "locality": "м. Новоукраїнка"
        }
    },
    "owner": "prom.ua",
    "awards": [{
        "status": "active",
        "date": "2020-05-08T12:29:57.379503+03:00",
        "suppliers": [{
            "scale": "mid",
            "contactPoint": {
                "name": "Демянович М.М",
                "telephone": "+380661401133"
            },
            "identifier": {
                "scheme": "UA-EDR",
                "id": "2920707533",
                "legalName": "ДЕМЯНОВИЧ МИКОЛА МИКОЛАЙОВИЧ"
            },
            "name": "ДЕМЯНОВИЧ МИКОЛА МИКОЛАЙОВИЧ",
            "address": {
                "postalCode": "27100",
                "countryName": "Україна",
                "streetAddress": "ВУЛИЦЯ ЛОМОНОСОВА будинок 7",
                "region": "Кіровоградська область",
                "locality": "місто Новоукраїнка"
            }
        }],
        "id": "2b9532b89cb34a6fa60629ba57528e0d",
        "value": {
            "currency": "UAH",
            "amount": 2500,
            "valueAddedTaxIncluded": False
        }
    }],
    "tenderID": "UA-2020-05-08-002276-b",
    "date": "2020-05-08T12:32:42.392747+03:00",
    "dateModified": "2020-05-08T12:32:42.392747+03:00",
    "plans": [{
        "id": "9ec058409b8349bc915ee74f564a2866"
    }]
}


def prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls):
    template_downloader = MagicMock()

    factory = MagicMock()
    factory.get_template_downloader.return_value = template_downloader
    mocked_downloader_factory_cls.return_value = factory

    mocked_client = MagicMock()

    mocked_client_cls.return_value = mocked_client
    return mocked_client, template_downloader, factory


dir_path = os.path.dirname(__file__)
registry_path = os.path.join(dir_path, 'registry')


class TestTemplateUploaderHandler(unittest.TestCase):
    config = {
        'worker_config':
            {
                'handler_registryBot': {
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
    @patch('openprocurement.bridge.registryBot.handlers.APIResourceClient')
    @patch('openprocurement.bridge.registryBot.handlers.TemplateDownloaderFactory')
    def test_init(self, mocked_downloader_factory_cls, mocked_client_cls, _):
        mocked_client, _, factory = prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls)

        handler = TemplateUploaderHandler(self.config, 'cache_db')

        self.assertEquals(handler.cache_db, 'cache_db')
        self.assertEquals(handler.handler_config, self.config['worker_config']['handler_registryBot'])
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

    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.registryBot.handlers.APIResourceClient')
    @patch('openprocurement.bridge.registryBot.handlers.TemplateDownloaderFactory')
    def test_api_upload_document(self, mocked_downloader_factory_cls, mocked_client_cls, _):
        mocked_client, template_downloader, _ = prepare_mocks_handler_mocks(mocked_client_cls, mocked_downloader_factory_cls)

        template_info = {
            'template': 'template',
            'scheme': 'scheme',
            'form': 'form',
        }
        template_downloader.get_template_by_id.side_effect = [
            deepcopy(template_info),
            deepcopy(template_info),
            deepcopy(template_info),
        ]

        docs = [
            {
                'data': {
                    'id': i,
                    'some': 'field'
                }
            } for i in range(3)
        ]
        docs = [munchify(doc) for doc in docs]
        mocked_client.upload_document.side_effect = deepcopy(docs)

        handler = TemplateUploaderHandler(self.config, 'cache_db')

        handler.process_resource(tender)

        self.assertEqual(template_downloader.get_template_by_id.call_count, 1)
        self.assertEqual(mocked_client.upload_document.call_count, 3)
        calls = [
            call(template_info['template'], tender['id'], doc_type='contractTemplate'),
            call(template_info['scheme'], tender['id'], doc_type='contractScheme'),
            call(template_info['form'], tender['id'], doc_type='contractForm'),
        ]
        mocked_client.upload_document.assert_has_calls(calls, any_order=False)

        self.assertEqual(mocked_client.patch_document.call_count, 3)

        doc = tender['documents'][1]
        doc_data = {
            'data': {
                'documentOf': 'document',
                'relatedItem': doc['id']
            }
        }
        calls = [
            call(tender['id'], doc_data, docs[0].data.id),
            call(tender['id'], doc_data, docs[1].data.id),
            call(tender['id'], doc_data, docs[2].data.id),
        ]
        mocked_client.patch_document.assert_has_calls(calls, any_order=False)

    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.registryBot.handlers.APIResourceClient')
    @patch('openprocurement.bridge.registryBot.handlers.TemplateDownloaderFactory')
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
                }
            ]
        }

        doc = handler.get_contract_proforma_document(test_data)
        self.assertEqual(doc, test_data['documents'][1])

    @patch('openprocurement.bridge.basic.handlers.APIClient')
    @patch('openprocurement.bridge.registryBot.handlers.APIResourceClient')
    @patch('openprocurement.bridge.registryBot.handlers.TemplateDownloaderFactory')
    def test_upload_document_to_api(self, mocked_downloader_factory_cls, mocked_client_cls, _):
        mocked_client, template_downloader, _ = prepare_mocks_handler_mocks(mocked_client_cls,
                                                                            mocked_downloader_factory_cls)
        handler = TemplateUploaderHandler(self.config, 'cache_db')

        docs = [
            {
                'data': {
                    'id': i,
                    'some': 'field'
                }
            } for i in range(3)
        ]
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

        handler.upload_document_to_api(test_resource, test_doc, test_file, 'test_doc_type')
        mocked_client.upload_document.assert_called_once_with(test_file, test_resource['id'], doc_type='test_doc_type')
        patched_data = {
            'data': {
                'documentOf': 'document',
                'relatedItem': test_doc['id'],
            }
        }
        mocked_client.patch_document.assert_called_once_with(
            test_resource['id'],
            patched_data,
            doc.data.id
        )


def suite():
    suite = unittest.TestSuite()
    return suite


if __name__ == "__main__":
    unittest.main(defaultTest='suite')
