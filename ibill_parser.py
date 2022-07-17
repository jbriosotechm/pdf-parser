from base_parser import BaseParser


# imports the module from the given path
class IBillParser(BaseParser):
    account_container = []
    statement_container = []

    def set_containers(self):
        self.set_account_summary()
        self.set_statement_summary()

    def set_account_summary(self):
        index = self.get_index_of_value("Amount to Pay")
        amount_to_pay = self.current_list[index]
        index += 2
        amount_to_pay_value = self.current_list[index]
        self.account_container.append([amount_to_pay, amount_to_pay_value])
        buffer = self.config.buffers['ACCOUNT_ITEMS']

        while buffer != 0:
            index += 1
            key = self.current_list[index]
            index += 1
            value = self.current_list[index]
            self.account_container.append([key, value])
            buffer -= 1

    def set_statement_summary(self):
        index = self.get_index_of_value("Statement Summary") + 1
        buffer = self.config.buffers['STATEMENT_ITEMS']
        count = 0

        for i in range(index, index + buffer):
            key = self.current_list[i]
            value = None
            if key[0] not in self.config.LABELS['STATEMENT_SUMMARY']:
                value = self.current_list[index+ buffer + count]
                count += 1
            self.statement_container.append([key, value])

    def get_company_name_value(self):
        return self.current_list[self.config.location['COMPANY_NAME']][0]

    def get_plan_name_value(self):
        index = self.get_index_of_substring("Bill no.")
        return self.current_list[index - 1][0]

    def get_company_address_value(self):
        index = self.get_index_of_substring("ATTN:")
        address = ""
        start = self.config.location['COMPANY_NAME'] + 1
        for i in range(start, index):
            address += self.current_list[i][0] + " "
        return address.strip()

    def get_account_summary_value(self, key):
        return self.get_from_container(key, self.account_container)

    def get_statement_summary_value(self, key):
        return self.get_from_container(key, self.statement_container)
