from djfritz import __version__


def djfritz_version_string(request):
    return {'djfritz_version_string': f'v{__version__}'}
