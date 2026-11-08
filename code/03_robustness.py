"""Separate the short-term extension from alternative-specification design sensitivity."""
from audit_lib import (ROOT, load_inputs, short_extension, h2_audit,
                       alternative_specifications, save_json, plot_style)
if __name__=='__main__':
    data,source=load_inputs();short,placebos=short_extension(data,source)
    save_json('short_term_extension.json',short)
    placebos[['cutoff','cohort_shift','month','b','se','p','wild_p','ci_lower','ci_upper']].to_csv(ROOT/'output/short_term_placebos.csv',index=False)
    _,h,_,_=h2_audit(data,source)
    save_json('specification_sensitivity.json',{'purpose':'Design sensitivity; changed assumptions, not a repair of the original H2',
                                             'models':alternative_specifications(h)})
    plt=plot_style();fig,ax=plt.subplots(figsize=(10,4),layout='constrained')
    for _,r in placebos.iterrows():
        color='#8B1E2D' if r.p<.05 else '#70869B'
        ax.errorbar(r.cutoff,r.b*100,yerr=[[100*(r.b-r.ci_lower)],[100*(r.ci_upper-r.b)]],fmt='o',ms=4,capsize=2,color=color)
    ax.axhline(0,color='black',ls='--');ax.set(xlabel='Placebo cutoff (33 separate regressions)',ylabel='DID coefficient (pp)')
    ax.set_title(f'Short-term extension: pre-treatment checks; joint p={short["joint_max_abs_t_p"]:.3f}',loc='left')
    fig.savefig(ROOT/'output/short_term_placebos.png');plt.close(fig)
    print('Short-term extension pp:',short['comparisons'][0]['b']*100,'wild p:',short['comparisons'][0]['wild_p'])
