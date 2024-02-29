"""Module including surface classes
"""

class CoonsPatch:
    """Not yet working properly
    """
    def __init__(self, Line1, Line2, Line3, Line4):
        self.pu0 = pu0
        self.pu1 = pu1
        self.p0w = p0w
        self.p1w = p1w
        assert (Line1.P1 == Line2.P0).all(), f'ERROR: pu0 and p1w does not share intersection point!'
        assert (Line2.P1 == Line3.P0).all(), f'ERROR: pu1 and p1w does not share intersection point!'
        assert (Line3.P1 == Line4.P0).all(), f'ERROR: pu1 and p0w does not share intersection point!'
        assert (Line1.P0 == Line4.P1).all(), f'ERROR: pu0 and p0w does not share intersection point!'
        self.p00 = Line1.P0# pu0[0,:]
        self.p01 = Line3.P0# pu1[0,:]
        self.p10 = Line2.P1# p1w[0,:]
        self.p11 = Line4.P1# pu1[-1,:]

    def get_points(self, method="linear"):
        assert (method == "linear" or method == "cosine"), f"method {method} is not 'linear' or 'cosine'."
        if method == "linear":
            return self.__get_points_linear()
        if method == "cosine":
            print('Cosine method not yet implemented!')

    def __get_points_linear(self, Nu, Nw):
        pu0 = self.Line1.getpoints(Nu)
        pu1 = self.Line2.getpoints(Nu)
        p0w = self.Line3.getpoints(Nw)
        p1w = self.Line4.getpoints(Nw)
        p = np.zeros((3, Nu, Nw))
        for i, u in enumerate(np.linspace(0, 1, num=self.Nu, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=self.Nw, endpoint=True)):
                p1 = (1-u)*self.p0w[j,:] + u*self.p1w[j,:]
                p2 = (1-w)*self.pu0[i,:] + w*self.pu1[i,:]
                p3 = (1-u)*(1-w)*self.p00 + u*(1-w)*self.p10 + (1-u)*w*self.p01 + u*w*self.p11
                for k in range(0, 3):
                    p[k,i,j] = p1[k] + p2[k] - p3[k]
        return p
