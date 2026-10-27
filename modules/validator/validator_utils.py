def urlIdToGmlId(uri):
    """Zwraca wynik operacji `urlIdToGmlId` wykonywanej w bieżącym module."""
    identyf = '/'.join(uri.split(
        'https://www.gov.pl/zagospodarowanieprzestrzenne/app/')[-1].split('/')[1:])
    # identyf = '/'.join(uri.split('https://www.gov.pl/static/zagospodarowanieprzestrzenne/app/')[-1].split('/')[1:])
    return identyf.replace('/', '_')
