import os
from yaml import safe_load


class TemplateDownloader(object):

    def __init__(self, config):
        pass

    def get_template_by_id(self, template_id):
        pass


class YamlTemplateDownloader(TemplateDownloader):

    def __init__(self, config):
        self.filename = config.get('filename')
        self.path_to_registry = config.get('registry_path')
        self.registry_spec_path = os.path.join(self.path_to_registry, self.filename)
        with open(self.registry_spec_path) as f:
            self.registry = safe_load(f)

    def get_template_by_id(self, template_id):
        template_location_info = self.registry.get(template_id)
        if not template_location_info:
            return

        template = {}
        full_path = os.path.join(self.path_to_registry, template_location_info.get('template'))
        with open(full_path) as f:
            template['template'] = f.read()

        full_path = os.path.join(self.path_to_registry, template_location_info.get('scheme'))
        with open(full_path) as f:
            template['scheme'] = f.read()

        full_path = os.path.join(self.path_to_registry, template_location_info.get('form'))
        with open(full_path) as f:
            template['form'] = f.read()

        return template


class TemplateDownloaderFactory(object):

    downloader_mappig = {
        'registry_file': YamlTemplateDownloader
    }

    def get_template_downloader(self, config):
        downloader_type = config.get('type')
        downloader_cls = self.downloader_mappig.get(downloader_type)
        if downloader_cls is None:
            raise ValueError(
                'No such downloader type {}. Available list of types {}'.format(
                    downloader_type,
                    self.downloader_mappig.keys()
                )
            )

        return downloader_cls(config)
