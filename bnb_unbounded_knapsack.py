import math


class BnB:
    def __init__(self, W, w, v) -> None:
        self.W = W
        self.w = w
        self.v = v
        self.n = len(v)
        

    def eliminate(self):
        self.N = [i for i in range(self.n)]
    
        for j in range(0, len(self.N)-1):
            k = j+ 1
            while k < len(self.N):
                wk = self.w[self.N[k]]
                wj = self.w[self.N[j]]
                vk = self.v[self.N[k]]
                vj = self.v[self.N[j]]
                if math.floor(wk/wj)*vj >= vk:  
                    self.N.pop(k)
                elif  math.floor(wj/wk)*vk >= vj:
                    self.N.pop(j)
                    break  # k = |N| means udah sampe akhir rangenya
                else:
                    k = k + 1
                    
    def intialize(self):
        self.eliminate()
        # sort the non-dominated items according to decreasing vi/wi ration
        self.N = sorted(self.N, key=lambda i: self.v[i]/self.w[i], reverse= True)
        self.w = [self.w[i] for i in self.N]
        self.v = [self.v[i] for i in self.N]
        print("After Sorting:")
        print(self.N)
        print("val   :", self.v)
        print("weight:", self.w)
        self.M =  [[0] * (self.W) for _ in range(len(self.N))]
        self.x_topi = [0 for _ in range(len(self.N))]
        self.x = [0 for _ in range(len(self.N))]
        self.i = 0
        self.z_topi = 0

        v1, w1 = self.v[self.i], self.w[self.i]
        self.x[0] = math.floor(self.W/w1)
        self.vn = v1*self.x[0]
        self.W_aksen = self.W - self.x[0] * w1

        self.U = self.upperbound()
        self.m = []
        for i in range(len(self.N)):
            min_value = float('inf')
            for j in range(i+1, len(self.N)):
                if self.w[j] < min_value:
                    min_value = self.w[j]
            self.m.append(min_value)
        print(self.m)
        self.develop()

    def upperbound(self):
        v1, w1 = self.v[self.i], self.w[self.i]
        v2, w2 = self.v[self.i+1], self.w[self.i+1]
        v3, w3 = self.v[self.i+2], self.w[self.i+2]
        if self.i + 2 < self.n:

            z_aksen = math.floor(self.W/w1)*v1 + math.floor(self.W_aksen/w2)*v3
            W_aksen_dua = self.W_aksen - math.floor(self.W_aksen/w2)*w2
            U_aksen = z_aksen + math.floor(W_aksen_dua*v3/w3)

            tmp = math.floor((W_aksen_dua + math.ceil(1/w1*(w2)-W_aksen_dua)
                             * v2/w2)-math.ceil(1/w1*(w2-W_aksen_dua)*v1))

            U_aksen_dua = z_aksen + tmp

            U = max(U_aksen, U_aksen_dua)

        else:
            U = self.vn
            
        return U

    def develop(self):
        if self.W_aksen < self.m[self.i]:
            if self.z_topi < self.vn:
                self.z_topi = self.vn
                self.x_topi = self.x.copy()
                if self.z_topi == self.U:
                    # finish
                    print("1. Result at Develop: ", self.z_topi, self.x_topi)
                    self.result()
            # backtrack 
            print("2. Develop Go to Step 3 Backtrack, ", self.x, self.i, self.vn, self.W_aksen, self.z_topi, self.x_topi)
            self.backtrack()
            
        else:
            min_j = min((j for j in range(self.i + 1, len(self.N)) if self.w[j] <= self.W_aksen), default=None)
            if (min_j is None) or (self.vn + self.upperbound() <= self.z_topi):
                print("3. Develop Go to Step 3 Backtrack")
                self.backtrack()
            if self.M[self.i][self.W_aksen] >= self.vn:
                print("4. Develop Go to Step 3 Backtrack")
                self.backtrack()
            self.x[min_j] = math.floor(self.W_aksen/self.w[min_j])
            self.vn += self.v[min_j]*self.x[min_j]
            self.W_aksen -= self.w[min_j] * self.x[min_j]
            self.M[self.i][self.W_aksen] = self.vn 
            self.i = min_j
            print("5. Develop Go Back at Develop")
            self.develop()

    def backtrack(self):
        j = max((j for j in range(self.i + 1) if self.x[j] > 0), default=None)
      
        if j is None:
            print("1. Backtrack Result: ", self.z_topi, self.x_topi)
            self.result()
            
        self.i = j
        self.x[self.i] -= 1
        self.vn -= self.v[self.i]
        self.W_aksen += self.w[self.i]
    
        if self.W_aksen < self.m[self.i]:
            print("2. Backtrack, ", self.x, self.i, self.vn, self.W_aksen, self.z_topi, self.x_topi) 
            self.backtrack()
        if self.vn + math.floor(self.W_aksen* self.v[self.i+1] / self.w[self.i+1]) <= self.z_topi:
            self.vn -= self.v[self.i] * self.x[self.i]
            self.W_aksen += self.w[self.i] * self.x[self.i]
            self.x[self.i] = 0
            print("3. Backtrack, ", self.x, self.i, self.vn, self.W_aksen, self.z_topi, self.x_topi) 
            self.backtrack()
        if self.W_aksen  >= self.m[self.i]:
            print("4. Backtrack Go To Develop")
            self.develop()
        self.replace(self.i, self.i+1)

    def replace(self, j, h):

        if self.z_topi >= self.vn + math.floor(self.W_aksen * self.v[h] / self.w[h]):
            print("1. Replace back to backtrack")
            self.backtrack()
            
        if self.w[h] >= self.w[j]:
            if self.w[h] == self.w[j] or self.w[h] > self.W_aksen or self.z_topi >= self.vn + self.v[h]:
                h = h + 1
                self.replace(j,h)
            self.z_topi = self.vn + self.v[h]
            self.x_topi = self.x
            self.x[h] = 1

            if self.z_topi == self.U:
                print("2. Result at replace: ", self.z_topi, self.x_topi)
                self.result()

            j = h
            h = h+1
            print("3. Replace back to replace")
            self.replace(j, h)
        else:
            if self.W_aksen - self.w[h] < self.m[h-1]:
                h = h+1
                print("3. Replace back to replace")
                self.replace(j,h)
            self.i = h
            self.x[self.i] = math.floor(self.W_aksen/self.w[self.i])
            self.vn += self.v[self.i]*self.x[self.i]
            self.W_aksen -= self.w[self.i]*self.x[self.i]
            print("4. Replace back to develop")
            self.develop()
    def result(self):
        print("Best Value: ", self.z_topi)
        print("Best Solution: ", self.x_topi)
        exit()


if __name__ == '__main__':
  
    file_path = "Datasets/dataset_100.txt"


    with open(file_path, 'r') as file:
        lines = file.readlines()

        wt = (lines[1].split())
        wt = [int(i) for i in wt]
        val = (lines[3].split())
        val = [int(i) for i in val]
           
        print("wt[]:", wt)
        print("val[]:", val)
        W = int(0.1 * sum(wt))
        print(W)
        
            
        bnb = BnB(W, wt, val)
        res, a = (bnb.intialize())



          
        