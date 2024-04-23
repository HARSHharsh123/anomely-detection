from flask import Flask , render_template , request
import pickle
import sklearn
from sklearn.preprocessing import StandardScaler
application = Flask(__name__)

model = pickle.load(open('model/dtc.pkl' , 'rb'))
scaler = pickle.load(open('model/scaling.pkl' , 'rb'))

@application.route('/')
def welcome():
    return render_template('index.html')


@application.route('/Prediction' , methods = ['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        protocol_type = int(request.form.get('protocol_type'))
        service = int(request.form.get('service'))
        flag = int(request.form.get('flag'))
        src_bytes = int(request.form.get('src_bytes'))
        dst_bytes = int(request.form.get('dst_bytes'))
        count = int(request.form.get('count'))
        same_srv_rate = float(request.form.get('same_srv_rate'))
        diff_srv_rate = float(request.form.get('diff_srv_rate'))
        dst_host_srv_count = int(request.form.get('dst_host_srv_count'))
        dst_host_same_srv_rate = float(request.form.get('dst_host_same_srv_rate'))

        new_data_scaled = scaler.transform([[protocol_type ,service ,flag ,src_bytes ,dst_bytes, count , same_srv_rate , diff_srv_rate ,dst_host_srv_count , dst_host_same_srv_rate]])
        result = model.predict(new_data_scaled)

        return render_template('home.html' , result = result[0])
    else:
        return render_template('home.html')


if __name__ == '__main__':
    application.run(debug=True)
