"""从官方来源下载论文数据；已有本地文件先校验，不删除或默认覆盖。

python download_data.py             # 获取缺少的文件，核对已有文件
python download_data.py --check     # 仅核对本地文件
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,urllib.request

ROOT=Path(__file__).resolve().parent
PAPERS = {'motolinia': {'folder': 'Motolinia-读论文',
               'doi': '10.7910/DVN/NOMC0H',
               'version': '1.0',
               'files': [{'filename': 'allres.csv',
                          'file_id': 3892153,
                          'role': 'analysis data',
                          'sha256': '7b9d34c7fa32501435e5a3f3bc7b1ea9262fb321aa504c038aa652beded798aa',
                          'url': 'https://dataverse.harvard.edu/api/access/datafile/3892153?format=original'},
                         {'filename': 'replication_analysis.do',
                          'file_id': 3892146,
                          'role': 'original main analysis',
                          'sha256': '074ebfd19d05c4d30c16f4118d820b929112be893c976288199bfe31f9725c54',
                          'url': 'https://dataverse.harvard.edu/api/access/datafile/3892146?format=original'},
                         {'filename': 'replication_appendix.do',
                          'file_id': 3892135,
                          'role': 'original appendix code',
                          'sha256': 'df377639185abde3bf226417b9b8ca7342859929fc2f0f700f8302682f6e1930',
                          'url': 'https://dataverse.harvard.edu/api/access/datafile/3892135?format=original'},
                         {'filename': 'replication_cleaning_CTM.R',
                          'file_id': 3892151,
                          'role': 'original CTM code',
                          'sha256': '0170446dbce39b8985a37f616521637ab234ab514a5cc353b863d84c5ba10b6e',
                          'url': 'https://dataverse.harvard.edu/api/access/datafile/3892151?format=original'},
                         {'filename': 'particularistic.csv',
                          'file_id': 3892157,
                          'role': 'original topic classification',
                          'sha256': '100b6b85ea03f16aa6a62dbbfa4d4c661cceef0f99bb115fb9bd1a228d6124f2',
                          'url': 'https://dataverse.harvard.edu/api/access/datafile/3892157?format=original'}]}}

def verify(path,expected):
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected:
        raise ValueError(f'{path.name} 的SHA256不匹配；本地文件已保留，未覆盖。')
    return actual

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paper',choices=sorted(PAPERS),default='motolinia')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    source=PAPERS[args.paper]
    directory=ROOT/source['folder']/'原作者文件'
    directory.mkdir(parents=True,exist_ok=True)
    results=[]
    for item in source['files']:
        target=directory/item['filename']
        if target.exists():
            verify(target,item['sha256']);status='已核对，保留原文件'
        elif args.check:
            raise FileNotFoundError(f'缺少{target.name}，可先运行 python download_data.py')
        else:
            partial=directory/(item['filename']+'.part')
            request=urllib.request.Request(item['url'],headers={'User-Agent':'Mozilla/5.0 (reading papers)'})
            try:
                with urllib.request.urlopen(request,timeout=120) as response,partial.open('wb') as out:
                    while chunk:=response.read(1024*1024):out.write(chunk)
                verify(partial,item['sha256'])
                os.replace(partial,target)
            finally:
                partial.unlink(missing_ok=True)
            status='已从Dataverse官方下载并核对'
        print(item['filename'],status,flush=True)
        results.append({'filename':item['filename'],'sha256':item['sha256'],'status':status})
    if not args.check:
        record={'doi':source['doi'],'version':source['version'],
                'verified_utc':datetime.now(timezone.utc).isoformat(),'files':results}
        (directory/'下载记录.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print('完成。本地原作者文件不随Git仓库上传。')

if __name__=='__main__':main()
