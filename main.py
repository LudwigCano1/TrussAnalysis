from pydoc import visiblename
import streamlit as st
import plotly_express as px
from functions import Assemble_K_general,Fix,load
from numpy.linalg import solve,det

st.set_page_config(page_title="Truss Analysis",page_icon=":shark:")

Tab1,Tab2,Tab3,Tab4,Tab5 = st.tabs(["[ Joints ]","[ Elements ]","[ Constraints ]","[ Forces ]","[ Results ]"])

with st.sidebar:
    st.title("Truss Analysis")
    st.write("**This app analyzes truss structures using the stiffness method.**")
    st.write("Temperature changes are not considered.")
    st.write("Fabrication error of elements are not considered.")
    #st.markdown("[aea](https://www.google.com)")
    st.write("Colors:")
    c1,c2 = st.columns([3,1])
    with c1: st.write("Node color:")
    with c2: col_joint = st.color_picker("col_j",label_visibility="collapsed")
    c1,c2 = st.columns([3,1])
    with c1: st.write("Element color:")
    with c2: col_elem = st.color_picker("col_e",label_visibility="collapsed")
    c1,c2 = st.columns([3,1])
    with c1: st.write("Constraint color:")
    with c2: col_const = st.color_picker("col_c",label_visibility="collapsed")

with Tab1:
    c1,c2,c3 = st.columns(3,gap="large")
    with c1:
        st.write("Number of joints:")
        nNudos = st.number_input("nNudos",2,100,2,1,label_visibility="collapsed")
    with c2:
        st.write("Length units:")
        length_unit = st.text_input("LU","m",label_visibility="collapsed")
    with c3:
        st.write("Force units:")
        force_unit = st.text_input("FU","kN",label_visibility="collapsed")
    plot1 = px.line(x=[0],y=[0],labels={"x":f"x ({length_unit})","y":f"y ({length_unit})"})
    st.write("---")
    dict_Nudos = {}
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
        dict_Nudos[label]=[coord_x,coord_y]
        plot1.update_layout(showlegend=False)
        plot1.add_scatter(x=[coord_x],y=[coord_y],mode="markers+text",marker={"color":col_joint,"size":15},name=label,text=label,textposition="bottom center")
        #st.write("---")
        labX += " "
        labY += " "
    st.write("---")
    ListaNudos = list(dict_Nudos.keys())
    st.plotly_chart(plot1,use_container_width=True)

with Tab2:
    c1,c2 = st.columns([1,1])
    Nudos_Usados = {}
    with c1: st.write("Number of elements:")
    with c2: nElements = st.number_input("nElements",1,100,1,1,label_visibility="collapsed")
    st.write("---")
    Elements = []
    dict_Elem = {}
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
    GdL = 0
    plot1.data = []
    for i in range(nElements):
        label = "Element #"+str(i+1).zfill(2)
        c1,c2,c3,c4,c5 = st.columns([1.5,2,2,2,2],gap="medium")
        with c1:
            st.write(" ")
            st.write("**"+label+"**")
        with c2:
            Joint_i = st.selectbox(lab_i,options=ListaNudos,label_visibility="collapsed")
        with c3:
            copiaListaNudos = ListaNudos[:]
            copiaListaNudos.remove(Joint_i)
            Joint_f = st.selectbox(lab_f,options=copiaListaNudos,label_visibility="collapsed")
        with c4:
            Area = st.number_input(lab_A,value=1.0,label_visibility="collapsed")
        with c5:
            Elast = st.number_input(lab_E,value=1.0,label_visibility="collapsed")
        Elements.append([label,Joint_i,Joint_f,Area,Elast])
        dict_Elem[label] = [Joint_i,Joint_f,Area,Elast]
        Nudos_Usados[Joint_i] = dict_Nudos[Joint_i]
        Nudos_Usados[Joint_f] = dict_Nudos[Joint_f]
        plot1.add_scatter(x=[dict_Nudos[Joint_i][0],dict_Nudos[Joint_f][0]],y=[dict_Nudos[Joint_i][1],dict_Nudos[Joint_f][1]],mode="lines",line={"color":col_elem,"width":4},name=label)
        plot1.add_scatter(x=[0.5*(dict_Nudos[Joint_i][0]+dict_Nudos[Joint_f][0])],y=[0.5*(dict_Nudos[Joint_i][1]+dict_Nudos[Joint_f][1])],mode="lines+text",line={"color":col_elem,"width":4},name=label,text=label,textposition="bottom center")
        lab_i += " "
        lab_f += " "
        lab_A += " "
        lab_E += " "
    GdL = 0
    for i in Nudos_Usados:
        Nudos_Usados[i] = Nudos_Usados[i] + [GdL,GdL+1]
        GdL += 2
        plot1.add_scatter(x=[Nudos_Usados[i][0]],y=[Nudos_Usados[i][1]],mode="markers",marker={"color":col_joint,"size":15},name=i)
    st.write("---")
    st.plotly_chart(plot1,use_container_width=True)

with Tab3:
    st.write("Active the checkbox to restraint the displacement in that direction")
    c1,c2,c3,c4,c5 = st.columns([2,1,1,1,2])
    label = " "
    dict_constraints = {}
    with c2: st.write("**Joint**")
    with c3: st.write("**DX**")
    with c4: st.write("**DY**")
    for i in Nudos_Usados:
        with c2: st.write(i)
        with c3:
            DX = st.checkbox(label=label)
            label += " "
        with c4:
            DY = st.checkbox(label=label)
            label += " "
        if DX or DY:
            dict_constraints[i] = [int(DX),int(DY),Nudos_Usados[i][2],Nudos_Usados[i][3]]
            if DX and not DY:
                plot1.add_scatter(x=[Nudos_Usados[i][0]],y=[Nudos_Usados[i][1]],marker={"symbol":"8","size":25,"color":col_const})
            if DY and not DX:
                plot1.add_scatter(x=[Nudos_Usados[i][0]],y=[Nudos_Usados[i][1]],marker={"symbol":"5","size":25,"color":col_const})
            if DY and DX:
                plot1.add_scatter(x=[Nudos_Usados[i][0]],y=[Nudos_Usados[i][1]],marker={"symbol":"1","size":25,"color":col_const})
    st.plotly_chart(plot1,use_container_width=True)

with Tab4:
    c1,c2 = st.columns(2)
    with c1: st.write("**Number of forces:**")
    with c2: nForces = st.number_input("nForces",1,100,1,1,label_visibility="collapsed")
    labJForces = " "
    labDForces = " "
    labVForces = " "
    list_forces = []
    for i in range(nForces):
        c1,c2,c3,c4,c5 = st.columns([1,2,1,2,1])
        with c2: J = st.selectbox(label=labJForces,options=Nudos_Usados,label_visibility="collapsed")
        with c3: D = st.radio(label=labDForces,options=("DX","DY"),label_visibility="collapsed")
        with c4: V = st.number_input(label=labVForces,label_visibility="collapsed")
        labJForces += " "
        labDForces += " "
        labVForces += " "
        if D == "DX": list_forces.append([J,[1,0],V,Nudos_Usados[J][2]])
        else: list_forces.append([J,[0,1],V,Nudos_Usados[J][2]])

K,F = Assemble_K_general(Nudos_Usados,dict_Elem)
K,F = Fix(K,F,dict_constraints)
F = load(F,list_forces)
st.write("---")

with Tab5:
    pes1,pes2 = st.tabs(["[ General ]","[ Elements ]"])
    with pes1:
        c1,c2,c3 = st.columns([3,1,1])
        if det(K) != 0:
            U = solve(K,F)
            with c1:
                st.write("Global stiffness matrix")
                st.write(K)
            with c2:
                st.write("Displacements")
                st.write(U)
            with c3:
                st.write("Forces")
                st.write(F)
        else:
            st.write("The constraints are not enough for equilibrium")
    with pes2:
        st.write("a")
        #ver_elem = st.selectbox()
