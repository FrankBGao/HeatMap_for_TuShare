from flask import Flask,  request,  render_template
import tushare as ts
import get_data as gd
import heatmap_real_time as heatmap
app = Flask(__name__)


@app.route('/', methods=['GET'])
def plot_days():
    if request.method == 'GET' :
        today = ts.get_today_all()
        code_info = ts.get_industry_classified()

        today['code'] = today['code'].astype(unicode)
        one_day = gd.get_data_real_time(code_info, today)
        body = heatmap.get_heatmap('Today', one_day)
        return render_template('heatmap.html', body=body)

if __name__ == '__main__':
    app.debug = True
    app.run()

