def tupleToSemver(version_tuple):
    return '.'.join(map(str, version_tuple)).strip('.').strip(',')
