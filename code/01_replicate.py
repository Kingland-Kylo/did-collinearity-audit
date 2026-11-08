"""Reproduce H1/H3 and original pre-treatment cutoffs. Writes aggregate outputs only."""
import pandas as pd
from audit_lib import ROOT, load_inputs, baselines, placebo_checks, save_json, plot_style
if __name__=='__main__':
    data,source=load_inputs();records=baselines(data)
    placebo_summary=[]
    for col,label in [('treat4','H1'),('treat42','H3')]:
        p,_=placebo_checks(data,source,col)
        placebo_summary.append({'hypothesis':label,'cutoffs':len(p),'conventional_p_lt_05':int(p.p.lt(.05).sum())})
    topics=pd.read_csv(ROOT/'data/raw/particularistic.csv')['part'].tolist()
    gap=float((data[[f'V{i}' for i in topics]].sum(axis=1)-data.particularistic).abs().max())
    save_json('replication.json',{'source_doi':'10.7910/DVN/NOMC0H','data_shape':[6890,471],
                'baseline':records,'original_placebos':placebo_summary,'topic_aggregation_max_gap':gap})
    plt=plot_style();fig,ax=plt.subplots(figsize=(9,3),layout='constrained')
    for i,r in enumerate(records):
        ax.errorbar(r['b']*100,i,xerr=[[100*(r['b']-r['ci_lower'])],[100*(r['ci_upper']-r['b'])]],fmt='o',capsize=4,color='#315F7D')
    ax.set_yticks([0,1],['H1: long-term vs term-limited','H3: long-term vs short-term'])
    ax.set_ylim(1.5,-.5);ax.axvline(0,color='gray',ls='--');ax.set_xlabel('Coefficient (pp); 95% state-clustered CI')
    ax.set_title('Baseline replication',loc='left');fig.savefig(ROOT/'output/baseline.png');plt.close(fig)
    print('Baseline replication complete. H1 pp:',records[0]['b']*100,'H3 pp:',records[1]['b']*100)
