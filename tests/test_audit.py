from pathlib import Path
import importlib.util,sys,tempfile,unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
from audit_lib import load_inputs,baselines,h2_audit,alternative_specifications

class IdentificationExamples(unittest.TestCase):
    def test_full_2x2_has_independent_treatment(self):
        state=np.array([1,1,0,0]);time=np.array([0,1,0,1]);D=state*time
        F=np.column_stack([np.ones(4),state,time])
        self.assertEqual(np.linalg.matrix_rank(F),3)
        self.assertEqual(np.linalg.matrix_rank(np.column_stack([F,D])),4)
    def test_missing_control_post_destroys_independence(self):
        state=np.array([1,1,0]);time=np.array([0,1,0]);D=state*time
        F=np.column_stack([np.ones(3),state,time])
        self.assertEqual(np.linalg.matrix_rank(F),np.linalg.matrix_rank(np.column_stack([F,D])))

class DownloadIntegrity(unittest.TestCase):
    def test_corrupt_file_is_rejected(self):
        spec=importlib.util.spec_from_file_location('download',ROOT/'data/download.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'source.csv';p.write_text('not the source',encoding='utf-8')
            with self.assertRaises(ValueError):module.verify(p,'0'*64)

@unittest.skipUnless((ROOT/'data/raw/allres.csv').is_file(),'Download official data first')
class OriginalDataChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data,cls.source=load_inputs()
    def test_baseline_replication(self):
        results=baselines(self.data)
        self.assertAlmostEqual(results[0]['b'],.01525336444865884,places=10)
        self.assertAlmostEqual(results[1]['b'],.02623265672428348,places=10)
    def test_h2_nonidentification_and_invariant_fits(self):
        result,h,_,_=h2_audit(self.data,self.source)
        self.assertEqual(result['N'],1511);self.assertEqual(result['ranks'],[59,59])
        self.assertEqual(result['identity_mismatches'],0)
        self.assertTrue(all(x['max_fitted_difference']<1e-12 for x in result['imposed_beta_checks']))
        self.assertEqual(result['restored_ranks'],[59,60])
        self.assertFalse(alternative_specifications(h)[0]['identified'])
    def test_coarser_year_effects_do_not_restore_identification(self):
        _,h,_,_=h2_audit(self.data,self.source)
        models=alternative_specifications(h)
        self.assertFalse(models[2]['identified'])
        self.assertTrue(models[1]['identified'])
if __name__=='__main__':unittest.main()
