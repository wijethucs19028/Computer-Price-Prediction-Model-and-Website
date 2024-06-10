import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

def prediction(lst):
    filename='ML_project/predictor.pickle'
    with open(filename,'rb') as file:
        model=pickle.load(file)
    pred_value=model.predict([lst])  
    return pred_value  

# Define the feature lists outside the route function for reusability
company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'Other', 'toshiba','samsung']
typename_list = ['2in1convertible', 'gaming', 'notebook', 'netbook', 'ultrabook', 'workstation']
opsys_list = ['windows', 'linux', 'mac', 'other','chrome']
cpu_list = ['IntelCorei3', 'IntelCorei5', 'IntelCorei7', 'amd','IntelCeleronDual','other']
gpu_list = ['intel', 'nvidia', 'amd',]

@app.route('/', methods=['POST', 'GET'])
def index():
    pred=0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpu']
        gpu = request.form['gpu']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')

        # Initialize the feature list
        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        # Define a function to traverse the lists and append the appropriate values to the feature list
        def traverse(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)

        # Traverse the lists with the respective input values
        traverse(company_list, company)
        traverse(typename_list, typename)
        traverse(opsys_list, opsys)
        traverse(cpu_list, cpu)
        traverse(gpu_list, gpu)

        pred=prediction(feature_list)*1.08
        pred=pred[0]
        

    return render_template("index.html", pred=pred)

if __name__ == '__main__':
    app.run(debug=True)
