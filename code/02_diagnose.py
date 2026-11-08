"""Audit the original H2 final-year specification; distinguish constraints from identification."""
import pandas as pd
from audit_lib import ROOT, load_inputs, h2_audit, save_json, plot_style
if __name__=='__main__':
    data,source=load_inputs();record,h,coverage,allocation=h2_audit(data,source)
    save_json('diagnostics.json',record)
    coverage.to_csv(ROOT/'output/coverage.csv',encoding='utf-8',index_label='group')
    keys=['beta','m_20160006','m_20140007','s_Puebla','const']
    table=pd.DataFrame({k:{key:values.get(key) for key in keys} for k,values in allocation.items()})*100
    table.to_csv(ROOT/'output/coefficient_allocation_pp.csv',encoding='utf-8',index_label='parameter')
    plt=plot_style();fig,ax=plt.subplots(figsize=(10,3.2),layout='constrained')
    ax.imshow(coverage,cmap='Blues',aspect='auto',vmin=0,vmax=492)
    for i in range(3):
        for j in range(4):
            n=int(coverage.iloc[i,j]);ax.text(j,i,str(n) if n else '—',ha='center',va='center',fontsize=16,color='white' if n>300 else '#172A3D')
    ax.set_xticks(range(4),coverage.columns);ax.set_yticks(range(3),coverage.index)
    ax.set_title('H2 final-year sample: Session coverage (— = no selected observations)',loc='left')
    fig.savefig(ROOT/'output/coverage.png');plt.close(fig)
    print('H2 final-year: N=',len(h),'rank(FE),rank(FE+D)=',record['ranks'],'identity mismatches=',record['identity_mismatches'])
