import os

os.system("$PWD")

class SimParams(object):
    def __init__(self, n = 100, n_steps=10000, b_top = 0.5, multiprocess = True, t_min = 1.6, t_max = 3.6, t_step = 0.1):
        self.n = n
        self.n_steps = n_steps
        self.b_top = b_top
        self.multiprocess = multiprocess
        self.t_min = t_min
        self.t_max = t_max
        self.t_step = t_step
    def __str__(self):
        return f"\n\tn:{self.n}\n\tn_steps:{self.n_steps}\n\tmultiprocess:{self.multiprocess}\n\tb_top:{self.b_top}\n\tt_min:{self.t_min}\n\tt_max:{self.t_max}\n\tt_step:{self.t_step}"

def _run_raw(test_path, snapshots=False, params: SimParams = SimParams()):
    mp = "t" if params.multiprocess else "f"
    os.system(f"cd .. && python ising.py N:{params.n} multiprocess:{mp} b_top:{params.b_top} t_min:{params.t_min} t_max:{params.t_max} t_step:{params.t_step}")

def copy_results(test_path, snapshots=False):
    os.system(f"mv ../data/* {test_path}/result/")
    if snapshots:
        os.system(f"mv ../snapshots/* {test_path}/snapshots/")

def store_metadata(test_path, snapshots, n_trials, params):
    with open(f"{test_path}/metadata.txt", "w") as f:
        f.write(f"n_trials: {n_trials}\n")
        f.write(f"snapshots taken: {snapshots}\n")
        f.write(f"params: {params}\n")
        
def rerun(test_path, snapshots=False, params: SimParams = SimParams()):
    _run_raw(test_path, snapshots, params)
    copy_results(test_path, snapshots)
    store_metadata(test_path, snapshots, 1, params)
        
def run_many(test_path, n_trials, snapshots=False, params: SimParams = SimParams()):
    for i in range(n_trials):
        _run_raw(test_path, snapshots, params)
    copy_results(test_path, snapshots)
    store_metadata(test_path, snapshots, n_trials, params)

def new_test(test_path):
    os.system(f"mkdir -p {test_path}/result")
    os.system(f"mkdir -p {test_path}/snapshots")
    os.system(f"mkdir -p {test_path}/plots")

data_tests = "../data_tests"
test_name = "fit-observables/many-runs-trial-3-fixN"
test_path = f"{data_tests}/{test_name}"
n_trials = 10 # How many times to run the simulation per temperature
params = SimParams(n = 100, n_steps=100000, b_top = 0.5, multiprocess = True, t_min = 1.6, t_max = 3.6, t_step = 0.02)

if True:
    #rerun(test_path)
    new_test(test_path)
    run_many(test_path, n_trials, snapshots=False, params=params)