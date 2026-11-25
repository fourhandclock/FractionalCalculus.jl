"""Apply the declared relative moment criterion without waiving boundary cases."""
import json,sys
data=json.load(open(sys.argv[1]))
failed=[r for r in data['boundary_probes'] if not r['meets_5e-12_relative']]
print(json.dumps({'criterion':'relative M0 error < 5e-12','failed_cases':failed,
                  'verdict':'REPAIR REQUIRED for the unrestricted generic moment API' if failed else 'PASS'},indent=2))
raise SystemExit(1 if failed else 0)
