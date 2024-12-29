import pandas as pd
import numpy as np 
import streamlit as st 
import pickle

df=pd.read_csv('./data/AllYearProcessed_data_1.csv')
columns_names=['Region','Standard Error','Economy (GDP per Capita)','Family','Health (Life Expectancy)','Freedom','Trust (Government Corruption)','Generosity','Dystopia Residual']
regions=list(df['Region'].value_counts().index)

with open('happinessModel.pkl', 'rb') as file:
    model = pickle.load(file)

st.header('Predicted the Happiness of Country')
with st.form(key="new form"):
                region=st.selectbox('Enter the Region',regions,key="region")
                std=st.number_input(f"Enter the {columns_names[1]}",key="std")
                ec=st.number_input(f"Enter the {columns_names[2]}",key="std1")
                fm=st.number_input(f"Enter the {columns_names[3]}",key="std2")
                ht=st.number_input(f"Enter the {columns_names[4]}",key="std4")
                fr=st.number_input(f"Enter the {columns_names[5]}",key="std5")
                tr=st.number_input(f"Enter the {columns_names[6]}",key="std6")
                gc=st.number_input(f"Enter the {columns_names[7]}",key="std7")
                ge=st.number_input(f"Enter the {columns_names[8]}",key="std8")
                submitted =st.form_submit_button("Predict")
            
                
                if submitted:
                    values=[region,float(std),float(ec),float(fm),float(ht),float(fr),float(tr),float(gc),float(ge)]
                    values=np.array(values)
                    values=values.reshape(1,-1)
                    pred_data=pd.DataFrame(values,columns=columns_names)
                    print(pred_data)
                    predict_val=model.predict(pred_data)[0]
                    print(predict_val)
                    st.write(f'Happiness Score is {np.round(predict_val,3)}')
                    # print(values)