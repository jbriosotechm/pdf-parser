from html.parser import HTMLParser
import importlib.util
import sys

class BaseParser(HTMLParser):
    current_attributes: str = ""
    current_list: list = []
    current_dict: dict = {}
    config = None

    def clear(self):
        self.current_attributes: str = ""
        self.current_list: list = []
        self.current_dict: dict = {}

    def handle_starttag(self, tag, attrs) -> None:
        if tag == "div":
            attribute_values = attrs[0][1]
            if "left" in attribute_values:
                position_start = attribute_values.index('left')
                attribute_values = attribute_values[position_start:].split(';')
                self.current_attributes = attribute_values

    def handle_endtag(self, tag) -> None:
        if tag == "div":
            self.current_attributes = ""

    def handle_data(self, data) -> None:
        if data.strip() != "" and self.current_attributes != "":
            self.current_list.append((data.strip(), self.current_attributes))

    def get_list(self) -> None:
        for elem in self.current_list:
            print (elem)

    def get_index_of_value(self, value, offset = 0) -> int:
        count = 0
        for index, item in enumerate(self.current_list):
            if item[0] == value:
                if offset == count:
                    return index
                count = count + 1
        print (f"[WARN] '{value}' with offset {offset} is not found")

    def get_index_of_substring(self, value, offset = 0) -> int:
        count = 0
        index = None
        for index, item in enumerate(self.current_list):
            if value in item[0]:
                if offset == count:
                    return index
                count = count + 1
        print (f"[WARN] '{value}' with offset {offset} is not found")

    def set_config(self, config):
        spec = importlib.util.spec_from_file_location("config", config)
        module = importlib.util.module_from_spec(spec)
        sys.modules["config"] = module
        spec.loader.exec_module(module)
        self.config = spec.loader.load_module()

    @staticmethod
    def get_from_container(key, container) -> str:
        for item in container:
            item_key = item[0][0]
            item_value = None

            if item[1] is not None:
                item_value = item[1][0]
            if key == item_key:
                return item_value
        print (f"[WARN] '{key}' is not found in given container")
