import os

os.system("$PWD")

class SimParams(object):
    def __init__(self, N = 100, n_steps=10000, n_analyze = 5000, n_burnin = 2000, b_top = 0.5, multiprocess = True, t_min = 1.6, t_max = 3.6, t_step = 0.1, n_trials = 10, snapshots = False):
        self.N = N
        self.n_steps = n_steps
        self.n_analyze = n_analyze
        self.n_burnin = n_burnin
        self.b_top = b_top
        self.multiprocess = multiprocess
        self.t_min = t_min
        self.t_max = t_max
        self.t_step = t_step
        self.n_trials = n_trials
        self.snapshots = snapshots
    def param_str(self):
        return f"N:{self.N} n_steps:{self.n_steps} n_analyze:{self.n_analyze} n_burnin:{self.n_burnin} b_top:{self.b_top} multiprocess:{'t' if self.multiprocess else 'f'} t_min:{self.t_min} t_max:{self.t_max} t_step:{self.t_step}"

def _run_raw(test_path, params: SimParams):
    #!cd .. && python ising.py N:{params.N} multiprocess:{"t" if params.multiprocess else "f"} b_top:{params.b_top} t_min:{params.t_min} t_max:{params.t_max} t_step:{params.t_step} n_steps:{params.n_steps} n_analyze:{params.n_analyze} n_burnin:{params.n_burnin}
    os.system(f"cd .. && python ising.py {params.param_str()}")

def copy_results(test_path, params: SimParams):
    os.system(f"mv ../data/* {test_path}/result/")
    if params.snapshots:
        os.system(f"mv ../snapshots/* {test_path}/snapshots/")

def store_metadata(test_path, params: SimParams):
    with open(f"{test_path}/metadata.txt", "w") as f:
        f.write(f"n_trials: {params.n_trials}\n")
        f.write(f"snapshots taken: {params.snapshots}\n")
        f.write(f"param string: {params.param_str()}\n")
    # Pickle the params object and store it into params.pkl
    with open(f"{test_path}/params.pkl", "wb") as f:
        pickle.dump(params, f)
        
def run_many(test_path, params: SimParams = SimParams()):
    for i in range(params.n_trials):
        _run_raw(test_path, params)
    copy_results(test_path, params)
    store_metadata(test_path, params)

def new_test(test_path):
    os.system(f"mkdir -p {test_path}/result")
    os.system(f"mkdir -p {test_path}/snapshots")
    os.system(f"mkdir -p {test_path}/plots")

data_tests = "../data_tests"
test_name = "fit-observables/many-runs-trial-3-fixN"
test_path = f"{data_tests}/{test_name}"
n_trials = 100 # How many times to run the simulation per temperature
params = SimParams(n = 100, n_steps=200000, b_top = 0.5, multiprocess = True, t_min = 1.6, t_max = 3.6, t_step = 0.02)

# (self, N = 100, n_steps=10000, n_analyze = 5000, n_burnin = 2000, b_top = 0.5, multiprocess = True, t_min = 1.6, t_max = 3.6, t_step = 0.1, n_trials = 10, snapshots = False)

if True:
    new_test(test_path)
    run_many(test_path, n_trials, snapshots=False, params=params)