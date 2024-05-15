def tupleToSemver(version_tuple):
    return '.'.join(map(str, version_tuple)).strip('.').strip(',')

def fahrenheitToCelsius(fahrenheit):
    return (fahrenheit - 32) * 5.0/9.0

def normalizeNumber(number):
    number = float("{:.2f}".format(number))
    return number
