import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Online Retail | U4", layout="wide")
st.title("Exploración de ventas | Online Retail")
st.caption("Demostración académica con datos históricos de UCI (2010–2011). Ingreso bruto = cantidad × precio; no equivale a utilidad.")
f=st.file_uploader("Carga Online Retail.xlsx o un CSV exportado", type=["xlsx","xls","csv"])
if f is None:
 st.info("Descarga el archivo original desde UCI (enlace en el informe) y cárgalo aquí."); st.stop()
df=pd.read_csv(f) if f.name.lower().endswith('.csv') else pd.read_excel(f)
df['InvoiceDate']=pd.to_datetime(df['InvoiceDate'], errors='coerce'); df['IsCancellation']=df['InvoiceNo'].astype(str).str.startswith('C'); df['Revenue']=df['Quantity']*df['UnitPrice']
s=df[(df.Quantity>0)&(df.UnitPrice>0)&(~df.IsCancellation)&df.InvoiceDate.notna()].copy()
s['Month']=s.InvoiceDate.dt.to_period('M').astype(str)
countries=sorted(s.Country.dropna().unique())
selected=st.sidebar.multiselect('País',countries,default=countries[:min(6,len(countries))])
months=sorted(s.Month.unique()); chosen=st.sidebar.select_slider('Periodo mensual',options=months,value=(months[0],months[-1])) if len(months)>1 else (months[0],months[-1])
s=s[s.Country.isin(selected)&s.Month.between(chosen[0],chosen[1])]
a,b,c=st.columns(3); a.metric('Ingreso bruto',f"£{s.Revenue.sum():,.0f}"); b.metric('Facturas',f"{s.InvoiceNo.nunique():,}"); c.metric('Países',f"{s.Country.nunique():,}")
monthly=s.groupby('Month',as_index=False).Revenue.sum()
fig=px.line(monthly,x='Month',y='Revenue',markers=True,title='Ingreso bruto por mes'); st.plotly_chart(fig,use_container_width=True)
ct=s.groupby('Country',as_index=False).Revenue.sum().sort_values('Revenue',ascending=False).head(12)
fig2=px.bar(ct.sort_values('Revenue'),x='Revenue',y='Country',orientation='h',title='Países con mayor ingreso bruto'); st.plotly_chart(fig2,use_container_width=True)
st.subheader('Lectura para decisión'); st.write('Identifica los mercados que concentran ingresos y revisa si el patrón se mantiene al cambiar periodo y país. Usa la concentración como señal para priorizar revisión de inventario y seguimiento comercial, validando con datos actuales y margen antes de asignar presupuesto.')
