from prometheus_client.core import (
    GaugeMetricFamily, REGISTRY
)

import prometheus_client, os, subprocess

class Storage:
    def __init__(self, path):
        self.path = path
        self.hostname = os.environ["HOSTNAME"]

    def df(self, path):
        out, err = subprocess.Popen(['/bin/df'], stdout=subprocess.PIPE).communicate()
        out = out.splitlines()
        for line in out:
            line = line.decode('utf-8')
            if path in line:
                line = ','.join(line.split()).split(",")
                return int(line[2]) + int(line[3]), line[2], line[3]

    #def getstorage(self):
    #    total, used, free = shutil.disk_usage("/")
    #    return total, used, free

    def collect(self):
        total_bytes, used_bytes, free_bytes = self.df(self.path)
        print(total_bytes)
        print(used_bytes)
        print(free_bytes)
        StorageFree = GaugeMetricFamily('prometheus_storage_free_kilobytes',
                                                  'prometheus storage free in kilobytes',
                                                  labels=['hostname'])

        StorageFree.add_metric([self.hostname], int(free_bytes))
        yield StorageFree

        StorageUsed = GaugeMetricFamily('prometheus_storage_used_kilobytes',
                                        'prometheus storage used in kilobytes',
                                        labels=['hostname'])

        StorageUsed.add_metric([self.hostname], int(used_bytes))
        yield StorageUsed

        StorageTotal = GaugeMetricFamily('prometheus_storage_total_kilobytes',
                                        'prometheus storage total in kilobytes',
                                        labels=['hostname'])

        StorageTotal.add_metric([self.hostname], int(total_bytes))
        yield StorageTotal

path = os.environ["PATH"]
REGISTRY.register(Storage(path=path))
app = prometheus_client.make_wsgi_app()
