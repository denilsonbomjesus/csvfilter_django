import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render

def upload_files(request):
    if request.method == 'POST':
        # Verificar se o diretório 'csv_files' dentro de MEDIA_ROOT existe, caso contrário, criá-lo
        csv_directory = os.path.join(settings.MEDIA_ROOT, 'csv_files')
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        # Salvar os arquivos CSV no diretório 'csv_files'
        csv_file_1 = request.FILES['csv_file_1']
        csv_file_2 = request.FILES['csv_file_2']

        csv_file_1_path = os.path.join(csv_directory, csv_file_1.name)
        csv_file_2_path = os.path.join(csv_directory, csv_file_2.name)

        with open(csv_file_1_path, 'wb+') as destination:
            for chunk in csv_file_1.chunks():
                destination.write(chunk)

        with open(csv_file_2_path, 'wb+') as destination:
            for chunk in csv_file_2.chunks():
                destination.write(chunk)

        # Carregar as duas planilhas CSV
        csv1 = pd.read_csv(csv_file_1_path, header=None)
        csv2 = pd.read_csv(csv_file_2_path, header=None)

        # Encontrar as linhas que são únicas para cada CSV
        unicas_csv1 = csv1[~csv1.apply(tuple, axis=1).isin(csv2.apply(tuple, axis=1))]
        unicas_csv2 = csv2[~csv2.apply(tuple, axis=1).isin(csv1.apply(tuple, axis=1))]

        # Combinar as linhas únicas de ambas as planilhas
        resultado_final = pd.concat([unicas_csv1, unicas_csv2])

        # Salvar o resultado final em um novo CSV sem cabeçalho
        result_file_name = 'result.csv'
        result_file_path = os.path.join(csv_directory, result_file_name)
        resultado_final.to_csv(result_file_path, index=False, header=False)

        # Passar os arquivos e o resultado para o contexto
        context = {
            'csv_files': {
                'csv_file_1': csv_file_1,
                'csv_file_2': csv_file_2,
                'result_file': os.path.join(settings.MEDIA_URL, 'csv_files', result_file_name)
            }
        }
        return render(request, 'uploadcsv/upload.html', context)

    return render(request, 'uploadcsv/upload.html')
