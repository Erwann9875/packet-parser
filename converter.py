import yaml

class Converter:
    @staticmethod
    def dto_to_yaml(dtos):
        yaml_data = []
        for dto in dtos:
            dto_dict = dto.__dict__
            yaml_data.append(dto_dict)
        return yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)