class TabuSearch:
    def __init__(self, init_solution, critical_path, max_iter, tabu_list_length):
        self.init_solution = copy.deepcopy(init_solution)
        self.best_solution = copy.deepcopy(init_solution)
        self.max_iter = max_iter
        self.tabu_list = [0]*tabu_list_length

    def search(self):
        print()