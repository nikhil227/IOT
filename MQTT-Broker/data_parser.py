"""
Parse message data into CSV File
"""
from datetime import datetime
import csv

dateTimeObj = datetime.now()

class CSV_Parser():

    def __init__(self):
        self.filename= dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S")+".csv"
        self.first_record=True

    def parse_str_dict(self, text):
        """
        String to dict parser
        :param text:Dict String
        :return: Python Dict object
        """
        return eval(text)

    def epoc_to_date_time(self, text):
        """
        Epoc Date to Text Date conversion is received message
        :param text: dict
        :return: dict with date converted
        """
        text["Timestamp"] = str(datetime.fromtimestamp(text["Timestamp"]).strftime("%Y-%m-%d %I:%M:%S"))
        return text

    def append_rows_file(self,text):
        """
        Write data to CSV File
        :param text: Mqtt message published by publisher in form of dict string
        """
        try:
            print("in append rows")
            print("Text received {}".format(text))

            data= self.parse_str_dict(text)
            data=self.epoc_to_date_time(data)
            csv_columns = data.keys()
            with open(self.filename, "a") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_columns, lineterminator='\n')
                if self.first_record == True:
                    writer.writeheader()
                    writer.writerow(data)
                    self.first_record = False
                else:
                    writer.writerow(data)

        except IOError:
            print("I/O error")
