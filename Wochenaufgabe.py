import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import requests
import os.path

st.title('Projektpräsentation')
st.subheader('Teamvorstellung')

st.write('Wir sind Gruppe 11 und bestehen aus Jorgo, Debora und Daniel. Wir alle studieren Wirtschaftsinformatik im 4. Semester.')

st.subheader('Projektvorstellung')
st.write('Wir haben uns als Projekt für Image Captioning entschieden.  \n' 
         'Das heißt, es soll ein Modell trainiert werden, welches in der Lage ist eine Bildunterschrift für Bilder einer spezifischen Domäne, also innerhalb eines spezifischen Bereiches, zu erzeugen.')

st.subheader('Datenset')
st.write('Als Datenset wird zum trainieren und testen das LAION5B Datenset verwenden, welches eine Sammlung von 6 Milliarden Bildern und 240 TB an Größe darstellt.  \n'
         'In der nachfolgenden Tabelle ist ein Ausschnitt aus einem Subset dargestellt, welchen man benutzen kann um die entsprechenden Bilder mithilfe der URL zu downloaden.  \n'
         'Hierzu einfach eine beliebige Zeile selektieren, das ausgewählte Bild wird anschließend angezeigt.')


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

if len(selection["selected_rows"]) > 0:
    st.write("Hier ist das ausgewählte Bild! ")
    url = selection["selected_rows"][0]["url"]
    id = selection["selected_rows"][0]["id"]
    filename = str(id) + '.jpg'
    bool = os.path.exists('pictures/' + filename)
    if not bool:
        r = requests.get(url, allow_redirects=True)
        open("pictures/" + str(id) + '.jpg', "wb").write(r.content)
    st.image('pictures/' + str(id) + '.jpg')
    st.write(selection["selected_rows"][0]["caption"])








