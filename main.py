import streamlit as st
import plotly_express as px
from functions import Assemble_K_element, Assemble_K_general,Fix,load
from numpy.linalg import solve,det
from numpy import array,zeros
from math import sqrt

st.set_page_config(page_title="Truss Analysis",page_icon=":shark:")

Tab1,Tab2,Tab3,Tab4,Tab5 = st.tabs(["[ Joints ]","[ Elements ]","[ Constraints ]","[ Forces ]","[ Results ]"])

with st.sidebar:
    st.title("Truss Analysis")
    st.write("**This app analyzes truss structures using the stiffness method.**")
    st.write("Temperature changes are not considered.")
    st.write("Fabrication error of elements are not considered.")
    #st.markdown("[aea](https://www.google.com)")
    with st.expander("Colors:"):
        c1,c2 = st.columns([3,1])
        with c1: st.write("Node color:")
        with c2: col_joint = st.color_picker("col_j","#FD0606",label_visibility="collapsed")
        c1,c2 = st.columns([3,1])
        with c1: st.write("Element color:")
        with c2: col_elem = st.color_picker("col_e","#07F7C0",label_visibility="collapsed")
        c1,c2 = st.columns([3,1])
        with c1: st.write("Constraint color:")
        with c2: col_const = st.color_picker("col_c","#1200FF",label_visibility="collapsed")
    st.write("**Developed by:** Ludwig Cano")

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
    plot1 = px.line(x=[0],y=[0],labels={"x":f"x ({length_unit})","y":f"y ({length_unit})"},height=600)
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

x_max = Nudos_Usados["Joint #01"][0]
x_min = Nudos_Usados["Joint #01"][0]
y_max = Nudos_Usados["Joint #01"][1]
y_min = Nudos_Usados["Joint #01"][1]

for nudo in Nudos_Usados:
    if Nudos_Usados[nudo][0] < x_min:
        x_min = Nudos_Usados[nudo][0]
    if Nudos_Usados[nudo][0] > x_max:
        x_max = Nudos_Usados[nudo][0]
    if Nudos_Usados[nudo][1] < y_min:
        y_min = Nudos_Usados[nudo][1]
    if Nudos_Usados[nudo][1] > y_max:
        y_max = Nudos_Usados[nudo][1]

dist_max = max(x_max-x_min,y_max-y_min)/10

with Tab3:
    st.write("Active the checkbox to restraint the displacement in that direction")
    c1,c2,c3,c4,c5 = st.columns([2,1,1,1,2])
    label = " "
    dict_constraints = {}
    with c2: st.write("**Joint**")
    with c3: st.write("**RX**")
    with c4: st.write("**RY**")
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
                plot1.add_scatter(x=[Nudos_Usados[i][0]],y=[Nudos_Usados[i][1]],marker={"symbol":"8","size":30,"color":col_const})
            if DY and not DX:
                plot1.add_scatter(x=[Nudos_Usados[i][0]],y=[Nudos_Usados[i][1]],marker={"symbol":"5","size":30,"color":col_const})
            if DY and DX:
                plot1.add_scatter(x=[Nudos_Usados[i][0]],y=[Nudos_Usados[i][1]],marker={"symbol":"1","size":20,"color":col_const})
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
    pes1,pes2,pes3 = st.tabs(["[ General ]","[ Elements ]","[ Deformed ]"])
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
        ver_elem = st.selectbox("Select Element:",dict_Elem)
        coord_start = array([Nudos_Usados[dict_Elem[ver_elem][0]][0],Nudos_Usados[dict_Elem[ver_elem][0]][1]])
        coord_end = array([Nudos_Usados[dict_Elem[ver_elem][1]][0],Nudos_Usados[dict_Elem[ver_elem][1]][1]])
        A = dict_Elem[ver_elem][2]
        E = dict_Elem[ver_elem][3]
        K_elem = Assemble_K_element(coord_start,coord_end,A,E)
        u_el = zeros((4,1))
        u_el[0] = U[Nudos_Usados[dict_Elem[ver_elem][0]][2]]
        u_el[1] = U[Nudos_Usados[dict_Elem[ver_elem][0]][3]]
        u_el[2] = U[Nudos_Usados[dict_Elem[ver_elem][1]][2]]
        u_el[3] = U[Nudos_Usados[dict_Elem[ver_elem][1]][3]]
        F_el = K_elem@u_el
        c1,c2,c3 = st.columns([3,2,1])
        if det(K) != 0:
            U = solve(K,F)
            with c1:
                st.write("Element stiffness matrix")
                st.write(K_elem)
            with c2:
                st.write("Displacements")
                st.write(u_el)
            with c3:
                st.write("Forces")
                st.write(F_el)
        else:
            st.write("The constraints are not enough for equilibrium")
        Joint_i = dict_Elem[ver_elem][0]
        Joint_f = dict_Elem[ver_elem][1]
        delta_x = -dict_Nudos[Joint_i][0]+dict_Nudos[Joint_f][0]
        delta_y = -dict_Nudos[Joint_i][1]+dict_Nudos[Joint_f][1]
        L = sqrt(delta_x**2+delta_y**2)
        delta_u = U[Nudos_Usados[Joint_f][2]][0] - U[Nudos_Usados[Joint_i][2]][0]
        delta_v = U[Nudos_Usados[Joint_f][3]][0] - U[Nudos_Usados[Joint_i][3]][0]
        N = dict_Elem[ver_elem][2]*dict_Elem[ver_elem][3]*(delta_x*delta_u+delta_y*delta_v)/(L**2)
        if N > 0: sss = "T"
        elif N < 0: sss = "C"
        else: sss = "0"
        st.write(f"Axial Force: {N:.2f} {force_unit} **{sss}**")

disp_max = max(abs(U))[0]

Nudos_Desplazados = {}
for n in Nudos_Usados:
    Nudos_Desplazados[n] = Nudos_Usados[n]
    Nudos_Desplazados[n][0] = Nudos_Usados[n][0] + U[Nudos_Usados[n][2]][0]*dist_max/disp_max
    Nudos_Desplazados[n][1] = Nudos_Usados[n][1] + U[Nudos_Usados[n][3]][0]*dist_max/disp_max

with pes3:
    plot_deformed = px.line(x=[0],y=[0],labels={"x":f"x ({length_unit})","y":f"y ({length_unit})"},range_x=[x_min-dist_max*1.5,x_max+dist_max*1.5],range_y=[y_min-dist_max*1.5,y_max+dist_max*1.5],height=600)
    plot_deformed.update_layout(showlegend=False)
    for el in dict_Elem:
        Joint_i = dict_Elem[el][0]
        Joint_f = dict_Elem[el][1]
        delta_x = -dict_Nudos[Joint_i][0]+dict_Nudos[Joint_f][0]
        delta_y = -dict_Nudos[Joint_i][1]+dict_Nudos[Joint_f][1]
        L = sqrt(delta_x**2+delta_y**2)
        delta_u = U[Nudos_Usados[Joint_f][2]][0] - U[Nudos_Usados[Joint_i][2]][0]
        delta_v = U[Nudos_Usados[Joint_f][3]][0] - U[Nudos_Usados[Joint_i][3]][0]
        N = dict_Elem[el][2]*dict_Elem[el][3]*(delta_x*delta_u+delta_y*delta_v)/(L**2)
        if N < 0: color = "#FF0000"
        elif N > 0: color = "#0000FF"
        else: color = "#FFFF00"
        plot_deformed.add_scatter(x=[dict_Nudos[Joint_i][0],dict_Nudos[Joint_f][0]],y=[dict_Nudos[Joint_i][1],dict_Nudos[Joint_f][1]],mode="lines",line={"color":"#000000","width":0.5,"dash":"dash"})
        plot_deformed.add_scatter(x=[Nudos_Desplazados[Joint_i][0],Nudos_Desplazados[Joint_f][0]],y=[Nudos_Desplazados[Joint_i][1],Nudos_Desplazados[Joint_f][1]],mode="lines",line={"color":color,"width":4})
        plot_deformed.add_scatter(x=[0.5*(Nudos_Desplazados[Joint_i][0]+Nudos_Desplazados[Joint_f][0])],y=[0.5*(Nudos_Desplazados[Joint_i][1]+Nudos_Desplazados[Joint_f][1])],mode="lines+text",line={"color":col_elem,"width":4},text=f"{N:.3f}",textposition="bottom center",textfont={"size":18,"color":color})
    st.plotly_chart(plot_deformed,use_container_width=True)
