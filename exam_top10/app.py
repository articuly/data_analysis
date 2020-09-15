from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/rating_top10')
def show_rating_top10():
    """将处理后的表格展示网页"""
    df = pd.read_csv('data_set/rating_top10.csv')
    data_html = df.to_html()
    return f"""
        <html>
            <body>
                <h3 align="center">Top 10 Rating Book Recommendation</h3>
                <div align="center">{data_html}</div>
                <p></p>
                <div align="center"><a href="/">Go back</a></div>
            </body>
        </html>
    """


@app.route('/reading_top10')
def show_reading_top10():
    """将处理后的表格展示网页"""
    df = pd.read_csv('data_set/count_top10.csv')
    data_html = df.to_html()
    return f"""
        <html>
            <body>
                <h3 align="center">Top 10 Reading Book Recommendation</h3>
                <div align="center">{data_html}</div>
                <p></p>
                <div align="center"><a href="/">Go back</a></div>
            </body>
        </html>
    """


@app.route('/rating_sum_top10')
def show_rating_sum_top10():
    """将处理后的表格展示网页"""
    df = pd.read_csv('data_set/rating_sum_top10.csv')
    data_html = df.to_html()
    return f"""
        <html>
            <body>
                <h3 align="center">Top 10 Overview Book Recommendation</h3>
                <div align="center">{data_html}</div>
                <p></p>
                <div align="center"><a href="/">Go back</a></div>
            </body>
        </html>
    """


if __name__ == '__main__':
    app.run()
