# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.
# Notes:
# - benchmarks may be organised into methods of classes if desired
#   (or just as functions that start with "time_")

# ------------------------------------
# Runtime benchmarks start with 'time' 
# (snake case or camelcase)
# ------------------------------------
class TimeSuite:
    """
    An example benchmark that times the performance of various kinds
    of iterating over dictionaries in Python.
    """
    def setup(self):
        """
        Setup includes initialisation bits that should not be included
        in the timing of the benchmark.

        It can be added as:
         - a method of a class, or
         - an attribute of a free function, or
         - a module-level setup function (run for every benchmark in the
           module, prior to any function-specific setup)

        If setup raises `NotImplementedError`, the benchmark is skipped
        """
        self.d = {}
        for x in range(500):
            self.d[x] = None

    def setup_cache(self):
        """
        `Setup_cache` only performs the setup calculation once
        (for each benchmark and each repeat) and caches the
        result to disk. This may be useful if the setup is
        expensive.

        A separate cache is used for each environment and each commit.
        The cache is thrown out between benchmark runs.

        There are two options to persist the data for the benchmarks:
        - `setup_cache` returns a data structure, which asv pickles to disk,
          and then loads and passes as first arg to each benchmark (not 
          automagically tho), or
        - `setup_cache` saves files to the cwd (which is a temp dir managed by
          asv), which are then explicitly loaded in each benchmark. Recomm
          practice is to actually read the data in a `setup` fn, so that 
          loading time is not part of the timing 
        """
        pass

    def teardown(self):
        """
        Benchmarks can also have teardown functions that are run after
        the benchmark. The behaviour is similar to setup fns. 

        Useful for example to clean up changes made to the
        filesystem
        """
        pass

    def time_keys(self):
        # benchmark attributes
        timeout = 123 # The amount of time, in seconds, to give the benchmark to run before forcibly killing it. Defaults to 60 seconds.
        pretty_name = 'pretty name'
        setup = setup
        teardown = teardown
        rounds = 2
        repeat = (1, 5, 10.0)
        warmup_time = 0.1
        # params_names
        # params ---> the params attribute allows us to run a single benchmark
        # for multiple values of the parameters
        
        for key in self.d.keys():
            pass

    def time_values(self):
        # For best results, the benchmark function should contain 
        # as little as possible, with as much extraneous setup moved to a setup function:
        for value in self.d.values():
            pass

    def time_range(self, n):
        d = self.d
        for key in range(500):
            x = d[key]

# -----------------------
# Parametrized benchmarks
# -------------------------
# - params can be any Python object, but it is recommended
#   only strings and number
# - w/ multiple params, the test is run for all combs
class Suite:
    params = [0, 10, 20]
    param_names = ['n']

    def setup(self, n):
        # Note that setup_cache is not parametrized (can it?)
        self.obj = range(n)

    def teardown(self, n):
        del self.obj

    def time_range_iter(self, n):
        for i in self.obj:
            pass


# ------------------------------------
# Memory benchmarks start with 'mem' 
# (snake case or camelcase)
# ------------------------------------
class MemSuite:
    def mem_list(self):
        return [0] * 256
