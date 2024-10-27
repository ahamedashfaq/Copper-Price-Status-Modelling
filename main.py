import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd
from pickle import dump
import joblib
import os
#------
from streamlit_navigation_bar import st_navbar

#st.set_page_config(initial_sidebar_state="collapsed", page_title="Industrial Copper Price Modelling", layout = "wide")

pages = ["Home", "Predict Price", "Predict order status"]

styles = {
    "nav": {
        "background-color": "rgb(203, 109, 81)",
    },
    "div": {
        "max-width": "40rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(49, 51, 63)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

page = st_navbar(pages, options={"use_padding": False}, styles=styles)



#----------------------------------------------HOME PAGE-----------------------------------------------------------------

if page == "Home":
    st.header("Copper price predictor app")
    
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("copper.png",width = 500)
        #st.write("test")
        #st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Friverworksmarketing.com%2Fwork%2Fcopper-co-logo-design-2%2F&psig=AOvVaw0YlgUnA-4IEaxsUQtJKRDR&ust=1729749247135000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCICL6p_oo4kDFQAAAAAdAAAAABAE",width = 500)
        #st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTK72RBoNYIExapV2XAQoVVBZQJz2oJsk9SHg&s",width = 500)
    #st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTK72RBoNYIExapV2XAQoVVBZQJz2oJsk9SHg&s",width = 500)
    
#----------------------------------------------Top10s PAGE-----------------------------------------------------------------


if page == "Predict Price":
    st.markdown("## :red[Please enter the values below to predict price]")
    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\le_col_val_rg.pkl', 'rb') as f:
        loaded_le_col_val_rg = pickle.load(f)

    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\oe_col_val_rg.pkl', 'rb') as f:
        loaded_oe_col_val_rg = pickle.load(f)

    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\rf_rg.pkl', 'rb') as f:
        loaded_rf_rg = pickle.load(f)

    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\scaler_rg.pkl', 'rb') as f:
        loaded_scaler_rg = pickle.load(f)

    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\le_rg.pkl', 'rb') as f:
        loaded_le_rg = pickle.load(f)

    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\oe_rg.pkl', 'rb') as f:
        loaded_oe_rg = pickle.load(f)
    #loaded_le_col_val = joblib.load('le_col_val.pkl')
    #loaded_oe_col_val = joblib.load('oe_col_val.pkl')
    #path1 = os.access("le_col_val.pkl", os.F_OK)
    #file = open('le_col_val.pkl', 'rb')
    #loaded_le_col_val = pickle.load(file)
    #file.close()

    col_df_rg = ['quantity_tons',	'customer',	'country','status', 'item_type','application','thickness','width','material_ref','product_ref','material_ref_bias']
    le_col_rg = ['product_ref' , 'country', 'application', 'customer', 'item_type', 'material_ref', 'status']
    oe_col_rg = ['width', 'thickness']

    left_co, cent_co,last_co = st.columns(3)
    with left_co:
        inp_quantity_tons = st.number_input("Enter required Quantity (in tons)")


        inp_Country = st.selectbox(
            'Select Country',
            (loaded_le_col_val_rg['country'].keys()))

        inp_Customer = st.selectbox(
            'Select Customer',
            (loaded_le_col_val_rg['customer'].keys()))

    with cent_co:
        inp_item_type = st.selectbox(
            'Select Item Type',
            (loaded_le_col_val_rg['item_type'].keys()))

        inp_application = st.selectbox(
            'Select Application',
            (loaded_le_col_val_rg['application'].keys()))

        inp_width = st.selectbox(
            'Select Width',
            (loaded_oe_col_val_rg['width'].keys()))

        

    with last_co:
        inp_thickness = st.selectbox(
            'SelectThickness',
            (loaded_oe_col_val_rg['thickness'].keys()))
        
        inp_product_ref = st.selectbox(
            'Select Product Reference',
            (loaded_le_col_val_rg['product_ref'].keys()))

        inp_material_ref = st.selectbox(
            'Select Material Reference',
            (loaded_le_col_val_rg['material_ref'].keys()))


    ######### Form input dataframe

    col_df_rg = ['quantity_tons',	'customer',	'country','status', 'item_type','application','thickness','width','material_ref','product_ref','material_ref_bias']
    if st.button("Predict"):
        input = [inp_quantity_tons, inp_Customer, inp_Country, 'Won',\
                    inp_item_type, inp_application, inp_thickness,\
                        inp_width, inp_material_ref, inp_product_ref,\
                             1 ]
        input_data = pd.DataFrame(columns = col_df_rg)
        input_data.loc[0] = input



        for col in le_col_rg:
            input_data[col] = loaded_le_rg[col].transform([input_data[col]])

        for col in oe_col_rg:
            input_data[col] = loaded_oe_rg[col].transform([input_data[col]])

        input_data[input_data.columns] = loaded_scaler_rg.transform(input_data[input_data.columns])


        predicted_val = loaded_rf_rg.predict(input_data)


        st.header(f'The predicted price is {predicted_val[0]} ')


#==================order page----------------------------------------------




if page == "Predict order status":
    st.markdown("## :red[Please enter the values below to predict order status]") 


    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\le_col_val_cl.pkl', 'rb') as f:
        loaded_le_col_val = pickle.load(f)

    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\oe_col_val_cl.pkl', 'rb') as f:
        loaded_oe_col_val = pickle.load(f)

    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\bbc_cl.pkl', 'rb') as f:
        loaded_bbc = pickle.load(f)

    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\scaler_cl.pkl', 'rb') as f:
        loaded_scaler = pickle.load(f)

    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\le_cl.pkl', 'rb') as f:
        loaded_le = pickle.load(f)

    with open(r'C:\Users\ashfaq.ahamed\Documents\projects1\ICM\oe_cl.pkl', 'rb') as f:
        loaded_oe = pickle.load(f)
    #loaded_le_col_val = joblib.load('le_col_val.pkl')
    #loaded_oe_col_val = joblib.load('oe_col_val.pkl')
    #path1 = os.access("le_col_val.pkl", os.F_OK)
    #file = open('le_col_val.pkl', 'rb')
    #loaded_le_col_val = pickle.load(file)
    #file.close()


    col_df = ['quantity_tons',	'customer',	'country','item_type','application','thickness','width','material_ref','product_ref','selling_price','material_ref_bias','delivery_days']
    le_col = ['product_ref' , 'country', 'application', 'customer', 'item_type', 'material_ref']
    oe_col = ['width', 'thickness']

    left_co, cent_co,last_co = st.columns(3)
    with left_co:
        inp_quantity_tons = st.number_input("Enter required Quantity (in tons)")


        inp_Country = st.selectbox(
            'Select Country',
            (loaded_le_col_val['country'].keys()))

        inp_Customer = st.selectbox(
            'Select Customer',
            (loaded_le_col_val['customer'].keys()))
        
        inp_item_type = st.selectbox(
            'Select Item Type',
            (loaded_le_col_val['item_type'].keys()))


    with cent_co:
        

        inp_application = st.selectbox(
            'Select Application',
            (loaded_le_col_val['application'].keys()))

        inp_width = st.selectbox(
            'Select Width',
            (loaded_oe_col_val['width'].keys()))
        
        inp_thickness = st.selectbox(
            'SelectThickness',
            (loaded_oe_col_val['thickness'].keys()))

        inp_product_ref = st.selectbox(
            'Select Product Reference',
            (loaded_le_col_val['product_ref'].keys()))
        
    with last_co:


        inp_material_ref = st.selectbox(
            'Select Material Reference',
            (loaded_le_col_val['material_ref'].keys()))

        inp_selling_price = st.number_input("Enter Estimated Selling price")

        inp_delivery_days = st.number_input("Enter Estimated days to deliver")

    ######### Form input dataframe

    if st.button("Predict"):
        input = [inp_quantity_tons, inp_Customer, inp_Country, \
                    inp_item_type, inp_application, inp_thickness,\
                        inp_width, inp_material_ref, inp_product_ref,\
                            inp_selling_price, 1,inp_delivery_days ]
        input_data = pd.DataFrame(columns = col_df)
        input_data.loc[0] = input



        for col in le_col:
            input_data[col] = loaded_le[col].transform([input_data[col]])

        for col in oe_col:
            input_data[col] = loaded_oe[col].transform([input_data[col]])

        input_data[input_data.columns] = loaded_scaler.transform(input_data[input_data.columns])


        predicted_val = loaded_bbc.predict(input_data)


        if predicted_val[0] == 1:
            st.header("The order status is likely to be Won ", divider="green")
        else:
            st.header("Sorry!, The order status is likely to be lost", divider="red")


    #print(f' For the given input data, the predicted PO status would be {predicted_val[0]}')

#streamlit run c:/Users/ashfaq.ahamed/Documents/projects1/ICM/main.py