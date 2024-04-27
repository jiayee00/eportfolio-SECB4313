from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

app = Flask(__name__,template_folder='template')

# Define the model
def model(y, t, rC, dC, rH, kIL, kCT, s, K):
    C, H, IL, T, S = y
    dCdt = rC * C * (1 - (T/K)) * (1 - S) - dC * C
    dHdt = rH * H
    dILdt = kIL * H
    dTdt = -kCT * C * T
    dSdt = s * T
    return [dCdt, dHdt, dILdt, dTdt, dSdt]

# Define the route for the homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    # Default values for the model parameters
    rC = 0.1
    dC = 0.05
    rH = 0.05
    kIL: float = 0.1
    kCT = 0.01
    s = 0.01
    K = 1000

    t = np.linspace(0, 100, 1000)
    y0 = [50, 10, 0, 1000, 0]
    sol = odeint(model, y0, t, args=(rC, dC, rH, kIL, kCT, s, K))

    # Plot the results
    fig, ax = plt.subplots()
    # plt.subplots()
    ax.plot(t, sol[:,0], 'b', label='CTL cells')
    ax.plot(t, sol[:,1], 'g', label='Th cells')
    ax.plot(t, sol[:,2], 'r', label='IL-2')
    ax.plot(t, sol[:,3], 'm', label='Tumour cells')
    ax.plot(t, sol[:,4], 'y', label='Immune suppression factor')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.legend()
    plt.savefig('env/static/images/plot.png')
    plt.close(fig)
    print("Hello11!!")
    
    # Render the homepage template with the current parameters and the graph
    return render_template('index.html', rC=rC, dC=dC, rH=rH, kIL=kIL, kCT=kCT, s=s, K=K)


# Define the route for the results page
@app.route('/results', methods=['GET', 'POST'])
def results():
    # Render the results template with the graph
    # If the form has been submitted, update the parameters
    if request.method == 'POST':
        
        rC = float(request.form.get('rC'))
        dC = float(request.form.get('dC'))
        rH = float(request.form.get('rH'))
        kIL = float(request.form.get('kIL'))
        kCT = float(request.form.get('kCT'))
        s = float(request.form.get('s'))
        K = float(request.form.get('K'))

    t = np.linspace(0, 100, 1000)
    y0 = [50, 10, 0, 1000, 0]
    sol = odeint(model, y0, t, args=(rC, dC, rH, kIL, kCT, s, K))

    # Plot the results
    fig, ax = plt.subplots()
    # plt.subplots()
    ax.plot(t, sol[:,0], 'b', label='CTL cells')
    ax.plot(t, sol[:,1], 'g', label='Th cells')
    ax.plot(t, sol[:,2], 'r', label='IL-2')
    ax.plot(t, sol[:,3], 'm', label='Tumour cells')
    ax.plot(t, sol[:,4], 'y', label='Immune suppression factor')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.legend()
    plt.savefig('env/static/images/plot.png')
    plt.close(fig)
    print("Hello22!!")
    
    return render_template('results.html',rC=rC, dC=dC, rH=rH, kIL=kIL, kCT=kCT, s=s, K=K)

if __name__ == '__main__':
    app.run(debug=True)
