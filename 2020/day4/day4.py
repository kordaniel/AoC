import sys
sys.path.insert(0, '..')

from helpers import filemap
import re

# Validators
def test_byr(val): return val.isdigit() and 1919 < int(val) < 2003 # Birth year
def test_iyr(val): return val.isdigit() and 2009 < int(val) < 2021 # Issue year
def test_eyr(val): return val.isdigit() and 2019 < int(val) < 2031 # Expiration year
def test_pid(val): return val.isdigit() and len(val) == 9          # Passport ID
def test_ecl(val): return val in valid_eyecolors                   # Eye color
def test_hcl(val): return re.match('^#[0-9|a-f]{6}$', val)         # Hair color
def test_cid(val): return True # Should be ignored, always True    # Country ID
def test_hgt(val):                                                 # Height
    min, max = 0,0
    if val.endswith('cm'):
        min, max = 149, 194
    elif val.endswith('in'):
        min, max = 58, 77
    else:
        return False

    try:
        val = int(val[:-2])
        return min < val < max
    except:
        return False

valid_eyecolors = ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
req_fields  = (    'byr',    'iyr',    'eyr',    'hgt',    'hcl',    'ecl',    'pid',    'cid')
field_tests = (test_byr, test_iyr, test_eyr, test_hgt, test_hcl, test_ecl, test_pid, test_cid)
validators = dict(zip(req_fields, field_tests))

def filter_passports(passports, required_fields = req_fields):
    required_fields = tuple(map(lambda f: f + ':', required_fields))
    def tester(pp, req = required_fields):
        for r in req:
            if not r in pp:
                return False
        return True
    return list(filter(tester, passports))

def validate_passport_fields(passprt):
    fields = passprt.split()

    for f in fields:
        field, val = f.split(':')
        if not validators[field](val):
            return False

    return True

def valid_passport_fields_count(passports):
    return sum([validate_passport_fields(pp) for pp in passports])


def main():
    data = filemap('input.txt', lambda s: s.strip(), '\n\n')

    passports_with_req_fields = filter_passports(data, req_fields[:-1]) # 'cid:' is optional => ignore it
    pp_req_fields_count = len(passports_with_req_fields)
    pp_valid_fields_count = valid_passport_fields_count(passports_with_req_fields)

    print('Part1, passports with required fields:', pp_req_fields_count)
    print('Part2, passports with valid fields   :', pp_valid_fields_count)


if __name__ == '__main__':
    main()
