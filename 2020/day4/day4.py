import re

valid_eyecolors = ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

def test_byr(val):
    if not val.isdigit():
        return False
    return 1919 < int(val) < 2003

def test_iyr(val):
    if not val.isdigit():
        return False
    return 2009 < int(val) < 2021

def test_eyr(val):
    if not val.isdigit():
        return False
    return 2019 < int(val) < 2031

def test_hgt(val):
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


def test_hcl(val):
    '''
    Returns match-object or None
    '''
    return re.match('^#[0-9|a-f]{6}$', val)
    #if not re.match('^#[0-9|a-f]{6}', val):
        #print(val)
        #return False
    #return True

def test_ecl(val):
    return val in valid_eyecolors
    #'''
    #Returns match-object or None
    #'''
    #return re.match('^(amb|blu|brn|gry|grn|hzl|oth)$', val)

def test_pid(val):
    return len(val) == 9 and val.isdigit()

def test_cid(val):
    return True

req_fields = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid')
field_tests = (test_byr, test_iyr, test_eyr, test_hgt, test_hcl, test_ecl, test_pid, test_cid)
fields_reqs = dict(zip(req_fields, field_tests))
#print(fields_reqs)
#{
#    'byr': test_byr,
#    'iyr': ETCETC
#    'eyr': JNE
#    'hgt': ,
#    'hcl',
#    'ecl',
#    'pid',
#    'cid'
#}

def read_inpt():
    content = None
    with open('input.txt', 'r') as f:
        content = f.read().split('\n\n')
    return [pp.strip() for pp in content]

def filter_passports(passports, required_fields = req_fields):
    required_fields = tuple(map(lambda f: f + ':', required_fields))
    def tester(pp, req = required_fields):
        for r in req:
            if not r in pp:
                return False
        return True
    return list(filter(tester, passports))

def check_passport_fields(passprt):
    fields = passprt.split()

    for f in fields:
        field, val = f.split(':')
        if not fields_reqs[field](val):
            return False

    return True

def main():
    valid_passprts_count = 0

    passprts_with_req_fields = filter_passports(read_inpt(), req_fields[:-1]) # 'cid:' is optional => ignore it
    for pp in passprts_with_req_fields:
        valid_passprts_count += check_passport_fields(pp)
    print(valid_passprts_count)

    # Boolean array containing true for every valid passport
    ppp = [check_passport_fields(pp) for pp in passprts_with_req_fields]
    print('valid passports:  ', sum(ppp))
    # Flip bool
    print('invalid passports:', sum([not pp for pp in ppp]))


if __name__ == '__main__':
    main()
