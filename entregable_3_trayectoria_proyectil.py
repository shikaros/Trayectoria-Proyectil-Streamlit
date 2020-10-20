import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Modelación matemática para calcular la trayectoria sin la resistencia del aire (drag)
def coeficiente_del_drag(rho,C,A):
    return rho*C*A/2

def proyectil_sin_drag(v_0, theta_degree, y_0, t_start, t_end, g = 9.81):
    
    # Ángulo en radianes
    theta_rad = np.radians(theta_deg)
    
    #Componentes de velocidad inicial
    v_0x = v_0*np.cos(theta_rad)
    v_0y = v_0*np.sin(theta_rad)
    
    #Tiempo sobre el proyectil
    t = np.linspace(t_start,t_end,1000)

    # Posiciones de x y y en cada paso t
    r_x = v_0x*t
    r_y = -1/2*g*t**2+v_0y*t+y_0
    
    return r_x, r_y

#___________________________________________________________________________________
# Efecto de la erupción volcanica a los siguientes pasos de la aplicación del drag. Ecuaciones.
def proyectil_por_drag(v_x,v_y,v,a_x,a_y,x,y,dt, D, m,g=9.81):

    v_x_next = v_x + a_x*dt
    v_y_next = v_y + a_y*dt

    v_next = np.sqrt(v_x_next**2 + v_y_next**2)

    x_next = -1/2*a_x*dt**2+v_x*dt+x
    y_next = -1/2*a_y*dt**2+v_y*dt+y

    a_x_next = -D/m*v_next*v_x_next
    a_y_next = -g-D/m*v_next*v_y_next

    return a_x_next, a_y_next, v_x_next, v_y_next, v_next, x_next, y_next

#___________________________________________________________________________________
# Calculación de los efectos con resistencia del aire. Ecuaciones.
def proyectil_con_drag(v_0, theta_degree, y_0, m, rho, C, A, dt, N, g=9.81):

    theta_rad = np.radians(theta_degree)

    v_x = v_0*np.cos(theta_rad)
    v_y = v_0*np.sin(theta_rad)
    v = v_0

    x = 0
    y = y_0

    D = coeficiente_del_drag(rho,C,A)

    a_x = -D/m*v*v_x
    a_y = -g-D/m*v*v_y

    t = 0

    x_list = [x]
    y_list = [y]

    v_x_list = [v_x]
    v_y_list = [v_y]

    v_list = [v]

    a_x_list = [a_x]
    a_y_list = [a_y]

    t_list = [t]

    for i in range(N):
        a_x, a_y, v_x, v_y, v, x, y = proyectil_por_drag(v_x,v_y,v,a_x,a_y,x,y,dt,D,m)

        a_x_list.append(a_x)
        a_y_list.append(a_y)

        v_x_list.append(v_x)
        v_y_list.append(v_y)

        v_list.append(v)

        x_list.append(x)
        y_list.append(y)

        t_list.append(t)

    return a_x_list, a_y_list, v_x_list, v_y_list, v_list, x_list, y_list, t_list

#______________________________________________________________________________

def puntos_de_trayectoria(x_no_drag,y_no_drag,x_drag,y_drag,x_max,y_max,grid_size,title="Trayectoria del Proyectil"):
    #Definición de grafica

    fig, ax = plt.subplots(figsize=(16,9))

    ax.plot(x_no_drag, y_no_drag, label = "Sin resistencia del aire")
    ax.plot(x_drag, y_drag, label = "Con resistencia del aire")

    plt.grid()
    plt.title(title)


    plt.axis('scaled')

    plt.xlim([0,x_max])
    plt.ylim([0,y_max])

    plt.xticks(np.arange(0,x_max+1,100))
    plt.yticks(np.arange(0,y_max+1,50))

    plt.legend()

    return fig

#______________________________________________________________________________

def main(v_0, theta_degree, y_0, m, z):
    # tiempo inicial
    t_start = 0
    # tiempo final
    t_end = 50

    # Calcular Trayectoria sin resistencia
    r_x, r_y = proyectil_sin_drag(v_0, theta_degree, y_0, t_start, t_end)

    # Densidad del aire
    rho = 0.785
    # Coeficiente de arrastre
    C = 0.5
    # Área de la pelota 
    r = z/2
    A = np.pi*r**2
    # Delta t
    dt = 0.01
    # Iteraciones
    N = 10000

    [a_x_list, a_y_list, v_x_list, v_y_list, v_list, x_list, y_list, t_list] = proyectil_con_drag(v_0, theta_degree, y_0, m, rho, C, A, dt, N)

    fig = puntos_de_trayectoria(r_x,r_y,x_list, y_list,2800,1000,500)
    return fig

#Aplicación de las utilidades de streamlit
st.title('Trayectoria de Proyectil de una Erupción Volcánica')
st.write('Yeh Chul Shin A01781289')
st.subheader("Simulación de un proyectil con y sin resistencia del aire")


# Sliders para velocidad inicial, ángulo en grados, altura inicial, masa y radio de la roca.
v_0 = st.slider("Velocidad Inicial:",0,160,100)
theta_deg = st.slider("Ángulo en grados:",40,50,45)
y_0 = st.slider("Altura Inicial:",0,100,5)
st.write('Modificar la masa y el nominador de la radio para dar un efecto en la visualización de la trayectoria del proyectil con resistencia del aire')
m = st.slider("Masa:",0.1,20.0,10.0)
z = st.slider("Radio",0.01,1.00,0.100)

fig = main(v_0, theta_deg, y_0, m, z)
st.pyplot(fig)