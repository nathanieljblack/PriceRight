import json
import datetime

class FileScrubber(object):
    """Scrubs raw data of missing prices, extreme price values, and re-formats fields"""
    def __init__(self, jsonstr):
        """for file """
        try:
            self.raw_file = json.loads(jsonstr)
            self.error_reading_file = False
        except:
            self.error_reading_file = True

    def scrub_data(self):
        if (self.error_reading_file):
            return None

        def price_not_null(price_field):
            if price_field != '':
                return True
            else:
                return False

        def make_price_num(price_field):
            return float(price_field[1:])

        def price_filter(price_field, low_price = 60, high_price = 1500):
            return low_price < price_field < high_price

        def encode_unicode(text_field):
            return text_field.encode('utf-8')

        def make_datetime(date_field):
            return datetime.datetime.strptime(date_field[:10], "%Y-%m-%d")

        #Filter blanks
        self.filter_data = [i for i in self.raw_file if price_not_null(i['price'])]

        #Convert to numbers
        for i in xrange(0, len(self.filter_data)):
            self.filter_data[i]['price'] = make_price_num(self.filter_data[i]['price'])
            self.filter_data[i]['create_date'] = make_datetime(self.filter_data[i]['create_date'])
            self.filter_data[i]['title'] = encode_unicode(self.filter_data[i]['title'])

        #Price filter
        self.filter_data = [i for i in self.filter_data if price_filter(i['price'])]
        return self.filter_data

if __name__ == "__main__":
    scrub = FileScrubber("atlanta.json")
    filtered = scrub.scrub_data()
