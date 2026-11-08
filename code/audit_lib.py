"""Shared estimation and diagnostics for the Motolinia (2021, APSR) audit."""
from pathlib import Path
from itertools import product
from functools import lru_cache
import hashlib,json,re
import numpy as np
import pandas as pd
from scipy.linalg import qr
from scipy.stats import t as student_t
import statsmodels.api as sm
ROOT=Path(__file__).resolve().parents[1]
@lru_cache(None)
def sign_weights(g):
    if g > 12:
        raise ValueError('枚举 bootstrap 仅用于本 notebook 的少聚类补充比较。')
    return np.asarray(list(product([-1., 1.], repeat=g))).T

class FixedEffectsDesign:
    def __init__(self, frame):
        self.frame = frame.dropna(subset=['state', 'date2', 'particularistic']).copy()
        self.n = len(self.frame)
        self.cluster_id, self.states = pd.factorize(self.frame.state, sort=True)
        self.g = len(self.states)
        self.cluster = np.eye(self.g)[self.cluster_id]
        months, _ = pd.factorize(self.frame.date2, sort=True)
        # 全套州虚拟变量表示截距；年月变量省略一类。
        self.controls = np.column_stack([self.cluster,
                            np.eye(months.max()+1)[months, 1:]])
        q, r, piv = qr(self.controls, mode='economic', pivoting=True)
        diagonal = np.abs(np.diag(r))
        tol = max(self.controls.shape) * np.finfo(float).eps * diagonal.max()
        self.rank = int((diagonal > tol).sum())
        self.q = q[:, :self.rank]
        self.y = self.frame.particularistic.to_numpy(float)
        self.yr = self.residualize(self.y)

    def residualize(self, z):
        z = np.asarray(z, dtype=float)
        return z - self.q @ (self.q.T @ z)

    def fit(self, regressor, wild=False, return_boot=False):
        if isinstance(regressor, str):
            regressor = self.frame[regressor]
        elif isinstance(regressor, pd.Series):
            regressor = regressor.reindex(self.frame.index)
        x = np.asarray(regressor, dtype=float)
        assert len(x) == self.n and np.isfinite(x).all()
        xr = self.residualize(x)
        xx = float(xr @ xr)
        result = dict(n=self.n, states=self.g, rank_FE=self.rank,
                      rank_FE_D=self.rank + int(xx > 1e-10), residual_D_ss=xx)
        if xx <= 1e-10:
            result.update(identified=False, b=np.nan, se=np.nan, p=np.nan,
                          ci_lower=np.nan, ci_upper=np.nan, wild_p=np.nan)
            return result
        b = float(xr @ self.yr / xx)
        u = self.yr - b*xr
        correction = self.g/(self.g-1) * (self.n-1)/(self.n-self.rank-1)
        cluster_scores = self.cluster.T @ (xr*u)
        se = float(np.sqrt(correction * (cluster_scores @ cluster_scores)) / xx)
        p = float(2*student_t.sf(abs(b/se), self.g-1))
        critical = student_t.ppf(.975, self.g-1)
        result.update(identified=True, b=b, se=se, p=p,
                      ci_lower=b-critical*se, ci_upper=b+critical*se, wild_p=np.nan)
        if wild:
            # H0: beta=0；固定效应受限拟合的残差是 yr。
            weights = sign_weights(self.g)
            y_star = self.yr[:, None] * weights[self.cluster_id]
            y_star = self.residualize(y_star)
            b_star = (xr @ y_star) / xx
            u_star = y_star - xr[:, None]*b_star
            scores = self.cluster.T @ (xr[:, None]*u_star)
            se_star = np.sqrt(correction*np.sum(scores**2, axis=0)) / xx
            boot_t = np.abs(b_star/se_star)
            result['wild_p'] = float(np.mean(boot_t >= abs(b/se)-1e-12))
            if return_boot:
                result['boot_t'] = boot_t
        return result


def load_inputs():
    manifest=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))
    directory=ROOT/'data/raw'
    for item in manifest['files']:
        p=directory/item['filename']
        if not p.is_file():raise FileNotFoundError(f'Missing {p.name}; run: python data/download.py')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError(f'Source hash mismatch: {p.name}')
    d=pd.read_csv(directory/'allres.csv')
    assert d.shape==(6890,471)
    dates=pd.to_datetime(d.realyear.astype(str)+' '+d.month,format='%Y %B',errors='coerce')
    d['date']=dates;d['date2']=dates.dt.year*10000+dates.dt.month
    d['month_index']=dates.dt.year*12+dates.dt.month
    d['D_long']=d.treat4*d.reform;d['D_short']=d.treat2*d.reform
    d['treat42']=np.select([d.treat4.eq(1),d.treat2.eq(1)],[1.,0.],default=np.nan)
    d['D_horizon']=d.treat42*d.reform
    d['group']=np.select([d.treat4.eq(1),d.treat2.eq(1)],['长期激励','短期激励'],default='无连任激励')
    return d,(directory/'replication_analysis.do').read_text(encoding='utf-8')

def fe_matrix(frame):
    return pd.concat([pd.Series(1.,index=frame.index,name='const'),
        pd.get_dummies(frame.state,prefix='s',drop_first=True,dtype=float),
        pd.get_dummies(frame.date2.astype(int),prefix='m',drop_first=True,dtype=float)],axis=1)

def ranks(frame):
    F=fe_matrix(frame)
    return [int(np.linalg.matrix_rank(F)),int(np.linalg.matrix_rank(np.column_stack([F,frame.D])))]

def timing_mask(data,source,name):
    clauses=re.findall(r'replace '+name+r'=1 if date2>(\d+) & date2<=(\d+) & \(([^\r\n]*)\)',source)
    if len(clauses)!=6:raise ValueError(f'Unexpected original selection rules: {name}')
    mask=pd.Series(False,index=data.index)
    for lo,hi,expr in clauses:
        mask|=data.date2.gt(int(lo)) & data.date2.le(int(hi)) & data.state.isin(re.findall(r'state=="([^"]+)"',expr))
    return mask

def baselines(data):
    records=[]
    for column,label in [('D_long','H1: long-term vs term-limited'),('D_horizon','H3: long-term vs short-term')]:
        design=FixedEffectsDesign(data.dropna(subset=[column]))
        r=design.fit(column);r['comparison']=label;records.append(r)
    assert records[0]['n']==4899 and np.isclose(records[0]['b'],.01525336444865884)
    assert records[1]['n']==6062 and np.isclose(records[1]['b'],.02623265672428348)
    return records

def placebo_checks(data,source,column,wild=False):
    cohort={}
    for threshold,expr in re.findall(r'(?:gen|replace) rm10[^=]*=0 if date2<(\d+)[^&]*& \(([^\r\n]*)\)',source):
        for state in re.findall(r'state=="([^"]+)"',expr):cohort[state]=int(threshold[:4])
    assert len(cohort)==20
    design=FixedEffectsDesign(data.loc[data.reform.eq(0)&data[column].notna()])
    rows=[];draws=[]
    for shift,count in [(2,12),(1,12),(0,9)]:
        for month in range(1,count+1):
            cutoff=(design.frame.state.map(cohort)-shift)*10000+month
            x=design.frame[column]*design.frame.date2.ge(cutoff)
            r=design.fit(x,wild=wild,return_boot=wild)
            if wild:draws.append(r.pop('boot_t'))
            r.update(cutoff=len(rows)+1,cohort_shift=shift,month=month);rows.append(r)
    table=pd.DataFrame(rows);joint=None
    if wild:
        observed=np.abs(table.b/table.se).max()
        joint=float(np.mean(np.vstack(draws).max(axis=0)>=observed-1e-12))
    return table,joint

def h2_audit(data,source):
    cycles=[];frames={}
    for name,label in [('timinga','Election (t)'),('timingb','t+1'),('timingc','t+2')]:
        model=FixedEffectsDesign(data.loc[timing_mask(data,source,name)&data.D_long.notna()])
        r=model.fit('D_long');r['comparison']=label;cycles.append(r);frames[name]=model.frame
    h=frames['timingc'].copy();h['D']=h.D_long
    h['L']=h.date2.between(20170007,20180006).astype(int)
    h['E']=h.date2.between(20120007,20130006).astype(int)
    h['P']=h.state.eq('Puebla').astype(int)
    mismatch=int((h.D!=h.L+h.E-h.P).sum())
    F=fe_matrix(h);assert ranks(h)==[59,59] and mismatch==0
    y=h.particularistic
    pure=sm.OLS(y,F).fit();constraints=[];allocation={'FE only':{'beta':None,**pure.params.to_dict()}}
    for omitted,label in [(20160006,'Omit June 2016'),(20140007,'Omit July 2014')]:
        X=pd.concat([F[['const']],h.D.rename('D'),F.drop(columns=['const',f'm_{omitted}'])],axis=1)
        assert np.linalg.matrix_rank(X)==59
        fit=sm.OLS(y,X).fit(cov_type='cluster',cov_kwds={'groups':h.state},use_t=True)
        gap=float(np.abs(fit.fittedvalues-pure.fittedvalues).max());assert gap<1e-12
        # Only the target contrast is interpreted. Other FE covariance diagonals
        # can be numerically negative at ~0 with a rank-deficient cluster meat.
        variance=float(fit.cov_params().loc['D','D'])
        if variance<0:raise ValueError('Negative target variance')
        target_se=float(np.sqrt(variance))
        target_p=float(2*student_t.sf(abs(fit.params.D/target_se),h.state.nunique()-1))
        constraints.append({'constraint':label,'beta':float(fit.params.D),'se':target_se,
            'p_conditional_on_constraint':target_p,'max_fitted_difference':gap})
        params=fit.params.to_dict();params[f'm_{omitted}']=0.;params['beta']=params.pop('D');allocation[label]=params
    fixed=[]
    for b in [-.1,0,.04599196022827533,.1]:
        nuisance=np.linalg.lstsq(F,y-b*h.D,rcond=None)[0]
        pred=F@nuisance+b*h.D
        gap=float(np.max(np.abs(pred-pure.fittedvalues)));assert gap<1e-12
        fixed.append({'imposed_beta':b,'max_fitted_difference':gap,'rss':float(np.sum((y-pred)**2))})
    windows=[(20120007,20130006),(20140007,20150006),(20150007,20160006),(20170007,20180006)]
    coverage=pd.DataFrame([[int((mask&h.date2.between(lo,hi)).sum()) for lo,hi in windows]
         for mask in [h.treat4.eq(1),h.state.eq('CdMex'),h.state.eq('Puebla')]],
         index=['Long-term','Mexico City','Puebla'],
         columns=['Jul12-Jun13','Jul14-Jun15','Jul15-Jun16','Jul17-Jun18'])
    minimal=h[['state','date2','D']].copy()
    hypothetical=pd.concat([minimal,pd.DataFrame([{'state':'CdMex','date2':20170007,'D':0.}])],ignore_index=True)
    actual=data.loc[data.state.eq('Puebla')&data.date2.eq(20140007)].copy();actual['D']=actual.D_long
    restored=pd.concat([minimal,actual[['state','date2','D']]],ignore_index=True)
    assert len(actual)==5 and ranks(restored)==[59,60] and ranks(hypothetical)==[59,60]
    return {'N':len(h),'clusters':h.state.nunique(),'ranks':ranks(h),'identity_mismatches':mismatch,
            'cycles':cycles,'extra_constraints':constraints,'imposed_beta_checks':fixed,
            'restored_actual_N':len(actual),'restored_ranks':ranks(restored),
            'hypothetical_ranks':ranks(hypothetical),'pure_FE_june2016':float(pure.params['m_20160006'])},h,coverage,allocation

def short_extension(data,source):
    rows=[]
    for label,exclude in [('Full sample',None),('Exclude Mexico City','CdMex'),('Exclude Puebla','Puebla')]:
        frame=data.loc[data.D_short.notna()]
        if exclude:frame=frame.loc[frame.state.ne(exclude)]
        r=FixedEffectsDesign(frame).fit('D_short',wild=True);r['comparison']=label;rows.append(r)
    table,joint=placebo_checks(data,source,'treat2',wild=True)
    assert np.isclose(rows[0]['b'],-.019597792144748865) and rows[0]['wild_p']==.0625
    assert len(table)==33 and table.p.lt(.05).sum()==6 and np.isclose(joint,.1171875)
    return {'comparisons':rows,'placebo_count':len(table),'conventional_significant':int(table.p.lt(.05).sum()),
            'joint_max_abs_t_p':joint},table

def alternative_specifications(h):
    rows=[]
    states=pd.get_dummies(h.state,drop_first=False,dtype=float)
    year=(h.date2//10000).astype(int)
    years=pd.get_dummies(year,drop_first=True,dtype=float)
    trend=(h.date2//10000)*12+h.date2.mod(100)
    trend=(trend-trend.mean())/12
    specs=[('Original: state + month-year FE',fe_matrix(h).to_numpy()),
           ('State FE only',states.to_numpy()),
           ('State + calendar-year FE',np.column_stack([states,years])),
           ('State FE + common linear trend',np.column_stack([states,trend])),
           ('State FE + state-specific linear trends',np.column_stack([states,states.to_numpy()*trend.to_numpy()[:,None]]))]
    for name,F in specs:
        x=h.D.to_numpy();xr=x-F@np.linalg.lstsq(F,x,rcond=None)[0]
        rank=int(np.linalg.matrix_rank(F));identified=bool(xr@xr>1e-10)
        row={'specification':name,'identified':identified,'rank_controls':rank,
             'rank_controls_D':rank+int(identified),'residual_D_ss':float(xr@xr),
             'beta':None,'se':None,'p':None}
        if identified:
            fit=sm.OLS(h.particularistic,np.column_stack([F,x])).fit(cov_type='cluster',
                 cov_kwds={'groups':h.state},use_t=True)
            variance=float(fit.cov_params().iloc[-1,-1])
            if variance<0:raise ValueError('Negative target variance')
            target_se=float(np.sqrt(variance));b=float(fit.params.iloc[-1])
            row.update(beta=b,se=target_se,p=float(2*student_t.sf(abs(b/target_se),h.state.nunique()-1)))
        rows.append(row)
    return rows

def clean_json(obj):
    if isinstance(obj,dict):return {str(k):clean_json(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [clean_json(v) for v in obj]
    if isinstance(obj,np.generic):return clean_json(obj.item())
    if isinstance(obj,float) and not np.isfinite(obj):return None
    return obj

def save_json(name,record):
    output=ROOT/'output';output.mkdir(exist_ok=True)
    (output/name).write_text(json.dumps(clean_json(record),ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def plot_style():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    names={f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family':'Times New Roman' if 'Times New Roman' in names else 'DejaVu Serif',
        'mathtext.fontset':'stix','figure.dpi':130,'axes.spines.top':False,'axes.spines.right':False})
    return plt
