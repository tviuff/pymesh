
import math

class CurveMeshDistributions:
    """Class with curve mesh distributions
    """

    def get_mesh_distribution_function(self, method:str=None):
        """Returns mesh distribution function based on a selected method.
        Available methods are:
            'linear'     : points spaced as a linear function
            'cosine_both': points spaced as a cosine function at both ends
            'cosine_end1': points spaced as a cosine function at end1
            'cosine_end2': points spaced as a cosine function at end2
        """
        available_methods = {
            "linear" : self.linear(),
            "cosine_both" : self.cosine_both(),
            "cosine_end1" : self.cosine_end1(),
            "cosine_end2" : self.cosine_end2(),
            }
        if not isinstance(method, str):
            raise TypeError("method must be of type 'str'.")
        if method is None:
            method = "linear"
        for mth, func in available_methods.items():
            if mth == method:
                return func
        raise ValueError("Selected method unknown.")

    def linear(self):
        """Points spaced as a linear function.
        Function: f(u) = u
        """
        return lambda u: u

    def cosine_both(self):
        """Points spaced as a cosine function.
        Function: f(u) = cos((1 - u)*pi)/2 + 0.5
        """
        return lambda u: math.cos((1 - u)*math.pi)/2 + 0.5

    def cosine_end1(self):
        """Points spaced as a cosine function.
        Function: f(u) = 1 - cos(u*pi/2)
        """
        return lambda u: 1 - math.cos(u*math.pi/2)

    def cosine_end2(self):
        """Points spaced as a cosine function.
        Function: f(u) = cos((u - 1)*pi/2)
        """
        return lambda u: math.cos((u - 1)*math.pi/2)
