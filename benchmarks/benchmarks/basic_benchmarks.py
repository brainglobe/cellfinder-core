class TimeSuiteBasic:
    params = [0, 10, 100, 1000]
    param_names = ['n']

    def setup(self, n):
        self.d = {}
        for x in range(n):
            self.d[x] = None

    def time_keys(self, n):  # why do I need to pass parameter here?
        for ky in self.d.keys():
            pass

    def time_values(self, n):
        for val in self.d.values():
            pass

    def teardown(self, n):
        pass