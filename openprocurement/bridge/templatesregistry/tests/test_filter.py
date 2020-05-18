# -*- coding: utf-8 -*-
import  os
import unittest
from copy import deepcopy
from mock import patch, MagicMock, call
from munch import munchify

from gevent.queue import PriorityQueue

from openprocurement.bridge.templatesregistry.filters import ContractProformaFilter


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


CONFIG = {
    'filter_config': {
        'status_accordance': {
            'dgf': ['status1'],
        },
        'timeout': 0,
    },
    'resource': 'tenders'
}


class TestContractProformaFilter(unittest.TestCase):
    conf = CONFIG
    db = {}

    @patch('openprocurement.bridge.templatesregistry.filters.INFINITY')
    def test_init(self, infinity):
        self.input_queue = PriorityQueue()
        self.filtered_queue = PriorityQueue()

        filter = ContractProformaFilter(self.conf, self.input_queue, self.filtered_queue, self.db)

        # Valid tender filtering
        infinity.__nonzero__.side_effect = [True, False]
        doc = {
            'id': 'test_id',
            'dateModified': '1970-01-02',
            'procurementMethodType': 'dgf',
            'status': 'status1',
            'documents': [
                {
                    'documentType': 'contractProforma'
                }
            ]
        }

        self.input_queue.put((None, deepcopy(doc)))
        filter._run()
        self.assertEqual(len(self.filtered_queue), 1)
        filtered_doc = self.filtered_queue.get(block=False)
        self.assertEqual(
            doc,
            filtered_doc[1]
        )

        # Not changed dateModified
        infinity.__nonzero__.side_effect = [True, False]
        doc = {
            'id': 'test_id',
            'dateModified': '1970-01-01',
            'procurementMethodType': 'dgf',
            'status': 'status1',
            'documents': [
                {
                    'documentType': 'contractProforma'
                }
            ],
        }

        self.input_queue.put((None, deepcopy(doc)))
        self.db['test_id'] = '1970-01-01'

        filter._run()
        self.assertEqual(len(self.filtered_queue), 0)

        self.db.pop('test_id')

        # No contractProforma doc
        infinity.__nonzero__.side_effect = [True, False]
        doc = {
            'id': 'test_id',
            'dateModified': '1970-01-01',
            'procurementMethodType': 'dgf',
            'status': 'status1',
            'documents': [
                {
                    'documentType': 'notContractProforma'
                }
            ],
        }

        filter._run()
        self.assertEqual(len(self.filtered_queue), 0)

        # Wrong tender status
        infinity.__nonzero__.side_effect = [True, False]
        doc = {
            'id': 'test_id',
            'dateModified': '1970-01-01',
            'procurementMethodType': 'dgf',
            'status': 'status3',
            'documents': [
                {
                    'documentType': 'contractProforma'
                }
            ],
        }

        self.input_queue.put((None, deepcopy(doc)))

        filter._run()
        self.assertEqual(len(self.filtered_queue), 0)

        # Wrong procurementMethodType
        infinity.__nonzero__.side_effect = [True, False]
        doc = {
            'id': 'test_id',
            'dateModified': '1970-01-01',
            'procurementMethodType': 'other_pmt',
            'status': 'status1',
            'documents': [
                {
                    'documentType': 'contractProforma'
                }
            ],
        }

        filter._run()
        self.assertEqual(len(self.filtered_queue), 0)


def suite():
    suite = unittest.TestSuite()
    return suite


if __name__ == "__main__":
    unittest.main(defaultTest='suite')
