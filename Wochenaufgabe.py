import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import requests
from pathlib import *
import os.path
import numpy as np
from pyarrow.parquet import ParquetFile
import pyarrow as pa 


st.title('Projektpräsentation')
st.subheader('Teamvorstellung')

st.write('Wir sind Jorgo, Deborah und Daniel und wir alle studieren Wirtschaftsinformatik im 4. Semester.')

st.subheader('Projektvorstellung')
st.write('Wir haben uns als Projekt für Image Captioning entschieden.')
st.write('Das heißt, wir sollen ein Modell trainieren, welches in der Lage ist eine Bildunterschrift für Bilder einer spezifischen Domäne, also innerhalb eines spezifischen Bereiches, zu erzeugen.')

st.subheader('Datenset')
st.write('Als Datenset sollen wir zum trainieren und testen das LAION5B Datenset verwenden, welches eine Sammlung von 6 Milliarden Bildern und 240 TB an Größe darstellt.')
st.write('In der nachfolgenden Tabelle ist ein Ausschnitt aus einer Metadatendatei dargestellt, welchen man benutzen kann um die entsprechenden Bilder mithilfe der URL zu downloaden.')

#pf = ParquetFile('FirstData.parquet') 
#rowNumber = next(pf.iter_batches(batch_size = 1000)) 
#df = pa.Table.from_batches([rowNumber]).to_pandas() 
#st.write(df)

df = pd.read_json('DogSubset.json')

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


selection = aggrid_interactive_table(df)

if selection:
    st.write("You selected:")
    #st.json(selection["selected_rows"])
    
url = selection["selected_rows"][0]["url"]
id = selection["selected_rows"][0]["id"]
filename = str(id) + '.jpg'
bool = os.path.exists('pictures/' + filename)
if not bool:
    r = requests.get(url, allow_redirects=True)
    open("pictures/" + str(id) + '.jpg', "wb").write(r.content)

st.image('pictures/' + str(id) + '.jpg')
st.write(selection["selected_rows"][0]["caption"])








