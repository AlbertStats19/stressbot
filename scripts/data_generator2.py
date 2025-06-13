import pandas as pd
import numpy as np
import os
import random
import json
import re # Para sanitizar nombres
import unicodedata # Para sanitizar nombres
from faker import Faker
from utils import timer # Asumo que utils.py está en la misma carpeta scripts/
# SI utils.py está en notebooks/, esta línea debería ser ajustada en tu entorno
# Si el error persiste, la importación relativa 'from .utils import timer' + __init__.py en scripts/
# es la solución robusta, pero por ahora seguimos con la que te funciona.

fake = Faker('es_CO') # Usar Faker con localización colombiana para nombres/fechas

def sanitize_folder_name(name):
    """Sanitiza un nombre de empresa para usarlo como nombre de carpeta."""
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
    name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
    return name

def generate_companies(num_companies=25):
    """
    Genera una lista de nombres de empresas colombianas simuladas
    y sus nombres de carpeta sanitizados.
    """
    company_data = []
    for i in range(num_companies):
        original_name = fake.company() + " S.A.S."
        sanitized_name = sanitize_folder_name(f"empresa_{i+1}_{original_name}")
        company_data.append({
            "original_name": original_name,
            "sanitized_folder_name": sanitized_name
        })
    return company_data # Retorna una lista de diccionarios

def generate_transactions_data(num_records=2_000, company_names_original=None): # REDUCIDO A 2,000
    """Genera datos simulados de transacciones."""
    print(f"Generando {num_records} registros de transacciones (LIGHT)...")
    data = {
        'transaction_id': np.arange(num_records),
        'company_name': np.random.choice(company_names_original, num_records),
        'date': pd.to_datetime([fake.date_between(start_date='-5y', end_date='today') for _ in range(num_records)]),
        'amount': np.random.uniform(1000, 1000000, num_records).round(2),
        'type': np.random.choice(['DEBIT', 'CREDIT'], num_records),
        'description': [fake.sentence(nb_words=5) for _ in range(num_records)],
    }
    df = pd.DataFrame(data)
    return df

def generate_financial_data(num_records=1_000, company_names_original=None): # REDUCIDO A 1,000
    """Genera datos simulados de métricas financieras."""
    print(f"Generando {num_records} registros financieros (LIGHT)...")
    data = {
        'financial_id': np.arange(num_records),
        'company_name': np.random.choice(company_names_original, num_records),
        'year': np.random.choice(np.arange(2019, 2024), num_records),
        'revenue': np.random.uniform(1_000_000, 100_000_000, num_records).round(2),
        'profit': np.random.uniform(100_000, 20_000_000, num_records).round(2),
        'liquidity_ratio': np.random.uniform(0.5, 3.0, num_records).round(2),
        'debt_equity_ratio': np.random.uniform(0.1, 2.5, num_records).round(2),
        'cash_flow': np.random.uniform(-5_000_000, 10_000_000, num_records).round(2),
    }
    df = pd.DataFrame(data)
    return df

def generate_pdf_content(company_name, doc_type):
    """Genera contenido textual simulado para un tipo de PDF."""
    if doc_type == 'gestion':
        return (
            f"Informe de Gestión {company_name} - Resumen Anual.\n"
            f"En el último año, {company_name} ha experimentado un crecimiento del {random.randint(5, 20)}% en sus operaciones, "
            f"consolidando su presencia en el mercado {fake.word()}."
            f"Los proyectos estratégicos se enfocaron en {fake.sentence(nb_words=10)}. "
            f"La fuerza laboral actual asciende a {random.randint(50, 1000)} empleados. "
            f"Se ha lanzado una iniciativa de sostenibilidad que busca reducir la huella de carbono en un {random.randint(10, 30)}%."
            f"Las inversiones futuras se centran en {fake.sentence(nb_words=8)}."
            f"El directorio aprobó un plan de inversión de $ {random.randint(100_000, 5_000_000):,} USD para nuevas tecnologías."
        )
    elif doc_type == 'sectorial':
        return (
            f"Análisis Sectorial del Mercado {fake.city()} - Impacto en {company_name}.\n"
            f"El sector {fake.word()} ha mostrado una recuperación, con un aumento del {random.randint(3, 15)}% en el último trimestre. "
            f"La competencia principal incluye a {fake.company()} y {fake.company()}. "
            f"Nuevas regulaciones sobre {fake.word()} podrían afectar las operaciones en el futuro cercano. "
            f"Las tendencias indican una mayor digitalización y enfoque en {fake.word()}."
        )
    elif doc_type == 'financiero':
        return (
            f"Estado Financiero Consolidado {company_name} - Análisis Clave.\n"
            f"Los ingresos de {company_name} alcanzaron los $ {random.randint(1_000_000, 50_000_000):,} USD en el último año, con una utilidad neta de $ {random.randint(100_000, 5_000_000):,} USD. "
            f"Los activos totales son de $ {random.randint(500_000, 20_000_000):,} USD y los pasivos de $ {random.randint(100_000, 10_000_000):,} USD. "
            f"El ratio de liquidez actual es de {random.uniform(1.0, 2.5):.2f}. "
            f"Se observa una mejora en el flujo de caja operativo del {random.randint(5, 25)}%."
        )
    return ""

def main():
    output_data_dir = 'data'
    output_docs_dir = 'company_docs'

    os.makedirs(output_data_dir, exist_ok=True)
    os.makedirs(output_docs_dir, exist_ok=True)

    print("Generando nombres de empresas y mapeo de carpetas...")
    company_data_list = generate_companies(num_companies=25)
    # Extraer solo los nombres originales para usar en los DataFrames
    company_names_original = [item["original_name"] for item in company_data_list]
    print(f"Empresas generadas: {len(company_data_list)}")

    # Guardar el mapeo de empresas a un archivo JSON
    company_mapping_path = os.path.join(output_data_dir, 'company_mapping.json')
    with open(company_mapping_path, 'w', encoding='utf-8') as f:
        json.dump(company_data_list, f, indent=4)
    print(f"Mapeo de empresas guardado en {company_mapping_path}.")

    # Generar data de transacciones (LIGHT)
    with timer("Generación de data de transacciones (LIGHT)"):
        transactions_df = generate_transactions_data(num_records=2_000, company_names_original=company_names_original)
        transactions_df.to_csv(os.path.join(output_data_dir, 'simulated_transactions.csv'), index=False)
    print("Data de transacciones LIGHT guardada.")

    # Generar data financiera (LIGHT)
    with timer("Generación de data financiera (LIGHT)"):
        financial_df = generate_financial_data(num_records=1_000, company_names_original=company_names_original)
        financial_df.to_csv(os.path.join(output_data_dir, 'simulated_financial_metrics.csv'), index=False)
    print("Data financiera LIGHT guardada.")

    # Generar contenido de PDFs por empresa
    print("\nGenerando contenido de documentos (PDFs simulados) por empresa...")
    for item in company_data_list:
        original_name = item["original_name"]
        sanitized_folder_name = item["sanitized_folder_name"]
        
        company_dir = os.path.join(output_docs_dir, sanitized_folder_name)
        os.makedirs(company_dir, exist_ok=True)

        with timer(f"Generando documentos para {original_name}"):
            with open(os.path.join(company_dir, 'gestion.txt'), 'w', encoding='utf-8') as f:
                f.write(generate_pdf_content(original_name, 'gestion'))
            with open(os.path.join(company_dir, 'sectorial.txt'), 'w', encoding='utf-8') as f:
                f.write(generate_pdf_content(original_name, 'sectorial'))
            with open(os.path.join(company_dir, 'financiero.txt'), 'w', encoding='utf-8') as f:
                f.write(generate_pdf_content(original_name, 'financiero'))
        print(f"Documentos para {original_name} guardados en {company_dir}.")

    print("\n¡Generación de datos LIGHT completa!")

if __name__ == "__main__":
    main()