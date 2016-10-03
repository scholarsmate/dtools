import ConfigParser
import itertools
import sys
from string import Template

from faker import Factory
from faker.providers import BaseProvider

from dtools_lib import chooser


class CsvProvider(BaseProvider):
    def __init__(self, generator, fileobj, sep='|', prefix=None):
        super(CsvProvider, self).__init__(generator)
        self.header_ = fileobj.readline().rstrip().split(sep)
        if prefix is not None:
            self.header_ = [prefix + x for x in self.header_]
        self.rows_ = []
        for line in fileobj:
            self.rows_.append(line.rstrip().split(sep))

    def generate(self):
        return dict(zip(self.header_, self.random_element(self.rows_)))


class ItineraryProvider(CsvProvider):
    def __init__(self, generator, fileobj, sep='|'):
        super(ItineraryProvider, self).__init__(generator, fileobj, sep)

    def generate(self):
        ADMISSIONCLASSES = ['K3', 'K2', 'J2', 'K4', 'P3', 'G4', 'P2', 'V3', 'Q3', 'L1A', 'L2', 'C1', 'D1', 'D2', 'K1',
                            'G3', 'V2', 'P4', 'L1B', 'H4', 'G5', 'H3', 'G2', 'C4', 'P1', 'C2', 'J1', 'C1D', 'Q2', 'V1',
                            'F2', 'N8', 'G1', 'N9', 'TN', 'A3', 'A2', 'B2', 'B1', 'Q1', 'A1', 'H2A', 'H1C', 'R1', 'H2B',
                            'TPS', 'T3', 'R2', 'T', 'M2', 'U1', 'T2', 'TD', 'S6', 'S5', 'O3', 'O1', 'H1B', 'M1', 'O2',
                            'T1']
        result = {
            'admission_class': self.random_element(ADMISSIONCLASSES),
            'contact_phone_number': self.generator.phone_number(),
        }
        result.update(self.leg_('departure_'))
        result.update(self.leg_('arrival_', airportNotIn=[result['departure_airport']]))
        return result

    def leg_(self, prefix, airportNotIn=None):
        CARRIERS = ['UA', 'BA', 'DL', 'SR', 'AA', 'CO', 'TW', 'SV', 'RB', 'WN', 'JL', '', 'QF', 'US', 'LH', 'LY', 'ZP',
                    'IQ', 'OS', 'AM', 'AC', 'PC', 'SU', 'AR', 'AF', 'FI', 'JM', 'AI', 'KX', 'MS', 'HH', 'KQ', 'UP',
                    'AS', 'AG']
        leg_data = CsvProvider.generate(self)
        if airportNotIn is not None:
            while leg_data['iata_code'] in airportNotIn:
                leg_data = CsvProvider.generate(self)
        return {
            prefix + 'airport': leg_data['iata_code'],
            prefix + 'country': leg_data['iso_country'],
            prefix + 'region': leg_data['iso_region'],
            prefix + 'municipality': leg_data['municipality'],
            prefix + 'carrier': self.random_element(CARRIERS),
            prefix + 'flight_number': self.generator.random_int(min=0, max=9000),
        }


class AddressProvider(CsvProvider):
    def __init__(self, generator, fileobj, sep='|', prefix=None):
        super(AddressProvider, self).__init__(generator, fileobj, sep, prefix)
        self.street_ = 'street'
        if prefix is not None:
            self.street_ = prefix + self.street_

    def generate(self):
        result = {self.street_: self.generator.street_address()}
        result.update(CsvProvider.generate(self))
        return result


class SequenceProvider(object):
    def __init__(self, seq=0, step=1, name='sequence'):
        self.seq_ = seq
        self.step_ = step
        self.name_ = name

    def generate(self):
        self.seq_ += self.step_
        return {self.name_: self.seq_}


class PersonProvider(BaseProvider):
    def __init__(self, generator):
        super(PersonProvider, self).__init__(generator)
        self.gender_chooser = chooser.WeightedChooser([('F', 1), ('M', 1)])

    def generate(self, gender=None):
        if gender not in self.gender_chooser.choices():
            gender = self.gender_chooser.choose()

        if gender == 'F':
            name = self.generator.name_female()
        else:
            name = self.generator.name_male()

        return {
            'name': name,
            'gender': gender,
            'email': self.generator.free_email(),
            'birth_date': self.generator.date(),
            'citizenship': self.generator.country_code(),
            'passport_number': self.generator.numerify(text='#########'),
            'job': self.generator.job(),
            'company': self.generator.company(),
            'ssn': self.generator.ssn(),
            'blood_type': ''.join(self.random_element(list(itertools.product(['A', 'B', 'AB', '0'], ['+', '-'])))),
            'website': self.generator.url(),
            'phone_number': self.generator.phone_number(),
        }


config = ConfigParser.ConfigParser()
try:
    config.read(sys.argv[1])
except IndexError:
    config.read('generate.ini')

num_records = 100
try:
    num_records = int(sys.argv[2])
except IndexError:
    if config.has_option('Generator', 'records'):
        num_records = config.getint('Generator', 'records')

record_template = Template(config.get('Record', 'template'))
generator = Factory.create(config.get('Generator', 'locale', None))
if config.has_option('Generator', 'seed'):
    generator.seed(config.getint('Generator', 'seed'))

with open(config.get('Generator', 'postal_codes', 'us_postal_codes.csv')) as f:
    residential_address_provider = AddressProvider(generator, f, prefix='residential_')
with open(config.get('Generator', 'airport_codes', 'airport_codes.csv')) as f:
    itinerary_provider = ItineraryProvider(generator, f)

person_provider = PersonProvider(generator)
sequence_provider = SequenceProvider()
if config.has_option('Record', 'header'):
    print config.get('Record', 'header')
for _ in range(num_records):
    while True:
        d = {}
        for provider in [sequence_provider, person_provider, residential_address_provider, itinerary_provider]:
            d.update(provider.generate())
        try:
            print record_template.safe_substitute(d)
        except UnicodeDecodeError:
            continue
        break
