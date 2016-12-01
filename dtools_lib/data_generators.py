import random

from faker.providers import BaseProvider
from faker.providers.person.en_US import Provider as BasePersonNameProvider

from dtools_lib import chooser
from dtools_lib.lazy import LazyDictionary


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
    ADMISSIONCLASSES = [
        'K3', 'K2', 'J2', 'K4', 'P3', 'G4', 'P2', 'V3', 'Q3', 'L1A', 'L2', 'C1', 'D1', 'D2', 'K1',
        'G3', 'V2', 'P4', 'L1B', 'H4', 'G5', 'H3', 'G2', 'C4', 'P1', 'C2', 'J1', 'C1D', 'Q2', 'V1',
        'F2', 'N8', 'G1', 'N9', 'TN', 'A3', 'A2', 'B2', 'B1', 'Q1', 'A1', 'H2A', 'H1C', 'R1', 'H2B',
        'TPS', 'T3', 'R2', 'T', 'M2', 'U1', 'T2', 'TD', 'S6', 'S5', 'O3', 'O1', 'H1B', 'M1', 'O2',
        'T1']

    CARRIERS = [
        'UA', 'BA', 'DL', 'SR', 'AA', 'CO', 'TW', 'SV', 'RB', 'WN', 'JL', 'QF', 'US', 'LH', 'LY', 'ZP',
        'IQ', 'OS', 'AM', 'AC', 'PC', 'SU', 'AR', 'AF', 'FI', 'JM', 'AI', 'KX', 'MS', 'HH', 'KQ', 'UP',
        'AS', 'AG']

    def __init__(self, generator, fileobj, sep='|'):
        super(ItineraryProvider, self).__init__(generator, fileobj, sep)

    def generate(self):
        result = LazyDictionary({
            'admission_class': lambda: self.random_element(ItineraryProvider.ADMISSIONCLASSES),
            'contact_phone_number': lambda: self.generator.phone_number(),
        })
        self.leg_(result, 'departure_')
        self.leg_(result, 'arrival_', airportNotIn=[result['departure_airport']])
        return result

    def leg_(self, ld, prefix, airportNotIn=None):
        leg_data = CsvProvider.generate(self)
        if airportNotIn is not None:
            while leg_data['iata_code'] in airportNotIn:
                leg_data = CsvProvider.generate(self)
        ld.update({
            prefix + 'airport': leg_data['iata_code'],
            prefix + 'country': leg_data['iso_country'],
            prefix + 'region': leg_data['iso_region'],
            prefix + 'municipality': leg_data['municipality'],
            prefix + 'carrier': lambda: self.random_element(ItineraryProvider.CARRIERS),
            prefix + 'flight_number': lambda: self.generator.random_int(min=0, max=9000),
        })


class AddressProvider(CsvProvider):
    def __init__(self, generator, fileobj, sep='|', prefix=None):
        super(AddressProvider, self).__init__(generator, fileobj, sep, prefix)
        self.street_ = 'street' if prefix is None else prefix + 'street'

    def generate(self):
        result = LazyDictionary({self.street_: lambda: self.generator.street_address()})
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


class GenderProvider(object):
    DEFAULT_WEIGHTED_GENDERS = [('F', 1), ('M', 1)]

    def __init__(self, weighted_genders=DEFAULT_WEIGHTED_GENDERS):
        self.gender_chooser = chooser.WeightedChooser(weighted_genders)

    def generate(self, prefix=''):
        return LazyDictionary({prefix + 'gender': lambda: self.gender_chooser.choose()})


class BiometricProvider(object):
    DEFAULT_WEIGHTED_EYE_COLORS = [
        ('amber', 5), ('black', 1), ('blue', 8), ('brown', 55), ('gray', 1), ('green', 2), ('hazel', 7),
    ]
    DEFAULT_WEIGHTED_HAIR_COLORS = [
        ('black', 64), ('brown', 16), ('blond', 5), ('red', 2), ('gray', 4),
    ]
    DEFAULT_WEIGHTED_BLOOD_TYPES = [
        ('A+', 34), ('A-', 6), ('B+', 9), ('B-', 2), ('AB+', 3), ('AB-', 1), ('O+', 38), ('O-', 7),
    ]

    def __init__(self, weighted_eye_colors=DEFAULT_WEIGHTED_EYE_COLORS,
                 weighted_hair_colors=DEFAULT_WEIGHTED_HAIR_COLORS, weighted_blood_types=DEFAULT_WEIGHTED_BLOOD_TYPES):

        self.eye_color_chooser = chooser.WeightedChooser(weighted_eye_colors)
        self.hair_color_chooser = chooser.WeightedChooser(weighted_hair_colors)
        self.blood_type_chooser = chooser.WeightedChooser(weighted_blood_types)

        self.female_height_chooser = chooser.GaussianChooser(65, 3.5)
        self.female_weight_chooser = chooser.GaussianChooser(155, 35)
        self.male_height_chooser = chooser.GaussianChooser(70, 4)
        self.male_weight_chooser = chooser.GaussianChooser(165, 40)

    def generate(self, gender, prefix=''):
        return LazyDictionary({
            prefix + 'height': lambda d:
            int(self.female_height_chooser.choose()) if gender == 'F' else int(self.male_height_chooser.choose()),
            prefix + 'weight': lambda d:
            int(self.female_weight_chooser.choose()) + d['height'] - 50 if gender == 'F' else
            int(self.male_weight_chooser.choose()) + d['height'] - 45,
            prefix + 'blood_type': lambda: self.blood_type_chooser.choose(),
            prefix + 'eye_color': lambda: self.eye_color_chooser.choose(),
            prefix + 'hair_color': lambda: self.hair_color_chooser.choose(),
        })


class PersonNameProvider(BasePersonNameProvider):
    def generate(self, gender, prefix=''):
        if gender == 'F':
            title = self.prefix_female() if random.random() <= 0.1 else ''
            given = self.first_name_female()
            middle = self.first_name_female() if random.random() <= 0.4 else ''
            surname = self.last_name_female()
            suffix = self.suffix_female() if random.random() <= 0.05 else ''
        else:
            title = self.prefix_male() if random.random() <= 0.1 else ''
            given = self.first_name_male()
            middle = self.first_name_male() if random.random() <= 0.4 else ''
            surname = self.last_name_male()
            suffix = self.suffix_male() if random.random() <= 0.05 else ''

        return {
            prefix + 'name': ' '.join([x for x in (title, given, middle, surname, suffix) if len(x) > 0]),
            prefix + 'name_prefix': title,
            prefix + 'first_name': given,
            prefix + 'middle_name': middle,
            prefix + 'last_name': surname,
            prefix + 'name_suffix': suffix,
        }


class PersonDetailsProvider(BaseProvider):
    def generate(self, prefix=''):
        return LazyDictionary({
            prefix + 'email': lambda: self.generator.free_email(),
            prefix + 'birth_date': lambda: self.generator.date(),
            prefix + 'citizenship': lambda: self.generator.country_code(),
            prefix + 'passport_number': lambda: self.generator.numerify(text='#########'),
            prefix + 'occupation': lambda: self.generator.job(),
            prefix + 'company': lambda: self.generator.company(),
            prefix + 'ssn': lambda: self.generator.ssn(),
            prefix + 'website': lambda: self.generator.url(),
            prefix + 'phone_number': lambda: self.generator.phone_number(),
        })
