import datetime
import dateutil.parser
import json
import pytz
import six

from .geo import geojson_to_reql

TIMEZONES = {tz: pytz.timezone(tz) for tz in pytz.all_timezones}


def coerce(value):
    if isinstance(value, list):
        if len(value) == 2 and value[0] in COERSIONS:
            return COERSIONS[value[0]](value[1])
        return [coerce(item) for item in value]
    return value


def coerce_datetime(value):
    '''
        ['$datetime', '1987-07-24 9:07pm']
    '''
    value = dateutil.parser.parse(value, tzinfos=TIMEZONES)
    if value.tzinfo is None:
        value = pytz.utc.localize(value)
    return value


def coerce_date(value):
    '''
        ['$date', '1987-07-24']
    '''
    value = coerce_datetime(value)
    return datetime.datetime(value.year, value.month, value.day,
        tzinfo=value.tzinfo)


def coerce_time(value):
    '''
        ['$time', '16:20']
    '''
    return coerce_datetime(value).time()


def coerce_geojson(value):
    if isinstance(value, six.string_types):
        value = json.loads(value)
    return geojson_to_reql(value)


COERSIONS = {
    '$date': coerce_date,
    '$time': coerce_time,
    '$datetime': coerce_datetime,
    '$geojson': coerce_geojson,
}
