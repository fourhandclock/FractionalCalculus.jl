"""Check researcher-facing closure documentation without touching history."""
import argparse,json,re
from pathlib import Path
from urllib.parse import unquote,urlsplit
from execution import ROOT,REVIEW,ORIGINAL

def slug(s):
    s=re.sub(chr(96)+r'|\*|\$', '', s).lower()
    return re.sub(r'[^\w\- ]','',s).replace(' ','-')

def headings(path):
    counts={};result=set()
    for match in re.finditer(r'^#{1,6}\s+(.+)$',path.read_text(),re.M):
        base=slug(match.group(1));n=counts.get(base,0);counts[base]=n+1
        result.add(base+('-'+str(n) if n else ''))
    return result

def inspect(path):
    failures=[];links=0;table_lines=0;display=0
    source=path.read_text();fence=chr(96)*3
    if source.count(fence)%2:failures.append(['unbalanced code fence'])
    plain=re.sub(fence+r'[^\n]*\n.*?'+fence,'',source,flags=re.S)
    if plain.count('$$')%2:failures.append(['unbalanced display math'])
    display+=plain.count('$$')//2
    rest=re.sub(r'\$\$.*?\$\$','',plain,flags=re.S)
    if rest.count('$')%2:failures.append(['unbalanced inline math'])
    previous=None
    for line in plain.splitlines():
        if line.startswith('|'):
            cols=len(re.findall(r'(?<!\\)\|',line))-1
            if previous is not None and cols!=previous:failures.append(['table columns',line])
            previous=cols;table_lines+=1
        else:previous=None
    for match in re.finditer(r'!?\[[^\]]+\]\(([^)\n]+)\)',plain):
        target=match.group(1).strip().strip('<>');parsed=urlsplit(target)
        if parsed.scheme or target.startswith('mailto:'):continue
        links+=1;resolved=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
        if not resolved.exists():failures.append(['missing target',target]);continue
        if parsed.fragment and resolved.suffix.lower()=='.md' and unquote(parsed.fragment) not in headings(resolved):
            failures.append(['missing fragment',target])
    return dict(file=str(path.relative_to(ROOT if path.is_relative_to(ROOT) else ORIGINAL)),local_links=links,table_lines=table_lines,
                display_math_blocks=display,failures=failures)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--id',required=True);args=parser.parse_args()
    assert args.id and all(c.isalnum() or c in '-_' for c in args.id)
    paths=[*REVIEW.glob('*.md'),ROOT/'README.md',ROOT/'studies/legendre/README.md',
           ROOT/'research/legendre/verification/README.md',ROOT/'studies/legendre/gr07/revision-01/README.md']
    rows=[inspect(p) for p in sorted(paths)]
    new_failures=[];existing_failures=[]
    for row in rows:
        old=ORIGINAL/row['file'];previous=inspect(old)['failures'] if old.exists() else []
        for f in row['failures']:
            target=existing_failures if f in previous else new_failures
            target.append(dict(file=row['file'],failure=f))
    result=dict(markdown_files=len(rows),local_links=sum(r['local_links'] for r in rows),
                table_lines=sum(r['table_lines'] for r in rows),files=rows,
                new_failures=new_failures,preexisting_failures=existing_failures,
                visual_github_render_performed=False,passed=not new_failures)
    output=REVIEW/'evidence'/('documentation-checks-'+args.id+'.json')
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));raise SystemExit(bool(new_failures))
if __name__=='__main__':main()
