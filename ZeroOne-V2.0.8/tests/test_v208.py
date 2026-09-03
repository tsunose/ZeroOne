import subprocess, sys, textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; ZO=ROOT/'zo.py'
def run(src):
 f=ROOT/'tests/_tmp_v208.zo'; f.write_text(src); p=subprocess.run([sys.executable,str(ZO),'run-source',str(f)],text=True,capture_output=True,cwd=ROOT); f.unlink(missing_ok=True); return p.returncode,p.stdout,p.stderr
def test_unsigned_shift():
 c,o,e=run('OUT(-8 >> 1)\nOUT("|")\nOUT(-8 >>> 1)\n'); assert c==0,e; assert o.strip()=='-4|9223372036854775804'
def test_add_type_error_is_vm_error():
 c,o,e=run('OUT(1 + "a")\n'); assert c!=0; assert 'TypeError' not in e; assert 'VMError' in e or 'ADD type error' in e
def test_multiline_array():
 c,o,e=run('SET arr = [\n  1,\n  2,\n  3\n]\nOUT(arr)\n'); assert c==0,e; assert '[1, 2, 3]' in o
def test_class_new_and_bound_method():
 src=textwrap.dedent('''\
CLASS Counter
FUNC init(self, value)
 SET self.value = value
END
FUNC add(self, amount)
 SET self.value = self.value + amount
 RETURN self.value
END
END
SET c = NEW Counter(10)
OUT(c.add(5))
OUT("|")
OUT(c.value)
'''); c,o,e=run(src); assert c==0,e; assert o.strip()=='15|15'
