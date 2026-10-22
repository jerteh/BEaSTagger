from pathlib import Path
import argparse, json, sys, time
import torch
from beast.tag import tag

torch.set_num_threads(2)
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Eight-token synthetic Serbian inference smoke test')
parser.add_argument('--output',type=Path,default=root/'runs/smoke')
args=parser.parse_args()
out=args.output if args.output.is_absolute() else root/args.output
out.mkdir(parents=True,exist_ok=False)
forms=['Ovo','je','test','.','Čovek','čita','knjigu','.']
input_path=out/'smoke_input.txt'
input_path.write_text('Ovo\nje\ntest\n.\n\nČovek\nčita\nknjigu\n.\n',encoding='utf-8',newline='\n')
start=time.perf_counter()
tag(src=str(input_path),model=str(root/'artifacts/serbian'),out_path=str(out),tokenize=False,transliterate=False,
    lexiconmagic=False,modelnames=['UD.pt'],lemmafor=['ud'],quiet=True)
output=out/'smoke_input.txt_serbian.tt'
lines=output.read_text(encoding='utf-8').splitlines()
rows=[line.split('\t') for line in lines[1:] if line]
assert len(rows)==len(forms),(len(rows),len(forms))
assert [r[0] for r in rows]==forms
assert all(len(r)==3 for r in rows),rows
report={'status':'passed','tokens':len(rows),'seconds':time.perf_counter()-start,'model':'UD.pt',
        'normalization':{'tokenize':False,'transliterate':False,'lexiconmagic':False},'rows':rows}
(root/'smoke-result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=True))
