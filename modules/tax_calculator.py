
import json
import time
import warnings
from app import app
from collections import OrderedDict
warnings.simplefilter(action='ignore', category=FutureWarning)

class TaxCalculator:
    __taxes = None
    __country = None

    def __init__(self, country):

        assert (isinstance(country, str)), 'country must be a str path'
        f = open(f'data/{country}_taxes.json')
        self.__taxes = OrderedDict((el['min'], el) for el in json.load(f))
        self.__country = country

    def generate(self, salary=0 , detailed=False):
        """
        export salary/income taxes

        Parameters
        ----------
        salary : float
            salary/income must be a float

        detailed : bool
            detailed can be True or False

        Returns
        -------
        dict.

        """
        assert (isinstance(salary, float) or isinstance(salary, int)), 'salary/income must be a float/int '
        assert (isinstance(detailed, bool) ), 'detailed must be a bool '
        details = {}
        total = 0
        prev_tax_range = 0
        for v in self.__taxes.values():
            if salary > v['max']:
                csum = (v['max'] - prev_tax_range) * v['tax_percent']/100
                total = total + csum
                details[v['label']] = csum
                prev_tax_range = v['max']
            else:
                csum = (salary - prev_tax_range) * v['tax_percent']/100
                details[v['label']] = csum
                total = total + csum

                break

        if detailed:
            return {'total': total, 'details': details}
        else:
            return {'total': total}
