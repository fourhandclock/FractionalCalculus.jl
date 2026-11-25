import importlib.metadata as m,json,os,platform,sys,hashlib
from pathlib import Path
packages={}
for name in ['numpy','scipy','mpmath','sympy']:
    d=m.distribution(name)
    records=[p for p in d.files if str(p).endswith('.dist-info/RECORD')]
    packages[name]={'version':d.version,'record_sha256':hashlib.sha256(Path(d.locate_file(records[0])).read_bytes()).hexdigest()}
print(json.dumps({'python':platform.python_version(),'prefix':sys.prefix,'base_prefix':sys.base_prefix,
                 'isolated':sys.prefix!=sys.base_prefix,'packages':packages,'platform':platform.platform(),
                 'cpu_affinity':sorted(os.sched_getaffinity(0)),'network_acquisition':False},indent=2))
