import streamlit as st
import plotly_express as px

st.set_page_config(page_title="Truss Analysis",page_icon=":shark:")

Tab1,Tab2,Tab3,Tab4 = st.tabs(["[ Joints ]","[ Elements ]","[ Forces ]","[ Results ]"])

with st.sidebar:
    st.title("Truss Analysis")
    st.write("**This app analyzes truss structures using the stiffness method.**")
    st.write("Temperature changes are not considered.")
    st.write("Fabrication error of elements are not considered.")
    st.markdown("[aea](https://www.google.com)")

with Tab1:
    c1,c2,c3 = st.columns(3,gap="large")
    with c1:
        st.write("Number of joints:")
        nNudos = st.number_input("nNudos",1,100,1,1,label_visibility="collapsed")
    with c2:
        st.write("Length units:")
        length_unit = st.text_input("LU","m",label_visibility="collapsed")
    with c3:
        st.write("Force units:")
        force_unit = st.text_input("FU","kN",label_visibility="collapsed")
    plot1 = px.line(x=[0],y=[0],labels={"x":f"x ({length_unit})","y":f"y ({length_unit})"})
    st.write("---")
    dict_Nudos = {}
    GdL = 1
    labX = f"Coord X ({length_unit}):"
    labY = f"Coord Y ({length_unit}):"
    c4,c1,c2,c3,c5 = st.columns([1,1.5,2,2,1],gap="medium")
    with c1: st.write("**Joint**")
    with c2: st.write("**"+labX+"**")
    with c3: st.write("**"+labY+"**")
    for i in range(nNudos):
        label = "Joint #"+str(i+1).zfill(2)
        c4,c1,c2,c3,c5 = st.columns([1,1.5,2,2,1],gap="medium")
        with c1:
            st.write(" ")
            st.write("**"+label+"**")
        with c2:
            coord_x = st.number_input(labX,label_visibility="collapsed")
        with c3:
            coord_y = st.number_input(labY,label_visibility="collapsed")
        dict_Nudos[label]=[coord_x,coord_y,GdL,GdL+1]
        plot1.update_layout(title_text="Joints")
        plot1.add_scatter(x=[coord_x],y=[coord_y],mode="markers",marker={"color":"#FF0101","size":15},name=label)
        GdL +=2
        #st.write("---")
        labX += " "
        labY += " "
    st.write("---")
    
    #dict_Nudos
    ListaNudos = list(dict_Nudos.keys())
    #ListaNudos
    st.plotly_chart(plot1,use_container_width=True)

with Tab2:
    c1,c2 = st.columns([1,1])
    with c1: st.write("Number of elements:")
    with c2: nElements = st.number_input("nElements",1,100,1,1,label_visibility="collapsed")
    st.write("---")
    Elements = []
    lab_i = "From:"
    lab_f = "To:"
    lab_A = f"A ({length_unit}²):"
    lab_E = f"E ({force_unit}/{length_unit}²)"
    c1,c2,c3,c4,c5 = st.columns([1.5,2,2,2,2],gap="medium")
    with c1: st.write("**Elements**")
    with c2: st.write("**"+lab_i+"**")
    with c3: st.write("**"+lab_f+"**")
    with c4: st.write("**"+lab_A+"**")
    with c5: st.write("**"+lab_E+"**")
    for i in range(nElements):
        label = "Element #"+str(i+1).zfill(2)
        c1,c2,c3,c4,c5 = st.columns([1.5,2,2,2,2],gap="medium")
        with c1:
            st.write(" ")
            st.write("**"+label+"**")
        with c2:
            Joint_i = st.selectbox(lab_i,options=ListaNudos,label_visibility="collapsed")
        with c3:
            Joint_f = st.selectbox(lab_f,options=ListaNudos,label_visibility="collapsed")
        with c4:
            Area = st.number_input(lab_A,value=1.0,label_visibility="collapsed")
        with c5:
            Elast = st.number_input(lab_E,value=1.0,label_visibility="collapsed")
        Elements.append([label,Joint_i,Joint_f,Area,Elast])
        plot1.add_scatter(x=[dict_Nudos[Joint_i][0],dict_Nudos[Joint_f][0]],y=[dict_Nudos[Joint_i][1],dict_Nudos[Joint_f][1]],mode="lines",line={"color":"#01FE40","width":4},name=label)
        lab_i += " "
        lab_f += " "
        lab_A += " "
        lab_E += " "
    st.write("---")
    #Elements
    st.plotly_chart(plot1,use_container_width=True)
