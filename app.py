import streamlit as st
import pandas as pd
import seaborn as sns

from biolearn.data_library import DataLibrary
from biolearn.model_gallery import ModelGallery



st.title('Biolearn: Epigenetic Clock Models')

st.write("Welcome to this demo of data sources and clock models from the [biolearn python module](https://bio-learn.github.io/index.html).")

data_sources = pd.read_csv("biolearn_docs/biolearn_data.csv")
clocks = pd.read_csv("biolearn_docs/biolearn_clocks.csv")

## Show data
with st.container(border = True):
    st.write("The data are pulled from the Gene Expression Omnibus (GEO).")
    with st.expander("Click for more information about the available GEO datasets"):
        data_sources

option = st.selectbox(
    'Select a GEO methylation dataset to work with',
     data_sources['ID'])

## Data loading functions
@st.cache_data(persist=True)
def load_data(name, nrows=None):
    data_source = DataLibrary().get(name)
    data=data_source.load()
    methylation_data = data.dnam
    metadata = data.metadata
    return methylation_data, metadata



methylation_data, metadata = load_data(option)
n = len(methylation_data.columns)

st.write(f"{option} contains methylation data from {n} subjects.")
st.write(f"Metadata available for {option}: {metadata.columns.values}")


## Add epigenetic clock plots

@st.cache_data(persist=True)
def load_predictions():
    horvath_results = gallery.get("Horvathv1").predict(methylation_data)
    hannum_results = gallery.get("Hannum").predict(methylation_data)
    phenoage_results = gallery.get("PhenoAge").predict(methylation_data)
    actual_age = metadata['age']
    plot_data = pd.DataFrame({
    'Horvath 2013': horvath_results,
    'Hannum 2013': hannum_results,
    'PhenoAge 2018': phenoage_results,
    "Actual Age": actual_age})
    #TODO add more plots / make them checkboxes to select for
    return plot_data

gallery = ModelGallery()
with st.spinner("Please wait while clock models load..."):
    results_data = load_predictions()


plot_data = results_data
plot_data.index=plot_data['Actual Age']

relplot = sns.relplot(data=plot_data, kind="scatter", s=15)

relplot.set_axis_labels("Actual Age", "Predicted Age")

st.write(f"Here are a few epigenetic clocks on {option}")
st.pyplot(relplot)





