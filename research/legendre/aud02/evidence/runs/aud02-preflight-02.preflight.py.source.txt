"""Small containment fixture before AUD-02 scientific execution."""
import os,subprocess
from pathlib import Path
p=Path(os.environ['AUD02_PROBE_SOURCE'])
for name,action in [('write',lambda:p.write_text('bad')),('chmod',lambda:p.chmod(0o600)),
                    ('rename',lambda:p.rename(p.with_suffix('.moved'))),('unlink',p.unlink)]:
    try:action()
    except OSError:print('read-only operation blocked:',name)
    else:raise AssertionError(name+' unexpectedly permitted')
child=subprocess.Popen(['/usr/bin/setsid','/usr/bin/sleep','20'])
print('detached child started; namespace teardown must remove it:',child.pid,flush=True)
