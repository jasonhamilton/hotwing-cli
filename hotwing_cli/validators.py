import os
import click
import json
# click parameters validators
def validate_side(ctx, param, value):
    if value not in ['l','r']:
        raise click.BadParameter('side needs to be in format of l or r')
    return value

def vaidate_config_file(ctx, param, value):
    if not os.path.isfile(value):
        raise click.BadParameter("could not find config file named: '%s'" % value)
    return value

def validate_trim(ctx, param, value):
    if value:
        try:
            a,b = value.split("-")
            TRIM_A = float(a)
            TRIM_B = float(b)
            return (TRIM_A, TRIM_B)
        except:
            raise click.BadParameter("got '%s', expecting something like 1-10" % value)
    else:
        return None

# custom validators

def validate_kerf(kerf):
    # should receive a string
    if "," in kerf:
        k = kerf.split(',')
        return (float(k[0]),float(k[1]))
    else:
        return float(kerf)