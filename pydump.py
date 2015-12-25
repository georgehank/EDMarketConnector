from os.path import join, basename, exists
from os import symlink, remove
from pprint import pformat
import time
from errno import ENOENT

from config import config

def makepyname(s):
    return s.replace(" ", "_").replace("-", "_").replace(".", "_")

def export_all(data):
    querytime = config.getint('querytime') or int(time.time())
    filename = join(config.get('outdir'), 'ALL_%s.py' % time.strftime('%Y%m%dT%H%M%S', time.localtime(querytime)))
    linkname = join(config.get('outdir'), 'ALL.py')
    export_with_link(filename=filename, linkname=linkname, data=data)

def export_commodities(data):
    export_all(data)

    querytime = config.getint('querytime') or int(time.time())

    filename = join(config.get('outdir'), 'COMMODITIES_%s_%s_%s.py' % (makepyname(data['lastSystem']['name'].strip()), makepyname(data['lastStarport']['name'].strip()), time.strftime('%Y%m%dT%H%M%S', time.localtime(querytime))))
    linkname = join(config.get('outdir'), 'COMMODITIES_%s_%s.py' % (makepyname(data['lastSystem']['name'].strip()), makepyname(data['lastStarport']['name'].strip())))

    export_with_link(filename=filename, linkname=linkname,
                                 system=data["lastSystem"]["name"],
                                 station=data["lastStarport"]["name"],
                                 data=data['lastStarport']['commodities'])

def export_outfitting(data):
    export_all(data)

    querytime = config.getint('querytime') or int(time.time())

    filename = join(config.get('outdir'), 'OUTFITTING_%s_%s_%s.py' % (makepyname(data['lastSystem']['name'].strip()),
                                                                    makepyname(data['lastStarport']['name'].strip()),
                                                                    time.strftime('%Y%m%dT%H%M%S', time.localtime(querytime))))
    linkname = join(config.get('outdir'), 'OUTFITTING_%s_%s.py' % (makepyname(data['lastSystem']['name'].strip()),
                                                                 makepyname(data['lastStarport']['name'].strip())))

    export_with_link(filename=filename, linkname=linkname,
                                 system=data["lastSystem"]["name"],
                                 station=data["lastStarport"]["name"],
                                 data=data['lastStarport']["modules"])

def export_shipyard(data):
    export_all(data)

    querytime = config.getint('querytime') or int(time.time())

    filename = join(config.get('outdir'), 'SHIPYARD_%s_%s_%s.py' % (makepyname(data['lastSystem']['name'].strip()),
                                                                    makepyname(data['lastStarport']['name'].strip()),
                                                                    time.strftime('%Y%m%dT%H%M%S', time.localtime(querytime))))
    linkname = join(config.get('outdir'), 'SHIPYARD_%s_%s.py' % (makepyname(data['lastSystem']['name'].strip()),
                                                                 makepyname(data['lastStarport']['name'].strip())))

    export_with_link(filename=filename, linkname=linkname,
                                 system=data["lastSystem"]["name"],
                                 station=data["lastStarport"]["name"],
                                 data=data['lastStarport']["ships"])


def export_loadout(data):
    export_all(data)

    querytime = config.getint('querytime') or int(time.time())

    filename = join(config.get('outdir'), 'SHIP_%s_%s_%s.py' % (makepyname(data['commander']['name'].strip()),
                                                                makepyname(data['ship']['name'].strip()),
                                                                time.strftime('%Y%m%dT%H%M%S', time.localtime(querytime))))
    linkname = join(config.get('outdir'), 'SHIP_%s_%s.py' % (makepyname(data['commander']['name'].strip()),
                                                             makepyname(data['ship']['name'].strip())))

    export_with_link(filename=filename, linkname=linkname, data=data["ship"])

def export_ships(data):
    export_all(data)
    querytime = config.getint('querytime') or int(time.time())

    filename = join(config.get('outdir'), 'SHIPS_%s_%s.py' % (makepyname(data['commander']['name'].strip()),
                                                              time.strftime('%Y%m%dT%H%M%S', time.localtime(querytime))))
    linkname = join(config.get('outdir'), 'SHIPS_%s.py' % (makepyname(data['commander']['name'].strip())))

    export_with_link(filename=filename, linkname=linkname, data=data["ships"])

def export_commander(data):
    export_all(data)

    querytime = config.getint('querytime') or int(time.time())

    filename = join(config.get('outdir'), 'COMMANDER_%s_%s.py' % (makepyname(data['commander']['name'].strip()),
                                                                  time.strftime('%Y%m%dT%H%M%S', time.localtime(querytime))))
    linkname = join(config.get('outdir'), 'COMMANDER_%s.py' % (makepyname(data['commander']['name'].strip())))

    export_with_link(filename=filename, linkname=linkname, data=data["commander"])

def export_with_link(filename=None, linkname=None, **kws):
    output = []
    for key, value in kws.items():
        output.append("%s=" % key)
        output.append(("\n"+" "*(len(key)+1)).join(pformat(value).split("\n")))
        output.append("\n")
    output = "".join(output)

    try:
        with open(linkname, "rt") as stream:
            old_output = stream.read()
    except IOError as err:
        if err.errno != ENOENT:
            raise
        old_output = ""
    if output != old_output:
        with open(filename, "wt") as stream:
            stream.write(output)

        try:
            remove(linkname)
        except OSError as err:
            if err.errno != ENOENT:
                raise
        symlink(basename(filename), linkname)
