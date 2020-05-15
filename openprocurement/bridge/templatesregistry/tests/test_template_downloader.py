# -*- coding: utf-8 -*-
import  os
import unittest
import json
from openprocurement.bridge.templatesregistry.template_downloader import (
    YamlTemplateDownloader,
    TemplateDownloaderFactory,
)

dir_path = os.path.dirname(__file__)
registry_path = os.path.join(dir_path, 'registry')


class TestYamlTemplateDownloader(unittest.TestCase):
    config = {
        'filename': 'registry.yml',
        'registry_path': registry_path
    }

    def test_init(self):
        template_downloader = YamlTemplateDownloader(self.config)

        self.assertEqual(self.config['filename'], template_downloader.filename)
        self.assertEqual(self.config['registry_path'], template_downloader.path_to_registry)
        reg_spec_file = os.path.join(self.config['registry_path'], self.config['filename'])
        self.assertEqual(reg_spec_file, template_downloader.registry_spec_path)

        test_registry_data = {
            'paper0000001': {
                'template': 'paper0000001.docx',
                'scheme': 'paper0000001-scheme.json',
                'form': 'paper0000001-form.json'
            }
        }
        self.assertEqual(test_registry_data, template_downloader.registry)

    def test_getting_doc_by_id(self):
        template_downloader = YamlTemplateDownloader(self.config)

        template_info = template_downloader.get_template_by_id('paper0000001')

        self.assertEqual(
            'template',
            template_info['template']
        )

        test_form = {
            'form': 'data'
        }
        self.assertEqual(
            test_form,
            json.loads(template_info['form'])
        )

        test_scheme = {
            'scheme': 'data'
        }
        self.assertEqual(
            test_scheme,
            json.loads(template_info['scheme'])
        )


class TestTemplateDownloaderFactory(unittest.TestCase):

    def test_get_existed_downloader(self):
        factory = TemplateDownloaderFactory()
        config = {
            'type': 'registry_file',
            'filename': 'registry.yml',
            'registry_path': registry_path
        }
        template_downloader = factory.get_template_downloader(config)
        self.assertIsInstance(template_downloader, YamlTemplateDownloader)

    def test_not_existed_downloader(self):
        factory = TemplateDownloaderFactory()
        config = {
            'type': 'not_existed',
            'filename': 'registry.yml',
            'registry_path': registry_path
        }
        try:
            factory.get_template_downloader(config)
        except ValueError as exc:
            self.assertEqual(
                str(exc),
                'No such downloader type {}. Available list of types {}'.format(
                    config['type'],
                    factory.downloader_mappig.keys()
                )
            )


def suite():
    suite = unittest.TestSuite()
    return suite


if __name__ == "__main__":
    unittest.main(defaultTest='suite')
