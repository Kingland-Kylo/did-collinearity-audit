"""Download immutable source files directly from Harvard Dataverse; no mirrors."""
from pathlib import Path
import argparse,hashlib,json,os,time,urllib.error,urllib.request
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'data/sources.json'
RAW=ROOT/'data/raw'

def verify(path,expected):
    actual=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual!=expected:
        raise ValueError(f'SHA256 mismatch: {Path(path).name}; expected {expected}, got {actual}')
    return actual

def download_one(item,force=False):
    RAW.mkdir(parents=True,exist_ok=True)
    target=RAW/item['filename']
    if target.exists() and not force:
        verify(target,item['sha256'])
        return {'filename':target.name,'status':'verified existing','sha256':item['sha256']}
    partial=target.with_suffix(target.suffix+'.part')
    try:
        request=urllib.request.Request(item['url'],headers={'User-Agent':'Mozilla/5.0 (reproducibility audit)'})
        # Network failures are reported; do not silently substitute another dataset.
        with urllib.request.urlopen(request,timeout=120) as response,partial.open('wb') as stream:
            while chunk:=response.read(1024*1024):stream.write(chunk)
        verify(partial,item['sha256'])
        os.replace(partial,target)
    finally:
        partial.unlink(missing_ok=True)
    return {'filename':target.name,'status':'downloaded and verified','sha256':item['sha256']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Verify existing files without networking')
    parser.add_argument('--force',action='store_true',help='Re-download files from the official source')
    args=parser.parse_args()
    source=json.loads(MANIFEST.read_text(encoding='utf-8'))
    records=[]
    for item in source['files']:
        if args.check:
            verify(RAW/item['filename'],item['sha256'])
            result={'filename':item['filename'],'status':'verified','sha256':item['sha256']}
        else:result=download_one(item,args.force)
        records.append(result);print(result['filename'],result['status'],flush=True)
    if not args.check:
        record={'source_doi':source['dataset_doi'],'source_version':source['version'],
            'retrieved_or_verified_utc':datetime.now(timezone.utc).isoformat(),'files':records}
        (RAW/'download_record.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    print('All source hashes match. Source files remain excluded from Git.')
if __name__=='__main__':main()
