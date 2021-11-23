import matplotlib.pyplot as pltfrom matplotlib import cmfrom matplotlib.ticker import LinearLocatorimport numpy as npimport matplotlib.pyplot as pltimport pandas as pdfrom datetime import datetimedef date_to_unix(date):    unx = int(datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime("%s"))    return unxdef today_unix():    unx = date_to_unix(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))    return unxdef format_vol(x):    return float(x.replace(',','')[:-1])/100def render_to_string_polynomial(betas):    res =f"Y = {betas[0]}"    if len(betas)>1:        for i in range(1,len(betas)):            res+=f" + {betas[i]}*X^{i}"    return resclass CubicSpline:    def __init__(self,X,Y,smoothing=0, extrapolation=False):        self.X = X        self.Y_original = Y        self.smoothing = smoothing        self.Y = Y        self.fit_status = False        self.coefs = []        self.extrapolate = extrapolation        self.min_eval = min(X)        self.max_eval = max(X)        self.M=[]        self.C=[]        self.Cp=[]        self.H=[]        if self.smoothing >0:            self.smooth()    def to_string(self):        pass    def smooth(self):        n=len(self.X)        Xi=self.X[0:n-1]        Xi_1 = self.X[1:n]        Xdiff = []        zip_object = zip(Xi, Xi_1)        for Xi, Xi_1 in zip_object:            Xdiff.append(Xi_1 - Xi)        #matrix of X increments        H=np.array(Xdiff).reshape((n-1,1))        #tridiag matrix        Q=np.zeros((n,n-2))        for i in range(1,n-1):            Q[i,i-1]=1/H[i-1]+1/H[i]        for i in range(0,n-2):            Q[i,i]=-1/H[i]        for i in range(2,n):            Q[i,i-2]=-1/H[i-1]        R = np.zeros((n-2, n - 2))        for i in range(0,n-2):            R[i,i]=(H[i]+H[i+1])/3        for i in range(0,n-3):            R[i,i+1]=-H[i]/6        for i in range(1,n-2):            R[i,i-1]=-H[i-1]/6        K=np.matmul(np.matmul(Q,np.linalg.inv(R)),np.transpose(Q))        s=np.matmul(np.linalg.inv(np.identity(n)+self.smoothing*K),self.Y_original)        self.Y=s    def change_smoothness(self,new_smooth):        self.smoothing = new_smooth        self.smooth()        self.fit_spline()    def fit_spline(self):        n = len(self.X)        Xi = self.X[0:n - 1]        Xi_1 = self.X[1:n]        Xdiff = []        zip_object = zip(Xi, Xi_1)        for Xi, Xi_1 in zip_object:            Xdiff.append(Xi_1 - Xi)        H = np.array(Xdiff).reshape((n - 1, 1))        #Matrix of second order derivatives        F=np.zeros(n)        for i in range(1,n-1):#F[0] and F[n-1] are left to 0 for natural spline            F[i]=(self.Y[i+1]-self.Y[i])/H[i]-(self.Y[i]-self.Y[i-1])/H[i-1]        F.reshape((n,1))#col vector        R = np.zeros((n, n))        R[0,0]=1        R[n-1,n-1]=1        for i in range(1, n - 1):            R[i, i] = (H[i-1] + H[i]) / 3        for i in range(1, n - 1):            R[i, i + 1] = H[i] / 6        for i in range(1, n - 1):            R[i, i - 1] = H[i - 1] / 6        M=np.matmul(np.linalg.inv(R),F)        C=[]        Cp=[]        for i in range(0,n-1):            C.append((self.Y[i+1]-self.Y[i])/H[i]-(M[i+1]-M[i])*H[i]/6)            Cp.append(self.Y[i]-M[i]*H[i]*H[i]/6)        self.M=M        self.C=C        self.Cp=Cp        self.H=H    def find_k(self,x):        k=0        while x>self.X[k]:            k+=1        return k-1    def eval_point(self,x):        y=0        if self.X[0]<= x < self.X[len(self.X)-1]:            k=self.find_k(x)            y=self.M[k]*((self.X[k+1]-x)**3)/(6*self.H[k])\              +self.M[k+1]*((x-self.X[k])**3)/(6*self.H[k])\              +self.C[k]*(x-self.X[k])\              +self.Cp[k]        return y[0]    def eval(self,X):        res=[]        for val in X:            res.append(self.eval_point(val))        return resclass PolynomialRegression:    def __init__(self,X,Y,order=-1, extrapolation=False):        if order<1 or order>=len(X):            if len(X)>3:                self.order=3            else:                self.order=len(X)-1        else:            self.order=order        self.X=X        self.Y=Y        self.fit_status=False        self.beta=[]        self.extrapolate=extrapolation        self.min_eval=min(X)        self.max_eval=max(X)    def to_string(self):        print("============================")        print(f"Regression of order {self.order}:")        print()        print(f"X len={len(self.X)}:")        print(self.X)        print()        print(f"Y len={len(self.Y)}:")        print(self.Y)        print()        print(f"Coefficients:")        print(render_to_string_polynomial(self.beta))        print(f"Extrapolate: {self.extrapolate}")        print(f"min eval: {self.min_eval}")        print(f"max eval: {self.max_eval}")    def fit_beta_coeff(self):        X_to_order =[np.ones(len(self.X)),self.X]        for i in range(2,self.order+1):            X_to_order.append(np.power(self.X,i))        X_to_order= np.transpose(X_to_order)        XtX_1 = np.linalg.inv(np.matmul(np.transpose(X_to_order),X_to_order))        self.beta= np.matmul(np.matmul(XtX_1,np.transpose(X_to_order)),self.Y)        self.fit_status=True    def fit(self):        self.fit_beta_coeff()    def change_order(self,order):        self.order=order        self.fit_status = False        self.fit_beta_coeff()        self.fit_status = True    #Evaluate a point    def evaluate_point(self, x):        if not self.extrapolate:            if not self.min_eval < x < self.max_eval:                return 0        X = [1,x]        for i in range(2,self.order+1):            X.append(np.power(x,i))        return np.dot(X,self.beta)    #Evaluate a vector of points    def evaluate_vector(self,X):        res=[]        for i in range(len(X)):            res.append(self.evaluate_point(X[i]))        return resclass Surface:    def __init__(self):        #calls        self.C_K=[]#vect of vect of strikes        self.C_min_K=0#window for viz        self.C_max_K = 0        self.C_imp_vol=[]#vect of vect of vols        self.C_bid = []  # vect of vect of bids        self.C_ask = []  # vect of vect of asks        self.C_T=[]#vect of T, my key        self.C_regressions=[]        #puts        self.P_K = []  # vect of vect of strikes        self.P_min_K=0#window for viz        self.P_max_K = 0        self.P_imp_vol = []  # vect of vect of vols        self.P_bid = []  # vect of vect of bids        self.P_ask = []  # vect of vect of asks        self.P_T = []  # vect of T, my key        self.P_regressions = []    def load_last_data(self):        c_data = pd.read_csv('/Users/glenhigh/Scrapping/OPERA_options_pricing/Market_data/Calls_AAPL_Last.csv')        p_data = pd.read_csv('/Users/glenhigh/Scrapping/OPERA_options_pricing/Market_data/Puts_AAPL_Last.csv')        today = today_unix()        self.C_max_K=max(c_data["Strike"])        self.C_min_K = min(c_data["Strike"])        self.P_max_K = max(p_data["Strike"])        self.P_min_K = min(p_data["Strike"])        #calls        for date in set(c_data['Date']):            filter=c_data['Date']==date            temp_c_k = c_data.loc[filter]["Strike"].values.tolist()            temp_c_imp_vol = list(map(format_vol, c_data.loc[filter]["Implied Volatility"]))            self.C_K.append(temp_c_k)            self.C_imp_vol.append(temp_c_imp_vol)            self.C_regressions.append(PolynomialRegression(temp_c_k,temp_c_imp_vol))            self.C_T.append((date_to_unix(date)-today)/(60*60*24*365))        # puts        for date in set(p_data['Date']):            filter = p_data['Date'] == date            temp_p_k = p_data.loc[filter]["Strike"].values.tolist()            temp_p_imp_vol = list(map(format_vol, p_data.loc[filter]["Implied Volatility"]))            self.P_K.append(temp_p_k)            self.P_imp_vol.append(temp_p_imp_vol)            self.P_regressions.append(PolynomialRegression(temp_p_k, temp_p_imp_vol))            self.P_T.append((date_to_unix(date) - today)/(60*60*24*365))    def build_viz(self,granularity_K=1):        c_axis_k=np.arange(self.C_min_K, self.C_max_K, granularity_K)        c_axis_t=self.C_T        print(c_axis_t)        c_vol_surface=[]        for i in range(len(c_axis_t)):            self.C_regressions[i].fit()            #self.C_regressions[i].to_string()            vol_t = self.C_regressions[i].evaluate_vector(c_axis_k)            c_vol_surface.append(vol_t)            print(c_vol_surface[i])        #print(c_vol_surface)        c_axis_k, c_axis_t = np.meshgrid(c_axis_k, c_axis_t)        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})        #print(c_vol_surface)        surf = ax.plot_surface(c_axis_t, c_axis_k, np.array(c_vol_surface), cmap=cm.coolwarm,linewidth=0, antialiased=False)        # Customize the z axis.        #ax.set_zlim(-1.01, 1.01)        ax.zaxis.set_major_locator(LinearLocator(10))        # A StrMethodFormatter is used automatically        ax.zaxis.set_major_formatter('{x:.02f}')        ax.set_ylabel('$Strike_K$', fontsize=20, rotation=150)        ax.set_xlabel('$Maturity_T$')        ax.set_zlabel(r'$\sigma$', fontsize=30, rotation=60)        # Add a color bar which maps values to colors.        fig.colorbar(surf, shrink=0.5, aspect=5)        plt.show()    def evaluate_point(self,k,t):        kc = 0        while t > self.C_T[kc]:            kc += 1        kc=kc - 1        kp = 0        while t > self.P_T[kp]:            kp += 1        kp = kp - 1        proportion_c=(t-self.C_T[kc])/(self.C_T[kc+1]-self.C_T[kc])        proportion_p = (t - self.P_T[kp]) / (self.P_T[kp + 1] - self.P_T[kp])        #make linear proportionnality        ret_c=self.C_regressions[kc].evaluate_point(k)*(1-proportion_c)+self.C_regressions[kc+1].evaluate_point(k)*(proportion_c)        ret_p=self.P_regressions[kp].evaluate_point(k) * (1 - proportion_p) + self.P_regressions[kp + 1].evaluate_point(k) * (proportion_p)        return (ret_c,ret_p)    def evaluate(self,K,T):        res=[]        for k,t in zip(K,T):            res.append(self.evaluate_point(k,t))        return res####################### vvv TESTS vvv ######################def try_spline():    sp=CubicSpline([1,2,3,4,5],[10,11,23,10,11],2)    sp.fit_spline()    print(sp.eval([1.0000000001,2,3,4,4.999999999]))def try_on_data_viz():    surf=Surface()    surf.load_last_data()    #surf.build_viz()    print(surf.evaluate_point(1,1))def try_regression():    X = [-1,0,1,2,3,4]    Y=np.power(X,2)    mod=PolynomialRegression(X,Y,2)    mod.fit()    print(mod.evaluate_vector([-3,1,0,1,3]))def try_fake_k_t_viz():    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})    # Make data.    T = [0,1,2]    K = [80,90,100]    K, T = np.meshgrid(K, T)    Z=np.array([[1,0,0.5],[2,1,1.5],[7,5,6]])    # Plot the surface.    surf = ax.plot_surface(K, T, Z, cmap=cm.coolwarm,                           linewidth=0, antialiased=False)    # Customize the z axis.    ax.set_zlim(-1.01, 1.01)    ax.zaxis.set_major_locator(LinearLocator(10))    # A StrMethodFormatter is used automatically    ax.zaxis.set_major_formatter('{x:.02f}')    ax.set_xlabel('$Strike K$', fontsize=20, rotation=150)    ax.set_ylabel('$Maturity T$')    ax.set_zlabel(r'$\sigma$', fontsize=30, rotation=60)    # Add a color bar which maps values to colors.    fig.colorbar(surf, shrink=0.5, aspect=5)    plt.show()##### TRIES #######try_spline()try_on_data_viz()#try_fake_k_t_viz()