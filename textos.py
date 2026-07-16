import streamlit as st

@st.dialog("Teoría del sistema", width="large")
def teoria():
    
    st.header("Fundamentos del cálculo (EPA)")
    st.markdown("""
    ### 1. La Ecuación teórica del $\Delta H_@$
    Según el documento técnico de la EPA (ver Fuentes), la siguiente ecuación (Ecuación 1) define el diferencial de presión del orificio bajo condiciones de referencia de 
    0.75 $dcfm$ (*dry cubic feet per minute*) de caudal, 68 $F$ de temperatura y 29,92 $in.Hg$ de presión:
    """)
    st.latex(r"""
    \Delta H_@ = \frac{0.0319 \  \Delta H}{P_{bar}(t_0 + 460)} \left[ \frac{(t_w+460) \ \theta}{V_w} \right]^2 \quad 
    \text{ya que} \quad \frac{0.75^2 \ 29.92}{68+460} = 0.031875 \approx 0.0319
    """)
    st.markdown("""
    y donde $\\theta$ representa el tiempo. En el caso de trabajar con el sistema internacional debemos usar los **factores de conversión** (ver la tercera sección):       
    """)
    st.latex(r"\vphantom{\frac{\left[ \right]^2}{1}} \frac{0.75}{35.3147}\approx 0.02124;\quad 29.92 \cdot 25.4 \approx 760;\quad (68-32)\frac{5}{9}=20.")
    st.write("""
    Con lo cual obtenemos:
    """)
    st.latex(r"""
    \Delta H_@ = \frac{0.0011695 \  \Delta H}{P_{bar}(t_0 + 273.15)} \left[ \frac{(t_w+273.15) \ \theta}{V_w} \right]^2 \quad 
    \text{pues} \quad\frac{0.02124^2 \ 760}{20+273.15}\approx 0.0011695.
    """)
    st.markdown("""
    Nota: el manual *Maintenance Calibration And Operation Of Isokinetic Source-sampling Equipment* utiliza una constante levemente distinta porque trabaja a 70 $F$ en vez 
    de 68 $F$.      
    """)
    st.markdown("""
    **Fuentes:** 
    * [TID-001: Derivation of $\Delta H_@$ for Orifice Meters (EPA)](https://www.epa.gov/sites/default/files/2020-08/documents/tid-01.pdf)
    * [Maintenance Calibration And Operation Of Isokinetic Source-sampling Equipment, Página 12 (20 virtual)](https://nepis.epa.gov/Exe/ZyNET.exe/20013PMH.txt?ZyActionD=ZyDocument&Client=EPA&Index=Prior%20to%201976&Docs=&Query=&Time=&EndTime=&SearchMethod=1&TocRestrict=n&Toc=&TocEntry=&QField=&QFieldYear=&QFieldMonth=&QFieldDay=&UseQField=&IntQFieldOp=0&ExtQFieldOp=0&XmlQuery=&File=D%3A%5CZYFILES%5CINDEX%20DATA%5C70THRU75%5CTXT%5C00000005%5C20013PMH.txt&User=ANONYMOUS&Password=anonymous&SortMethod=h%7C-&MaximumDocuments=1&FuzzyDegree=0&ImageQuality=r75g8/r75g8/x150y150g16/i425&Display=hpfr&DefSeekPage=&SearchBack=ZyActionL&Back=ZyActionS&BackDesc=Results%20page&MaximumPages=1&ZyEntry=2#)
    """)

    st.markdown("---")

    st.markdown("""
    ### 2. Factor de calibración de la consola ($Y$) utilizando el patrón húmedo
    El factor $Y$ compara el volumen medido por el patrón húmedo frente al volumen de la consola bajo las mismas condiones de referencia. Para deducirlo debemos utilizar la ley de los gases ideales que relaciona volúmenes, 
    temperaturas y presiones. Si tenemos un vector de volumen, temperatura y presión $(V, T, P)$ y queremos relacionarlo el mismo gas bajo condiciones de referencia 
    $(V_{(sdt)}, T_{(sdt)}, P_{(sdt)})$, resulta que:
    """)
    st.latex(r"\vphantom{\frac{\left[ \right]^2}{1}} V_{(sdt)} = V\frac{T_{(sdt)}P}{P_{(sdt)} T}")
    st.markdown("""
    donde las temperaturas son absolutas en ambos casos (utilizamos las mayúsculas para distinguirlas). Entonces queremos llevar el volumen patrón ($V_w$ en nuestro caso) a las 
    condiciones de referencia:
    """)
    st.latex(r"\vphantom{\frac{\left[ \right]^2}{1}} V_{w(sdt)}=V_w\frac{T_{(sdt)}P_w}{P_{(sdt)} T_w}=V_w\frac{T_{(sdt)}P_{bar}}{P_{(sdt)} T_w}")
    st.markdown("""
    donde la presión está dada por $P_{bar}$. De igual forma, ahora queremos estudiar el resultado del medidor volumétrico:
    """)
    st.latex(r"V_{m(sdt)}=V_m\frac{T_{(sdt)}P_m}{P_{(sdt)} T_m}=V_m\frac{T_{(sdt)}\left(P_{bar}+\frac{\Delta H}{13.6}\right)}{P_{(sdt)} T_m}")
    st.markdown("""
    donde la presión es la suma de la del barímetro más la del orificio. Notemos que, debido que $\Delta H$ está expresada pulgadas (o milímetros) de agua, debemos 
    dividirla por 13.6 para llevarla a las mimas unidades de $P_{bar}$. Entonces ya podemos deducir la ecuación para $Y$:
    """)
    st.latex(r"""
    Y = \frac{V_{w(sdt)}}{V_{m(sdt)}}= \frac{V_w\frac{T_{(sdt)}P_{bar}}{P_{(sdt)} T_w}}{V_m\frac{T_{(sdt)}\left(P_{bar}+\frac{\Delta H}{13.6}\right)}{P_{(sdt)} T_m}} 
    = \frac{V_w  P_{bar}  T_m}{V_m  (P_{bar} + \frac{\Delta H}{13.6})  T_w}
    """)

    st.markdown("""
    **Fuente:** 
    * [Appendix A-3 to Part 60—Test, Método 5, Sección 12.3](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-60/appendix-Appendix%20A-3%20to%20Part%2060)
    """)

    st.markdown("---")

    st.markdown("""
    ### 3. Unidades
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        #### Sistema Imperial: 
        * Volumen en pies cúbicos ($ft^3$)
        * Presión en pulgadas de mercurio ($in. Hg$)
        * Presión en el orificio en pulgadas de agua ($in. H_2O$)
        * Temperatura Absoluta en Rankine: $^\circ R = ^\circ F + 460$
        * Constante EPA: **0.0319**
        """) 

    with col2:
        st.markdown("""
        ####  Sistema Internacional: 
        * Volumen en metros cúbicos ($m^3$)
        * Presión en milímetros de mercurio ($mm Hg$) 
        * Presión en el orificio en $mm H_2O$
        * Temperatura Absoluta en Kelvin: $K = ^\circ C + 273.15$
        * Constante Convertida: **0.0011695**
        """)

    with col3:
        st.markdown("""
        #### Factores de conversión 
        * 35.3147 $ft^3$ = 1 $m^3$
        * 1 $in. Hg$ = 25.4 $mm Hg$
        * 1 $in. H_2O$ = 25.4 $mm H_2O$
        * $^\circ F =  \\frac95 \,^\circ C +32$
        """)

    st.markdown("---")

    st.markdown("""
    ### 4. Otras consideraciones
    """)

    col_tem, col_med, col_error = st.columns(3)

    with col_tem:
        st.markdown("""
        #### Temperatura 
        La normativa exige el uso de la temperatura absoluta promedio del gas en el medidor.
        """)

        st.latex(r"\vphantom{\frac{\left[ \right]^2}{1}} T_m = \frac{T_{m(entrada)} + T_{m(salida)}}{2}")

    with col_med:
        st.markdown("""
        #### Mediciones 
        La normativa exige promediar al menos tres corridas válidas de ensayo.
        """)

    with col_error:
        st.markdown("""
        #### DIferencias entre los sistemas de unidades 
        La difrencia entre los decimales a pasar del sistema internacional al imperial se deben a los errores de truncamiento y que la EPA exige ajustar la temperatura 
        sumando 460 a los grados Fahrenheit, mientras que el cero absoluto real es -459.67.    
        """)
        
    st.markdown("""
    **Fuentes:** 
    * [40 CFR Parte 60, Apéndice A-3, Método 5, Sección 12.1](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-60/appendix-Appendix%20A-3%20to%20Part%2060)
    * [60.8 Performance tests, (f)](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-60/subpart-A/section-60.8)
    * [TID-001: Derivation of $\Delta H_@$ for Orifice Meters (EPA)](https://www.epa.gov/sites/default/files/2020-08/documents/tid-01.pdf)
    """)