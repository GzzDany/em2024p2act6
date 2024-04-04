### Misc functions: 
def make_argument_combinations(d_choices):
    """Takes a dictionary where the keys are parameter names, and the values are lists of choices for
    those parameters and returns a list of dictionaries of every combinations of those parameters. 
    
    Parameters:
        d_choices dict{str:list[any]}: a dictionary where keys are strings representing parameter names, and the
            values are lists containing possible choices for those parameters. 
    
    Returns:
        input_args list[dict{str:any}]: the product of all combinations of choices of parameter values provided. 
    """
    from itertools import product
    combinations = product(*d_choices.values())
    input_args = []
    for combo in combinations:
        input_args.append(dict(zip(d_choices.keys(), combo)))
    return input_args

def generate_random_number(seed_value=None, min_num=1, max_num=20):
    """This function generates random numbers between min_num and max_num using a Linear Congruential Generator.
    
    Sets the value of a global variable seed for reproducibility. 
    
    Parameters:
        seed_value (default=None): if provided, sets the global variable to seed_value. Else, checks if
            the global variable "seed" exists. If it doesn't, it sets a value to it. If it exists,
            it uses that value. After generating the random number, it updates the seed value. 
        min_num (int, default=1): the random number lower-bound.
        max_num (int, default=20): the random number upper-bound. 
    
    Returns:
        rand_num (int): a random number between min_num and max_num (both inclusive)
        """
    global seed
    if "seed" not in globals():
        # set a default initial seed value. 
        try:
            import getpass
            username= getpass.getuser()
            seed = int(username[-5:])
        except:
            seed = 92572
    if seed_value is not None:
        seed = seed_value
    mod = 2**31-1
    seed = (16807*seed)%mod
    return int((seed-min_num)/(mod-(min_num-1))*(max_num+1))

def get_seed_value_pairs(rand_gen_func, num_results):
    """When a function has a random number generator, this function can be used to find seed values
    that produce specific results for testing. 
    
    Parameters:
        rand_gen_func (function): a random number generator function. 
        num_results (int): amount of results:seed_value pairs required. Ensure the random number generator
            has at least this range of numbers to generate. 
    
    Returns:
        d_results (dict{(result):int}): A dictionary with key values results obtained from the function, and
            values corresponding to seeds that produced those results. 
    """
    global seed
    if "seed" not in globals():
        # set a default initial seed value. 
        seed = 7930248
    d_results = {}
    while True:
        old_seed = seed
        rand = rand_gen_func()
        if rand not in d_results.keys():
            d_results[rand] = old_seed
        if len(d_results) == num_results:
            break
    return d_results


### Import solution functions:
def get_function(act_name, func_name):
    # text = "from hidden_tests_" + act_name + " import sol_" + func_name
    import importlib
    module = importlib.import_module("em2024p2act5.hidden_tests_"+act_name)
    return getattr(module, "sol_"+func_name)

def get_input(act_name, func_name):
    # text = "from hidden_tests_" + act_name + " import input_" + func_name
    import importlib
    module = importlib.import_module("em2024p2act5.hidden_tests_"+act_name)
    return getattr(module, "input_"+func_name)()

def error_message_simple(expected_output, real_output, func_name, arg_name=False, **args):
    """This function generates error messages for simple functions (no interaction) given
    their expected and real output. 
    
    Parameters:
        expected_output (int, float, str): The expected correct function output. Either a return value or more complicated 
            messages.
        real_output (int, float, str): The output obtained from the student code function. 
        func_name (str): The name of the function to include it in the message. 
        arg_name (boolean, default=False): Whether to include parameter names in the error message. 
            Example: "Calling foo(x=1) ..." when True or "Calling foo(1)..." when False. 
    
    Returns:
        text (str): Error message that can easily be read to compare expected and real outputs. 
        """
    if args:
        for keyword, value in args.items():
            if type(value) == str:
                args[keyword] = '"' + value + '"'
        if arg_name:
            arg_text = [str(key)+"="+str(value) for key, value in args.items()]
        else:
            arg_text = [str(value) for value in args.values()]
        arg_text = ", ".join(arg_text)
    text = f'\nCalling {func_name}({arg_text}) returned: \n{real_output} \n\nExpected: \n{expected_output}'
    return text

def compare_returns(act_name, func_name, global_vars, arg_name=False):
    """Compares the return values of the student function and solution function, assuming the solution function is 
    found in the appropriate module and is appropriately named. This assumes the student function is localed in "globals()" within the 
    kernel where this function will be called. 
    This also assumes there is a function that generates the input argument test cases appropriately named like:
        input_[func_name]
    
    Parameters:
        act_name (str): The name of the activity
        func_name (str): The name of the function to assess 
        error_generator: A function that generates the appropriate error message
        arg_name (boolean, default=False): Whether to include parameter names in the error message. 
            Example: "Calling foo(x=1) ..." when True or "Calling foo(1)..." when False. 
    
    Returns:
        None
    
    Prints out assertion errors with the appropriate messages when the outputs of the two functions
    don't match EXACTLY. 
    """
    test_input, input_args = get_input(act_name, func_name)
    sol_func = get_function(act_name, func_name)
    func = global_vars[func_name]
    for arg in input_args:
        expected_output = sol_func(**arg)
        real_output = func(**arg)
        assert expected_output == real_output, error_message_simple(expected_output, real_output, func_name, arg_name=arg_name, **arg)
    return

### For interactive functions: 
from contextlib import redirect_stdout
from io import StringIO
import builtins
import sys

class PatchedInput:
    def __init__(self, input_values):
        self.input_values = input_values
        self.input_copy = input_values.copy()
        self.original_input = builtins.input
        self.original_output = sys.stdout
        self.captured_lines = []
        self.captured_io = StringIO()
        self.input_lines = []
        self.output_lines = []
        self.failed_to_end = False
        self.ended_soon = False
        
    def __enter__(self):
        builtins.input = self.custom_input
        sys.stdout = self.captured_io
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.input_values:
            print("FUNCTION SHOULD HAVE CONTINUED, BUT INSTEAD ENDED.")
            self.ended_soon = True
        builtins.input = self.original_input
        sys.stdout = self.original_output
        self.clean_up()
    
    def custom_input(self, prompt):
        self.input_lines.append(prompt)
        self.captured_lines.append(prompt)
        print(prompt, end='\n')
        if self.input_values:
            return self.input_values.pop(0)
        else:
            print("THE FUNCTION SHOULD HAVE ENDED HERE, BUT INSTEAD CONTINUED.")
            self.failed_to_end = True
            self.__exit__
    
    def clean_up(self):
        self.captured_lines = self.captured_io.getvalue().splitlines()
        if self.failed_to_end:
            self.captured_lines = self.captured_lines[0:self.captured_lines.index("THE FUNCTION SHOULD HAVE ENDED HERE, BUT INSTEAD CONTINUED.")+1]
        i = 0
        for input_line in self.input_lines:
            try:
                self.captured_lines[self.captured_lines.index(input_line)] = input_line + self.input_copy[i]
            except:
                pass
            i += 1

def simulate_interaction(input_values, function, args={}):
    """Function that automatically interacts with an interactive function in Python given a pre-selected
        list of input values. It returns a PatchedInput instance (pi) with pi.captured_lines showing the
        full interaction, pi.failed_to_end =True in case the function did not end with the provided arguments
        and pi.ended_soon=True in case the function ended without using all provided input arguments. 
    
        Parameters:
            input_values (list[str]): The list of pre-selected input values to test the function. 
            function (func): The interactive function which takes the input values. 
            args (dict{str:any}, Optional, default:None): arguments required by the function. 
        
        """
    patched_input = PatchedInput(input_values)
    with patched_input:
        try:
            function(**args)
        except:
            return patched_input
            pass
    return patched_input

def compare_interactive_function(act_name, func_name, global_vars):
    """Function that compares the output of an interactive function to the expected output. It prints out
    an error message if the outputs don't match exactly.
    
    Parameters:
        act_name (str): The activity name
        func_name (str): The name of the tested function
            
    Returns:
        None
        
    Notes:
    Assumes there is a function called sol_[func_name] in the appropriate module
    Assumes there is a function called input_[func_name] in the appropriate module which generates a tuple:
        (list of input values (for the input function), list of parameters (list of dictionaries))
    """
    test_inputs, args = get_input(act_name, func_name)
    sol_func = get_function(act_name, func_name)
    func = global_vars[func_name]
    for input_values, arg in zip(test_inputs, args):
        ### Run the simulation to obtain expected values. 
        exp_pi = simulate_interaction(input_values.copy(), sol_func, arg)
        real_pi = simulate_interaction(input_values.copy(), func, arg)
        message = ""
        if real_pi.failed_to_end:
            message = "Your function continued after it should have ended. \n"
        if real_pi.ended_soon:
            message = "Your function ended when it shouldn't have. \n"
        exp_interaction = "\n".join(exp_pi.captured_lines)
        real_interaction = "\n".join(real_pi.captured_lines)
        assert exp_interaction == real_interaction, message + "Your function returned: \n" + real_interaction + "\n\nExpected: \n" + exp_interaction
    return
