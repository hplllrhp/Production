import numpy as np

def matrix_trans(matrix):
    return [[row[col] for row in matrix] for col in range(len(matrix[0]))]

#假定seq_len = 7#队列长度72
#input_size = 1#输入大小
#hidden_size_a = 14#隐藏大小
class LSTMPopulation(object):
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size#输入训练数据的纬度-1
        self.hidden_size = hidden_size#隐藏层矩阵的纬度—7
        #WLSTM:9x28的矩阵，元素值都很小
        self.WLSTM = np.random.randn(1 + input_size + hidden_size, 4 * hidden_size) / np.sqrt(input_size + hidden_size)
        self.WLSTM[0,:] = 0#将第一行置0
        self.WpeepIFO = np.ones((3, hidden_size))#3x7的矩阵的单位矩阵
        self.c0 = np.zeros((self.hidden_size))#1行7列的0矩阵
        self.h0 = np.zeros((self.hidden_size))#1行7列的0矩阵
        self.dcn = np.zeros((self.hidden_size))#1行7列的0矩阵
        self.dhn = np.zeros((self.hidden_size))#1行7列的0矩阵
        self.mWLSTM = np.zeros_like(self.WLSTM)#跟WLSTM:9x28的矩阵一样纬度的0矩阵
        self.mWpeepIFO = np.zeros_like(self.WpeepIFO)#跟3x7的矩阵一样纬度的0矩阵
    #复位状态函数
    def reset_states(self):
        self.c0 = np.zeros((self.hidden_size))#复位为0矩阵
        self.h0 = np.zeros((self.hidden_size))#复位为0矩阵
        self.dcn = np.zeros((self.hidden_size))#复位为0矩阵
        self.dhn = np.zeros((self.hidden_size))#复位为0矩阵
        print ("Network states RESET")#每调用一次打印一次该语句
        
    def forward(self, X):
        """
        X is the input (n,input_size). n = length of sequence, and input_size = input size (input dimension)
        """
#        n = X.shape[0]#返回矩阵的行数7
        n = len(X)
        #X是一个7x1的矩阵
        # (LSTM前向传播从这里开始)LSTM forward pass begins here
        xphpbias = self.WLSTM.shape[0] # xphpbias = WLSTM的行数-9
        self.Hin = np.zeros((n, xphpbias))#7x9的矩阵
        self.Hout = np.zeros((n, self.hidden_size))#7*7的矩阵
    
        self.IFOA = np.zeros((n, self.hidden_size * 4)) #7*28的矩阵before non-linearlity
        self.IFOA_f = np.zeros((n, self.hidden_size * 4)) #7*28的矩阵after the non-linearity
        self.C = np.zeros((n, self.hidden_size)) #7*7的矩阵Cell values/ cell contents
        #循环7次
        for t in range(n):
            prev_h = self.Hout[t-1,:] if (t > 0) else self.h0
            prev_c = self.C[t-1,:] if (t>0) else self.c0
            self.Hin[t,0] = 1 # this is for the bias
            self.Hin[t,1:1+self.input_size] = X[t][0]
            self.Hin[t,1+self.input_size:] = prev_h
            # Computing all gate activations 

            self.IFOA[t,:] = self.Hin[t,:].dot(self.WLSTM)
            # Adding peephole weights connections
            self.IFOA[t,:self.hidden_size] = self.IFOA[t,:self.hidden_size] + np.multiply(prev_c, self.WpeepIFO[0,:])       # input gate - adding peephole connections
            self.IFOA[t,self.hidden_size:2*self.hidden_size] = self.IFOA[t,self.hidden_size:2*self.hidden_size] + np.multiply(prev_c, self.WpeepIFO[1,:])       # forget gate - adding peephole connections
            
            # Passing through the non-linearities - sigmoid for gates input and forget - output is below due to peephole connections 
            self.IFOA_f[t,0:2*self.hidden_size] = 1.0 / (1.0 + np.exp(-self.IFOA[t,0:2*self.hidden_size]))
            self.IFOA_f[t,3*self.hidden_size:] = np.tanh(self.IFOA[t,3*self.hidden_size:]) # tanh non-linearity for the A gate (before the multiplicated input to the cell)
            
            # Computing the cell activation            
            self.C[t,:] = self.IFOA_f[t,self.hidden_size:2*self.hidden_size]*prev_c + self.IFOA_f[t,:self.hidden_size]*self.IFOA_f[t,3*self.hidden_size:]

            # Computing the output gate with peephole connections
            self.IFOA[t,2*self.hidden_size:3*self.hidden_size] = self.IFOA[t,2*self.hidden_size:3*self.hidden_size] + np.multiply(self.C[t,:], self.WpeepIFO[2,:]) # output gate - adding peephole connections            
            
            self.IFOA_f[t,2*self.hidden_size:3*self.hidden_size] = 1.0 / (1.0 + np.exp(-self.IFOA[t,2*self.hidden_size:3*self.hidden_size]))
            self.Hout[t,:] = self.IFOA_f[t,2*self.hidden_size:3*self.hidden_size]*np.tanh(self.C[t,:])
        
        self.c0 = self.C[t,:]
        self.h0 = self.Hout[t,:]
        
        
    def backward(self, dHout_temp):               
        # backprop through the LSTM now
        self.dIFOA = np.zeros_like(self.IFOA)
        self.dIFOA_f = np.zeros_like(self.IFOA_f)
        self.dWLSTM = np.zeros_like(self.WLSTM)
        self.dWpeepIFO = np.zeros_like(self.WpeepIFO)
        self.dC = np.zeros_like(self.C)
        self.dHout = dHout_temp.copy()
        self.dHin = np.zeros_like(self.Hin)
        self.dh0 = np.zeros((self.hidden_size))
        
        n = self.Hin.shape[0]
        
        if self.dcn is not None: self.dC[n-1] += self.dcn.copy()
        if self.dhn is not None: self.dHout[n-1] += self.dhn.copy()
        
#        print(dHout.shape, C.shape)
        for t in reversed(range(n)):
            self.dIFOA_f[t,2*self.hidden_size:3*self.hidden_size] = self.dHout[t,:]*np.tanh(self.C[t,:]) # backprop in to output gate
            # backprop through the tanh non-linearity to get in to the cell, then will continue through it
            self.dC[t,:] += (self.dHout[t,:] * self.IFOA_f[t,2*self.hidden_size:3*self.hidden_size]) * (1 - np.tanh(self.C[t,:]**2))
                     
            if (t>0):
                self.dIFOA_f[t,self.hidden_size:2*self.hidden_size] = self.dC[t,:]*self.C[t-1,:] # backprop in to the forget gate
                self.dC[t-1,:] += self.IFOA_f[t,self.hidden_size:2*self.hidden_size] * self.dC[t,:] # backprop through time for C (The recurrent connection to C from itself)
            else:
                self.dIFOA_f[t,self.hidden_size:2*self.hidden_size] = self.dC[t,:]*self.c0 # backprop in to forget gate
                self.dc0 = self.IFOA_f[t,self.hidden_size:2*self.hidden_size] * self.dC[t,:]
            
            self.dIFOA_f[t,:self.hidden_size] = self.dC[t,:]*self.IFOA_f[t,3*self.hidden_size:] #backprop in to the input gate
            self.dIFOA_f[t,3*self.hidden_size:] = self.dC[t,:]*self.IFOA_f[t,:self.hidden_size] #backprop in to the a gate                    

            # backprop through the activation functions
            # for input, forget and output gates - derivative of the sigmoid function
            # for a - derivative of the tanh function                
            
            self.dIFOA[t,3*self.hidden_size:] =  self.dIFOA_f[t,3*self.hidden_size:] * (1 - self.IFOA_f[t,3*self.hidden_size:]**2)              
            y = self.IFOA_f[t,:3*self.hidden_size]
            self.dIFOA[t,:3*self.hidden_size] = (y*(1-y)) * self.dIFOA_f[t,:3*self.hidden_size] 
        
            # backprop the input matrix multiplication            
            self.dWLSTM += np.dot(self.Hin[t:t+1,:].T, self.dIFOA[t:t+1,:])
            self.dHin[t,:] = self.dIFOA[t,:].dot(self.WLSTM.T) 
            
            # backprop the peephole connections
            if t>0:
                self.dWpeepIFO[0,:] += np.multiply(self.dIFOA[t,:self.hidden_size], self.C[t-1,:])
                self.dWpeepIFO[1,:] += np.multiply(self.dIFOA[t,self.hidden_size:2*self.hidden_size], self.C[t-1,:])  
                self.dWpeepIFO[2,:] += np.multiply(self.dIFOA[t,2*self.hidden_size:3*self.hidden_size], self.C[t,:]) 
            else:
                self.dWpeepIFO[0,:] += np.multiply(self.dIFOA[t,:self.hidden_size], self.c0)
                self.dWpeepIFO[1,:] += np.multiply(self.dIFOA[t,self.hidden_size:2*self.hidden_size], self.c0)  
                self.dWpeepIFO[2,:] += np.multiply(self.dIFOA[t,2*self.hidden_size:3*self.hidden_size], self.C[t,:])
                    
            if (t>0):
                self.dHout[t-1,:] += self.dHin[t,1+self.input_size:]
            else:
                self.dh0 += self.dHin[t,1+self.input_size:] 
                
    def get_hidden_output(self):      
        return self.Hout


    def train_network(self, learning_rate):
        for param, dparam, mem in zip([self.WLSTM, self.WpeepIFO],
                                  [self.dWLSTM, self.dWpeepIFO ],
                                  [self.mWLSTM, self.mWpeepIFO]):
            mem += dparam * dparam
            param += -learning_rate * dparam / np.sqrt(mem + 1e-8)
    
    def sample_network(self, X, W_out, next_data_points):
        self.reset_states()
        n = X.shape[0]
    
        p = n + next_data_points
          
        # LSTM forward pass for the duration of X, and then prediction for another n duration
        xphpbias = self.WLSTM.shape[0] # x (input) plus, hidden plus, bias
        self.Hin = np.zeros((p, xphpbias))
        self.Hout = np.zeros((p, self.hidden_size))
        
        self.IFOA = np.zeros((p, self.hidden_size * 4)) #before non-linearlity
        self.IFOA_f = np.zeros((p, self.hidden_size * 4)) # after the non-linearity
        self.C = np.zeros((p, self.hidden_size)) # Cell values/ cell contents
                  
        for t in range(p):
            prev_h = self.Hout[t-1,:] if (t > 0) else self.h0
            prev_c = self.C[t-1,:] if (t>0) else self.c0
            
            self.Hin[t,0] = 1 # this is for the bias
            
            self.Hin[t,1+self.input_size:] = prev_h
            if (t<n):
                self.Hin[t,1:1+self.input_size] = X[t, :]
            else:
                self.Hin[t,1:1+self.input_size] = (self.Hout[t-1,:].dot(matrix_trans(W_out)))[0]
            # Computing all gate activations 
            self.IFOA[t,:] = self.Hin[t,:].dot(self.WLSTM)
            
            # Adding peephole weights connections
            self.IFOA[t,:self.hidden_size] = self.IFOA[t,:self.hidden_size] + np.multiply(prev_c, self.WpeepIFO[0,:])       # input gate - adding peephole connections
            self.IFOA[t,self.hidden_size:2*self.hidden_size] = self.IFOA[t,self.hidden_size:2*self.hidden_size] + np.multiply(prev_c, self.WpeepIFO[1,:])       # forget gate - adding peephole connections
            
            # Passing through the non-linearities - sigmoid for gates input and forget - output is below due to peephole connections 
            self.IFOA_f[t,0:2*self.hidden_size] = 1.0 / (1.0 + np.exp(-self.IFOA[t,0:2*self.hidden_size]))
            self.IFOA_f[t,3*self.hidden_size:] = np.tanh(self.IFOA[t,3*self.hidden_size:]) # tanh non-linearity for the A gate (before the multiplicated input to the cell)
            
            # Computing the cell activation            
            self.C[t,:] = self.IFOA_f[t,self.hidden_size:2*self.hidden_size]*prev_c + self.IFOA_f[t,:self.hidden_size]*self.IFOA_f[t,3*self.hidden_size:]

            # Computing the output gate with peephole connections
            self.IFOA[t,2*self.hidden_size:3*self.hidden_size] = self.IFOA[t,2*self.hidden_size:3*self.hidden_size] + np.multiply(self.C[t,:], self.WpeepIFO[2,:]) # output gate - adding peephole connections            
            
            self.IFOA_f[t,2*self.hidden_size:3*self.hidden_size] = 1.0 / (1.0 + np.exp(-self.IFOA[t,2*self.hidden_size:3*self.hidden_size]))
            self.Hout[t,:] = self.IFOA_f[t,2*self.hidden_size:3*self.hidden_size]*np.tanh(self.C[t,:])
        
        return self.Hout
  
