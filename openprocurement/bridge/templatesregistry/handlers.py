# -*- coding: utf-8 -*-
import logging

from openprocurement_client.exceptions import (
    RequestFailed,
    ResourceNotFound,
    ResourceGone
)

from retrying import retry

from openprocurement.bridge.basic.handlers import HandlerTemplate
from openprocurement_client.clients import APIResourceClient
from openprocurement.bridge.templatesregistry.utils import journal_context
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
    'handler_cfaua': {
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


class TemplateUploaderHandler(HandlerTemplate):

    def __init__(self, config, cache_db):
        logger.info("Init registryBot handler.")
        self.handler_name = 'handler_registryBot'
        super(TemplateUploaderHandler, self).__init__(config, cache_db)
        self.template_downloader = TemplateDownloaderFactory().get_template_downloader(self.handler_config.get('template_downloader', {}))

        self.client = APIResourceClient(
            key=self.handler_config.get('resources_api_token'),
            resource=self.handler_config['resource'],
            host_url=self.handler_config['resources_api_server'],
            api_version=self.handler_config['resources_api_version'],
            ds_config=self.handler_config.get('DS', {}),
        )

    def upload_document_to_api(self, resource, doc, file_, doc_type):
        response = self.client.upload_document(file_, resource['id'], doc_type=doc_type)
        new_doc_id = response.data.id

        doc_data = {
            'relatedItem': doc['id'],
            'documentOf': 'document'
        }
        response = self.client.patch_document(
            resource['id'],
            {'data': doc_data},
            new_doc_id,

        )
        return response

    def get_contract_proforma_document(self, resource):
        for doc in resource.get('documents', []):
            if doc.get('documentType', '') == 'contractProforma':
                return doc

    def process_resource(self, resource):
        doc = self.get_contract_proforma_document(resource)

        template_info = self.template_downloader.get_template_by_id(doc['id'])

        self.upload_document_to_api(
            resource,
            doc,
            template_info['template'],
            'contractTemplate'
        )

        self.upload_document_to_api(
            resource,
            doc,
            template_info['scheme'],
            'contractScheme'
        )

        self.upload_document_to_api(
            resource,
            doc,
            template_info['form'],
            'contractForm'
        )
