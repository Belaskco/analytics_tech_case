import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_loader import get_db_connection

def run_case_3():
    """
    Gera uma visualização analítica baseada na tabela IMDB_movies.
    
    Racional de Arquitetura:
    Além de plotar o gráfico, o script automatiza a higienização dos dados 
    (tratamento de nulos e normalização de colunas) e exporta o artefato 
    diretamente para a raiz do projeto, pronto para relatórios executivos.
    """
    print("\n" + "="*55)
    print(" DATA VIZ: ANÁLISE DE AVALIAÇÕES (IMDB_movies)")
    print("="*55 + "\n")
    
    # =========================================================
    # 1. EXTRAÇÃO SEGURA (INFRA DEFENSE)
    # =========================================================
    print("-> Conectando ao banco e extraindo IMDB_movies...")
    engine = get_db_connection()
    
    # Mantém a nomenclatura exata solicitada, mas trata a case-sensitivity 
    # do servidor Linux na execução utilizando o .lower()
    query = "SELECT * FROM `looqbox-challenge`.IMDB_movies"
    
    try:
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f"Erro Crítico ao extrair a tabela: {e}")
        return
        
    # =========================================================
    # 2. HIGIENIZAÇÃO E PROGRAMAÇÃO DEFENSIVA
    # =========================================================
    print("-> Normalizando schema e higienizando dados...")
    
    # Padroniza todas as colunas para minúsculo no Pandas para evitar KeyError 
    # caso o schema do banco mude de 'Rating' para 'rating' no futuro.
    df.columns = [col.lower() for col in df.columns]
    
    # Busca dinâmica: encontra a coluna de nota independente do nome exato
    rating_col = next((col for col in df.columns if 'rating' in col or 'score' in col), None)
    
    if not rating_col:
        print("Erro Crítico: Coluna de avaliação (rating/score) não encontrada no schema.")
        return
        
    df_clean = df.dropna(subset=[rating_col])
    
    # =========================================================
    # 3. CONSTRUÇÃO DA VISUALIZAÇÃO (DATA-INK RATIO)
    # =========================================================
    print("-> Renderizando Histograma com Curva de Densidade (KDE)...")
    
    # Tema corporativo
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    
    # Plot principal
    ax = sns.histplot(
        df_clean[rating_col], 
        bins=20, 
        kde=True, 
        color="#2c3e50", 
        edgecolor="white"
    )
    
    plt.title('Distribuição de Avaliações do IMDB', fontsize=14, pad=15, fontweight='bold')
    plt.xlabel('Nota do Filme', fontsize=12)
    plt.ylabel('Frequência (Quantidade de Filmes)', fontsize=12)
    
    # Remove bordas desnecessárias (Princípio de Minimização de Tinta de Edward Tufte)
    sns.despine(left=True)
    
    # =========================================================
    # 4. EXPORTAÇÃO DO ARTEFATO E JUSTIFICATIVA
    # =========================================================
    output_path = "imdb_distribution_chart.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    print(f"-> Sucesso! Gráfico salvo em alta resolução: {os.path.abspath(output_path)}\n")
    
if __name__ == "__main__":
    run_case_3()