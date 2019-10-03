import numpy as np

class Filter():
    
    def __init__(self,prototype,ftype,w,fs):
        self.fs = fs
        self.wc = w*2*math.pi

        self.y = np.zeros((3,)) 
        self.x = np.zeros((3,))
        self.iteration = 0
        self.prototype = prototype
        self.type = ftype

        if self.prototype is "BW":
            if self.type is "LP":
                ##butterworth prototype LP
                self.a = 0
                self.b = 0
                self.c = 1
                self.d = 1/(self.wc**2)
                self.e = math.sqrt(2)/self.wc
                self.f = 1

            if self.type is "HP":
                ##butterworth prototype HP
                self.a = 1
                self.b = 0
                self.c = 0
                self.d = 1
                self.e = math.sqrt(2)*self.wc
                self.f = (self.wc**2)

        if self.prototype is "CB":

            if self.type is "LP":
                ##chebchev prototype LP
                b0 = 0.70794
                b1 = 0.6448
                e2 = 0.99526
                self.a = 0
                self.b = 0
                self.c = (b0/math.sqrt(1+e2))
                self.d = 1/(self.wc**2)
                self.e = b1/self.wc
                self.f = b0    

        self.A = self.a*4*self.fs**2 + self.b*2*self.fs + self.c
        self.B = -1*(self.a*8*self.fs**2) + 2*self.c
        self.C = self.a*4*self.fs**2 - self.b*2*self.fs + self.c
        self.D = self.d*4*self.fs**2 + self.e*2*self.fs + self.f
        self.E = -1*(self.d*8*self.fs**2) + 2*self.f
        self.F = self.d*4*self.fs**2 - 2*self.e*self.fs + self.f
 
        print("Parameters:",self.A ,self.B,self.C,self.D,self.E,self.F )

    def calc(self,newvalue):

        self.y[:-1] = self.y[1:]
        self.x[:-1] = self.x[1:]
        self.x[-1] = newvalue
        
        self.iteration += 1

        if self.iteration > 2:           
            self.y[2] = (self.A/self.D)*self.x[2] + (self.B/self.D)*self.x[1] + (self.C/self.D)*self.x[0]  - (self.E/self.D)*self.y[1] - (self.F/self.D)*self.y[0] 
        else:
            self.y[2] = newvalue

        return self.y[2]
        
