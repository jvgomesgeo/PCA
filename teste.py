
import streamlit as st
import folium
import pandas as pd
import plotly.express as px
from datetime import datetime
from plotly.subplots import make_subplots
import pydeck as pdk
import os
from streamlit_folium import folium_static
from streamlit_gsheets import GSheetsConnection



st.set_page_config(layout = 'wide', page_title = 'Dashboard PCA', page_icon= "💹")


@st.cache_data()
def load_dados(path):
    df = pd.read_excel(path)
    df['Bairro'] = df['Bairro'].astype(str)
    bairros = ['Todos'] + sorted(df['Bairro'].unique().tolist())

    coluna_nome = 'Qual área da infraestrutura da sua comunidade precisa de atenção?'
    options_list = [
        "Calçamento/Pavimentação",
        "Coleta de lixo",
        "Iluminação pública",
        "Recapeamento (reparo do asfalto)",
        "Saneamento",
        "Poda de árvore",
        "Outros"
    ]

    for option in options_list:
        df[option + '_bool'] = df[coluna_nome].apply(lambda x: 'Precisa de Atenção' if option in str(x) else 'Não Precisa de Atenção')

    coluna_nome = 'Qual área da educação na sua comunidade precisa de atenção?'
    options_list = [
        "Infraestrutura escolar",
        "Quantidade de professores",
        "Material escolar",
        "Outro"
        ]

    for option in options_list:
        df[option + '_bool'] = df[coluna_nome].apply(lambda x: 'Precisa de Atenção' if option in str(x) else 'Não Precisa de Atenção')

    coluna_nome = 'Qual área de esporte e lazer na sua comunidade precisa de atenção?'
    options_list = [
        "Praças",
        "Atividades esportivas",
        "Atividades culturais",
        "Áreas verdes",
        "Outro"
        ]

    for option in options_list:
        df[option + '_bool'] = df[coluna_nome].apply(lambda x: 'Precisa de Atenção' if option in str(x) else 'Não Precisa de Atenção')

    coluna_nome = 'Qual área da saúde na sua comunidade precisa de atenção?'
    options_list = [
        "Postos de saúde",
        "Profissionais de saúde",
        "Fornecimento de Medicamentos",
        "Marcação de Consultas e Exames"
        ]

    for option in options_list:
        df[option + '_bool'] = df[coluna_nome].apply(lambda x: 'Precisa de Atenção' if option in str(x) else 'Não Precisa de Atenção')

    coluna_nome = 'Qual área da segurança pública na sua comunidade precisa de atenção?'
    options_list = [
        "Monitoramento",
        "Outro"
        ]

    for option in options_list:
        df[option + '_bool'] = df[coluna_nome].apply(lambda x: 'Precisa de Atenção' if option in str(x) else 'Não Precisa de Atenção')


    coluna_nome = 'Qual área social na sua comunidade precisa de atenção?'
    options_list = [
        "Acesso a Programas de Assistência Social",
        "Apoio a Grupos Vulneráveis",
        "População de rua"
        ]

    for option in options_list:
        df[option + '_bool'] = df[coluna_nome].apply(lambda x: 'Precisa de Atenção' if option in str(x) else 'Não Precisa de Atenção')

    for option in options_list:
        df[option + '_bool'] = df[coluna_nome].apply(lambda x: 'Precisa de Atenção' if option in str(x) else 'Não Precisa de Atenção')


    coluna_nome = 'Qual área do transporte na sua comunidade precisa de atenção?'
    options_list = [
        "Infraestrutura de transporte (Ex: abrigo de passageiros)",
        "Quantidade de linhas e horários dos ônibus",
        "Acessibilidade",
        "Trânsito"
        ]

    for option in options_list:
        df[option + '_bool'] = df[coluna_nome].apply(lambda x: 'Precisa de Atenção' if option in str(x) else 'Não Precisa de Atenção')

    return df


df = load_dados(os.getcwd()  +'/dfs/PCA- Comunidades de Angra  COPIA.xlsx')
bairros = ['Todos'] + sorted(df['Bairro'].unique().tolist())
df['Bairro'] = df['Bairro'].astype(str)


# Estilo CSS
st.markdown(
    """
    <style>
        .main {background-color: #f4f4f4;}
        .stText, .stTitle, .stSubheader {color: #333333;}
        .css-1d391kg {color: #333333;}
    </style>
    """,
    unsafe_allow_html=True
)

# Cabeçalho com logo e título
col_logo, col_titulo = st.columns([1.5, 3])
with col_logo:
    st.image('logo.png', width=400)
with col_titulo:
    st.markdown("<h1 style='text-align: center;'>Programa Comunidades Angra - PCA</h1>", unsafe_allow_html=True)
 
    
#filtro de seleção do bairro:
bairro_caixas = st.sidebar.multiselect('Selecione o(s) Bairro (s)', bairros)


if 'Todos' in bairro_caixas or not bairro_caixas:
    df_filter = df.copy()
else:
    df_filter = df[df['Bairro'].isin(bairro_caixas)]


#DF DE EXIBIÇÃO
with st.container(border = True, height= 300):
    df_exibição = df.drop(['Trânsito_bool', 'Acessibilidade_bool',
       'Quantidade de linhas e horários dos ônibus_bool',
       'Infraestrutura de transporte (Ex: abrigo de passageiros)_bool',
       'População de rua_bool', 'Apoio a Grupos Vulneráveis_bool',
       'Acesso a Programas de Assistência Social_bool', 'Monitoramento_bool',
       'Marcação de Consultas e Exames_bool',
       'Fornecimento de Medicamentos_bool', 'Profissionais de saúde_bool',
       'Postos de saúde_bool', 'Áreas verdes_bool',
       'Atividades culturais_bool', 'Atividades esportivas_bool',
       'Praças_bool', 'Outro_bool', 'Material escolar_bool',
       'Quantidade de professores_bool', 'Infraestrutura escolar_bool',
       'Outros_bool', 'Poda de árvore_bool', 'Saneamento_bool',
       'Recapeamento (reparo do asfalto)_bool', 'Iluminação pública_bool',
       'Coleta de lixo_bool', 'Calçamento/Pavimentação_bool', 'lon', 'lat',], axis= 1)
    st.subheader(f" Registros coletados do PCA no(s) bairro(s)")
    st.dataframe(df_exibição)


aba1, aba2, aba3 = st.tabs(["Visão Geral", "Avaliações", "Distribuição Espacial"])


with aba1:
    col_1, col_2, col_3 = st.columns([1,0.7,1], vertical_alignment= 'top', border= True)
    with col_1: 
        with st.container(border = True, height= 350):
            st.subheader("Informações Gerais do(s) bairro(s) selecionado(s)")
            st.text(f"Quantidade de Formulários Preenchidos: {len(df_filter)} unidades")
            st.text(f"Tempo Médio de Moradia: {int(df_filter['Há quanto tempo mora no bairro? (em anos)'].mean())}")

            
        with st.container(border = True, height= 450):
            fig_sexo = px.bar(df_filter, x = 'Gênero', color= 'Gênero', template= 'simple_white',  
                            title = 'Distribuição de Gênero:' )
            fig_sexo.update_xaxes(title_text =  ' ')
            fig_sexo.update_yaxes(title_text =  'Respostas Coletadas')
            fig_sexo.update_layout(width = 250, height = 350)
            st.plotly_chart(fig_sexo) 
        
    with col_2:
        with st.container(border = True, height= 350): 
            df_pie = df_filter['Raça'].value_counts().reset_index()
            df_pie.columns = ['Raça', 'Quantidade']
            fig_pie = px.pie(df_pie, values = 'Quantidade',
                            names = 'Raça', 
                            title = 'Distribuição racial', 
                            template= 'simple_white')
            fig_pie.update_layout(width = 250, height = 350)
            st.plotly_chart(fig_pie)
        with st.container(border = True, height= 450):
            fig_idade = px.histogram(df_filter, x = 'Idade', template= 'simple_white', 
                                     color= 'Gênero', title = 'Faixa Etária')
            fig_idade.update_yaxes(title_text = 'Respostas Coeltadas')
            st.plotly_chart(fig_idade)



    with col_3:
        with st.container(border = True, height= 800):
            fig_moradia = px.histogram(df_filter, y = 'Há quanto tempo mora no bairro? (em anos)', color = 'Gênero', template= 'simple_white', title= 'Tempo de Moradia')
            fig_moradia.update_yaxes(title_text = 'Respostas Coeltadas')
            fig_moradia.update_xaxes(title_text = 'Tempo de moradia (em anos)')
            fig_moradia.update_layout(width = 600, height = 800)

            st.plotly_chart(fig_moradia)

           

with aba2:

    col_4, col_5, col_6 = st.columns([2,2,2], vertical_alignment= 'top', border= True)
    with col_4:

        calcamento_graph = px.bar(df_filter, x = 'Avaliação quanto ao fornecimento de Serviços Públicos na sua comunidade: [Calçamento]' ,
                color = 'Gênero', template= 'simple_white', title = 'Avaliação do Calçamento')

        seguranca_graph = px.bar(df_filter, x = 'Avaliação quanto ao fornecimento de Serviços Públicos na sua comunidade: [Segurança]', 
                        color = 'Gênero', template= 'simple_white', title = 'Avaliação da Segurança')

        lixo_graph = px.bar(df_filter, x = 'Avaliação quanto ao fornecimento de Serviços Públicos na sua comunidade: [Coleta de lixo]', 
                        color = 'Gênero', template= 'simple_white', title = 'Avaliação da Coleta de Lixo')

        educacao_graph = px.bar(df_filter, x = 'Avaliação quanto ao fornecimento de Serviços Públicos na sua comunidade: [Educação]',
                        color = 'Gênero', template= 'simple_white', title = 'Avaliação da Educação')

        lazer_graph = px.bar(df_filter, x = 'Avaliação quanto ao fornecimento de Serviços Públicos na sua comunidade: [Lazer]', 
                        color = 'Gênero', template= 'simple_white', title = 'Avaliação da Lazer')

        iluminacao_graph = px.bar(df_filter, x = 'Avaliação quanto ao fornecimento de Serviços Públicos na sua comunidade: [Iluminação Pública]', 
                        color = 'Gênero', template= 'simple_white', title = 'Avaliação da Iluminação Pública')

        saneamento_graph = px.bar(df_filter, x = 'Avaliação quanto ao fornecimento de Serviços Públicos na sua comunidade: [Saneamento]', 
                        color = 'Gênero', template= 'simple_white', title = 'Avaliação do Saneamento')

        saude_graph = px.bar(df_filter, x = 'Avaliação quanto ao fornecimento de Serviços Públicos na sua comunidade: [Saúde]', 
                        color = 'Gênero', template= 'simple_white', title = 'Avaliação da Saúde')

        social_graph = px.bar(df_filter, x = 'Avaliação quanto ao fornecimento de Serviços Públicos na sua comunidade: [Social]', 
                        color = 'Gênero', template= 'simple_white', title = 'Avaliação do Social')

        transporte_graph = px.bar(df_filter, x = 'Avaliação quanto ao fornecimento de Serviços Públicos na sua comunidade: [Transporte]', 
                        color = 'Gênero', template= 'simple_white', title = 'Avaliação do Transporte')



        list_charts = [calcamento_graph, seguranca_graph,lixo_graph, educacao_graph, lazer_graph, iluminacao_graph,
                    saneamento_graph, saude_graph, social_graph, transporte_graph]

        list_charts_name = ['Avaliação do Calçamento', 'Avaliação da Segurança', 'Avaliação da Coleta de Lixo', 
                            'Avaliação da Educação', 'Avaliação da Lazer', 'Avaliação da Iluminação Pública', 
                            'Avaliação do Saneamento', 'Avaliação da Saúde', 'Avaliação do Social', 'Avaliação do Transporte']
        
        with st.container(border=True):
            selected_chart_name = st.selectbox("# Selecione o tipo de Avaliação", list_charts_name)
            selected_chart = list_charts[list_charts_name.index(selected_chart_name)]
            selected_chart.update_xaxes(title_text =  ' ')
            selected_chart.update_yaxes(title_text =  'Respostas Coletadas')
            st.plotly_chart(selected_chart)
    
    with col_5:

        list_areas = ['Infraestrutura', 'Educação', 'Lazer', 'Saúde', 'Segurança Pública',
                    'Social', 'Transporte']
        
        dict_troubles = {
                        'Infraestrutura': ['Calçamento/Pavimentação','Coleta de lixo', 'Iluminação pública','Recapeamento (reparo do asfalto)', "Saneamento", "Poda de árvore", "Outros"],
                        'Educação': ['Infraestrutura escolar','Quantidade de professores', 'Material escolar', 'Outro'],
                        'Lazer': ['Praças', 'Atividades esportivas', 'Atividades culturais', 'Áreas verdes','Outro'],
                        'Saúde': ['Postos de saúde','Profissionais de saúde', 'Fornecimento de Medicamentos', 'Marcação de Consultas e Exames'],
                        'Segurança Pública': ['Monitoramento', 'Outro'],
                        'Social': ['Acesso a Programas de Assistência Social', 'Apoio a Grupos Vulneráveis', 'População de rua'],
                        'Transporte': ['Infraestrutura de transporte (Ex: abrigo de passageiros)', 'Quantidade de linhas e horários dos ônibus', 'Trânsito']
                        }
        
        fig_dict = {
            'Calçamento/Pavimentação': px.bar(df_filter, x='Calçamento/Pavimentação_bool', color= 'Gênero', template= 'simple_white'),
            'Poda de árvore': px.bar(df_filter, x='Poda de árvore_bool', color= 'Gênero', template= 'simple_white'),
            'Saneamento': px.bar(df_filter, x='Saneamento_bool', color= 'Gênero', template= 'simple_white'),
            'Recapeamento (reparo do asfalto)': px.bar(df_filter, x='Recapeamento (reparo do asfalto)_bool', color= 'Gênero', template= 'simple_white'),
            'Coleta de lixo': px.bar(df_filter, x='Coleta de lixo_bool', color= 'Gênero', template= 'simple_white'),
            'Infraestrutura escolar' :px.bar(df_filter, x='Infraestrutura escolar_bool', color= 'Gênero', template= 'simple_white'),
            'Quantidade de professores': px.bar(df_filter, x='Quantidade de professores_bool', color= 'Gênero', template= 'simple_white'), 
            'Material escolar': px.bar(df_filter, x='Material escolar_bool', color= 'Gênero', template= 'simple_white'), 
            'Praças':px.bar(df_filter, x='Praças_bool', color= 'Gênero', template= 'simple_white'), 
            'Atividades esportivas': px.bar(df_filter, x='Atividades esportivas_bool', color= 'Gênero', template= 'simple_white'), 
            'Atividades culturais': px.bar(df_filter, x='Atividades culturais_bool', color= 'Gênero', template= 'simple_white'), 
            'Áreas verdes': px.bar(df_filter, x='Áreas verdes_bool', color= 'Gênero', template= 'simple_white'),
            'Postos de saúde': px.bar(df_filter, x='Postos de saúde_bool', color= 'Gênero', template= 'simple_white'),
            'Profissionais de saúde': px.bar(df_filter, x='Profissionais de saúde_bool', color= 'Gênero', template= 'simple_white'), 
            'Fornecimento de Medicamentos': px.bar(df_filter, x='Fornecimento de Medicamentos_bool', color= 'Gênero', template= 'simple_white'), 
            'Marcação de Consultas e Exames': px.bar(df_filter, x='Marcação de Consultas e Exames_bool', color= 'Gênero', template= 'simple_white'),
            'Monitoramento': px.bar(df_filter, x='Monitoramento_bool', color= 'Gênero', template= 'simple_white'),
            'Acesso a Programas de Assistência Social': px.bar(df_filter, x='Acesso a Programas de Assistência Social_bool', color= 'Gênero', template= 'simple_white'), 
            'Apoio a Grupos Vulneráveis': px.bar(df_filter, x='Apoio a Grupos Vulneráveis_bool', color= 'Gênero', template= 'simple_white'), 
            'População de rua': px.bar(df_filter, x='População de rua_bool', color= 'Gênero', template= 'simple_white'),
            'Infraestrutura de transporte (Ex: abrigo de passageiros)': px.bar(df_filter, x='Infraestrutura de transporte (Ex: abrigo de passageiros)_bool', color= 'Gênero', template= 'simple_white'), 
            'Quantidade de linhas e horários dos ônibus': px.bar(df_filter, x='Quantidade de linhas e horários dos ônibus_bool', color= 'Gênero', template= 'simple_white'), 
            'Trânsito': px.bar(df_filter, x='Trânsito_bool', color= 'Gênero', template= 'simple_white')
        }
        
        selection_area = st.selectbox('Selecione o Serviço Pública', list_areas)
        

        if selection_area in dict_troubles.keys():
            selection_trouble = st.selectbox('Selecione o Tipo de Problema', dict_troubles[selection_area])
            
            if selection_trouble in fig_dict:
                fig = fig_dict[selection_trouble]
                fig.update_xaxes(title_text =  ' ')
                fig.update_yaxes(title_text =  'Respostas Coletadas')
                col_5.plotly_chart(fig)
        
            else:
                col_5.write('Não há dados dispponíveis para essa opção')
   
    with col_6:

        df_pie_col6 = df_filter['Teria alguma demanda específica quanto à algum tipo de serviço público na sua comunidade?'].value_counts().reset_index()
        df_pie_col6.columns = ['Teria alguma demanda específica quanto à algum tipo de serviço público na sua comunidade?', 'Quantidade']

        fig_pie_col6 = px.pie(df_pie_col6, values = 'Quantidade', 
                names = 'Teria alguma demanda específica quanto à algum tipo de serviço público na sua comunidade?', 
                title = 'Demanda específica quanto à algum tipo de serviço público', 
                template= 'simple_white')
        col_6.plotly_chart(fig_pie_col6)    

with aba3:
    with st.container(border= True,height= 600):
        st.subheader("Mapa de Registros")
        st.map(df_filter)


    