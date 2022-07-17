from copy import copy
from base_parser import BaseParser

class VibeParser(BaseParser):
    charges_container = []
    subscription_container = []
    account_container = []
    statement_container = []
    adjusting_list = []
    foot_note_container = []

    def set_containers(self):
        self.set_account_summary()
        self.set_statement_summary()
        self.set_charges_container()
        self.set_subscriptions_container()
        self.set_footnote_container()

    def set_charges_container(self):
        index = self.get_index_of_value("Charges For This Month", 1)
        buffer = self.config.buffers['CHARGES_HEADERS']
        for i in range(index, index + buffer + 1):
            key = self.current_list[i]
            value = self.current_list[i + buffer]
            self.charges_container.append([key, value])

    def set_subscriptions_container(self):
        index = self.get_index_of_value("Subscription Charges")
        buffer = self.config.buffers['SUBSCRIPTION_HEADERS']
        for i in range(index, index + buffer + 1):
            key = self.current_list[i]
            value = self.current_list[i + buffer]
            self.subscription_container.append([key, value])

    def set_account_summary(self):
        self.adjusting_list = copy(self.current_list)
        index = self.get_index_of_value("Statement Summary:") + 1
        buffer = self.config.buffers['ACCOUNT_ITEMS']
        end_of_headers = index + buffer

        for i in range(index, index + buffer):
            top_location = self.current_list[i][1][1].strip()
            self.adjusting_list.remove(self.current_list[i])
            for j in range(end_of_headers, len(self.current_list)):
                if top_location in self.current_list[j][1][1]:
                    key = self.current_list[i]
                    value = self.current_list[j]
                    self.adjusting_list.remove(value)
                    self.account_container.append([key, value])
                    break

    def set_statement_summary(self):
        index = self.get_index_of_value("Statement Summary:") + 1
        previous_bill_amount = self.adjusting_list[index]
        previous_bill_amount_value = self.adjusting_list[index + 1]
        self.statement_container.append([previous_bill_amount,
                                         previous_bill_amount_value])

        index += 2
        buffer = self.config.buffers['STATEMENT_ITEMS']
        for i in range(index, index + buffer):
            key = self.adjusting_list[i]
            value = self.adjusting_list[i + buffer]
            self.statement_container.append([key, value])

    def set_footnote_container(self):
        index = self.get_index_of_substring("PAY IN FULL : ") - 1
        buffer = self.config.buffers['FOOTNOTE_ITEMS']

        for i in range(buffer):
            insert_index = buffer - i - 1
            value = self.current_list[index - i]
            self.foot_note_container.insert(insert_index, value)

    def get_company_name_value(self):
        return self.current_list[0][0]

    def get_tmp_list(self):
        for elem in self.adjusting_list:
            print (elem)

    def get_company_address_value(self):
        index = self.get_index_of_value("Statement Summary:")
        address = ""
        for i in range(1, index):
            address += self.current_list[i][0]
        return address

    def get_pay_in_full_value(self):
        for item in self.current_list:
            if "PAY IN FULL : " in item[0]:
                return item[0].replace("PAY IN FULL : ", "")


    def get_charges_value(self, key):
        return self.get_from_container(key, self.charges_container)

    def get_subscriptions_value(self, key):
        return self.get_from_container(key, self.subscription_container)

    def get_account_summary_value(self, key):
        return self.get_from_container(key, self.account_container)

    def get_statement_summary_value(self, key):
        return self.get_from_container(key, self.statement_container)

    def get_footnote_value(self, item):
        return self.foot_note_container[item][0]
