import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px


def run():

    st.sidebar.info('Welcome Samaneh Beigi')

    data = pd.read_json('./data/5.json', encoding='utf-8-sig')




    def date_range(start, end):
        delta = end - start  # as timedelta
        days = [start + timedelta(days=i) for i in range(delta.days + 1)]
        return days

    start_date = st.date_input('from date:')
    end_date = st.date_input('to date:')
    dates = date_range(start_date, end_date)


    text = st.selectbox('select option', ['number of relation',
                                          'number of product',
                                          'number of non-product',
                                          'number of attributes',
                                          'number of skiped',
                                          'number of comments'])

    num_relation = 0
    product_count = 0
    non_product_count = 0
    attribute_count = 0
    num_skip = 0
    num_comment = 0
    comment = []
    rel = []
    pro = []
    non_pro = []
    attribute = []
    skip = []
    date = []

    for d in dates:
        for i in range(len(data)):
            created_at = datetime.strptime(data['annotations'][i][0]['created_at'][2:-8], "%y-%m-%dT%H:%M:%S").date()
            for j in range(len(data['annotations'][i][0]['result'])):
                # number of relation
                if 'value' not in data['annotations'][i][0]['result'][j] and str(created_at) == str(d):
                    num_relation += 1
            
                if 'value' in data['annotations'][i][0]['result'][j] and str(created_at) == str(d):
                    # number of product
                    if data['annotations'][i][0]['result'][j]['value']['labels'][0] == 'محصول':
                        product_count += 1
                    # number of non-product
                    elif data['annotations'][i][0]['result'][j]['value']['labels'][0] == 'غیر محصول':
                        non_product_count += 1
                    # number of attribute
                    elif data['annotations'][i][0]['result'][j]['value']['labels'][0] == 'ویژگی':
                        attribute_count += 1
            
            # number of skip
            if len(data['annotations'][i][0]['result']) == 0 and str(created_at) == str(d):
                num_skip += 1
            
            # number of comment
            if str(created_at) == str(d):
                num_comment += 1

        date.append(d)
        comment.append(num_comment)
        rel.append(num_relation)
        pro.append(product_count)
        non_pro.append(non_product_count)
        attribute.append(attribute_count)
        skip.append(num_skip)
        
        num_comment = 0
        num_skip = 0
        non_product_count = 0
        attribute_count = 0
        product_count = 0
        num_relation = 0
    

    output = ''
    
    # if st.button('show'):
    if text == 'number of relation':
        output = str(sum(rel))
    elif text == 'number of product':
        output = str(sum(pro))
    elif text == 'number of non-product':
        output = str(sum(non_pro))
    elif text == 'number of attributes':
        output = str(sum(attribute))
    elif text == 'number of skiped':
        output = str(sum(skip))
    elif text == 'number of comments':
        output = str(sum(comment))

    st.success(output)

    
    data = pd.DataFrame()
    data['date'] = date
    data['num_comments'] = comment
    data['num_rel'] = rel
    data['num_product'] = pro
    data['num_non_pro'] = non_pro
    data['num_attr'] = attribute
    data['num_skip'] = skip

    fig = px.line(data, x='date',y=data.columns,
              hover_data={"date": "|%B %d, %Y"},
              title='custom tick labels')
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    run()
