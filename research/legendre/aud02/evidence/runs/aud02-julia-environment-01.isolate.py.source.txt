"""GR-07 namespace launcher, executed under the existing bounded supervisor.

This does not supply aggregate cgroup limits. It preserves the outer sandbox,
mounts host files read-only, exposes only the selected scratch directory writable,
uses a new PID namespace, masks service-manager sockets and disables nested user
namespaces. It never starts a daemon or acquires dependencies.
"""
import os,sys
from pathlib import Path

scratch=Path(sys.argv[1]).resolve()
command=sys.argv[2:]
assert command and scratch.is_dir()
fd=os.open(scratch/'bwrap-info.json',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
os.set_inheritable(fd,True)
args=['/usr/bin/bwrap','--unshare-user','--unshare-pid','--unshare-ipc','--unshare-uts',
      '--disable-userns','--ro-bind','/','/','--proc','/proc','--dev','/dev',
      '--tmpfs','/tmp','--tmpfs','/run','--die-with-parent','--new-session',
      '--bind',str(scratch),'/var/tmp','--chdir','/var/tmp','--info-fd',str(fd)]
for key,value in {'TMPDIR':'/var/tmp/tmp','XDG_CACHE_HOME':'/var/tmp/cache','PYTHONDONTWRITEBYTECODE':'1'}.items():
    args+=['--setenv',key,value]
os.execv(args[0],args+['--',*command])
