# -*- coding: utf-8 -*-
import logging
from io import BytesIO

from openprocurement.bridge.basic.handlers import HandlerTemplate
from openprocurement_client.clients import APIResourceClient
from openprocurement.bridge.templatesregistry.template_downloader import TemplateDownloaderFactory


config = {
    'worker_type': 'contracting',
    'client_inc_step_timeout': 0.1,
    'client_dec_step_timeout': 0.02,
    'drop_threshold_client_cookies': 2,
    'worker_sleep': 5,
    'retry_default_timeout': 3,
    'retries_count': 10,
    'queue_timeout': 3,
    'bulk_save_limit': 100,
    'bulk_save_interval': 3,
    'resources_api_token': '',
    'resources_api_version': '',
    'input_resources_api_server': '',
    'input_public_resources_api_server': '',
    'input_resource': 'tenders',
    'output_resources_api_server': '',
    'output_public_resources_api_server': '',
    'output_resource': 'agreements',
    'handler_templateUploader': {
        'resources_api_token': '',
        'output_resources_api_token': 'agreement_token',
        'resources_api_version': '',
        'input_resources_api_token': 'tender_token',
        'input_resources_api_server': '',
        'input_public_resources_api_server': '',
        'input_resource': 'tenders',
        'output_resources_api_server': '',
        'output_public_resources_api_server': '',
        'output_resource': 'agreements'
    }
}

CONFIG_MAPPING = {
    'input_resources_api_token': 'resources_api_token',
    'output_resources_api_token': 'resources_api_token',
    'resources_api_version': 'resources_api_version',
    'input_resources_api_server': 'resources_api_server',
    'input_public_resources_api_server': 'public_resources_api_server',
    'input_resource': 'resource',
    'output_resources_api_server': 'resources_api_server',
    'output_public_resources_api_server': 'public_resources_api_server'
}


logger = logging.getLogger(__name__)
TEMPLATE_DOCUMENT_TYPES = [
    'contractTemplate',
    'contractSchema',
    'contractForm',
]


class TemplateUploaderHandler(HandlerTemplate):

    def __init__(self, config, cache_db):
        logger.info("Init registryBot handler.")
        self.handler_name = 'handler_templateUploader'
        super(TemplateUploaderHandler, self).__init__(config, cache_db)
        self.template_downloader = TemplateDownloaderFactory().get_template_downloader(self.handler_config.get('template_downloader', {}))

        self.client = APIResourceClient(
            key=self.handler_config.get('resources_api_token'),
            resource=self.handler_config['resource'],
            host_url=self.handler_config['resources_api_server'],
            api_version=self.handler_config['resources_api_version'],
            ds_config=self.handler_config.get('DS', {}),
        )

    def _upload_document_to_api(self, resource, contract_proforma_document, file_, doc_type):
        logger.info(
            "Create document for contractProforma document {} of tender {}".format(
                contract_proforma_document['id'],
                resource['id']
            )
        )
        doc_data = {
            'relatedItem': contract_proforma_document['id'],
            'documentOf': 'document'
        }
        response = self.client.upload_document(
            BytesIO(file_),
            resource['id'],
            doc_type=doc_type,
            additional_doc_data=doc_data
        )

        return response

    def _update_document_in_api(self, resource, document, contract_proforma_document, file_, doc_type):
        logger.info(
            "Update document {} for contractProforma document {} of tender {}".format(
                document['id'],
                contract_proforma_document['id'],
                resource['id'],
            ),
        )

        doc_data = {
            'relatedItem': contract_proforma_document['id'],
            'documentOf': 'document'
        }
        response = self.client.update_document(
            BytesIO(file_),
            resource['id'],
            document['id'],
            doc_type=doc_type,
            additional_doc_data=doc_data
        )
        return response

    def get_contract_proforma_documents(self, resource):
        return [doc for doc in resource.get('documents', []) if doc.get('documentType', '') == 'contractProforma']

    def get_template_documents(self, resource, contract_proforma_document):
        template_documents = [doc for doc in resource.get('documents', []) if doc.get('relatedItem') == contract_proforma_document['id']]
        template_documents = [doc for doc in template_documents if doc.get('documentType') in TEMPLATE_DOCUMENT_TYPES]
        return template_documents

    def is_templates_should_be_changed(self, resource, contract_proforma_document):
        template_documents = self.get_template_documents(resource, contract_proforma_document)
        is_template_documents_older = [contract_proforma_document['dateModified'] > doc['dateModified'] for doc in template_documents]
        return any(is_template_documents_older)

    def is_templates_should_be_created(self, resource, contract_proforma_document):
        template_documents = self.get_template_documents(resource, contract_proforma_document)
        return not template_documents

    def _create_template_documents(self, resource, document):
        logger.info('Get templates for tender {} and document {}'.format(resource['id'], document['id']))
        template_info = self.template_downloader.get_template_by_id(document['templateId'])

        self._upload_document_to_api(
            resource,
            document,
            template_info['template'],
            'contractTemplate'
        )

        self._upload_document_to_api(
            resource,
            document,
            template_info['scheme'],
            'contractSchema'
        )

        self._upload_document_to_api(
            resource,
            document,
            template_info['form'],
            'contractForm'
        )

    def _update_template_documents(self, resource, document):
        logger.info('Get templates for tender {} and document {}'.format(resource['id'], document['id']))
        template_info = self.template_downloader.get_template_by_id(document['templateId'])

        template_docs = {
            doc['documentType']: doc
            for doc in self.get_template_documents(resource, document)
        }

        self._update_document_in_api(
            resource,
            template_docs['contractTemplate'],
            document,
            template_info['template'],
            'contractTemplate'
        )

        self._update_document_in_api(
            resource,
            template_docs['contractSchema'],
            document,
            template_info['scheme'],
            'contractSchema'
        )

        self._update_document_in_api(
            resource,
            template_docs['contractForm'],
            document,
            template_info['form'],
            'contractForm'
        )

    def process_document(self, resource, document):
        logger.info("Process document {} of tender {} ".format(document['id'], resource['id']))
        if self.is_templates_should_be_created(resource, document):
            logger.info("Create documents for document {} of tender {}".format(document['id'], resource['id']))
            self._create_template_documents(resource, document)
        elif self.is_templates_should_be_changed(resource, document):
            logger.info("Update documents for tender {} of tender {}".format(document['id'], resource['id']))
            self._update_template_documents(resource, document)

    def process_resource(self, resource):
        cp_documents = self.get_contract_proforma_documents(resource)
        for doc in cp_documents:
            self.process_document(resource, doc)