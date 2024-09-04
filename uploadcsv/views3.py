import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render

def upload_files(request):
    if request.method == 'POST':
        # Diretório onde os arquivos CSV serão armazenados
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

        # Carregar os arquivos CSV e realizar o filtro
        df1 = pd.read_csv(csv_file_1_path)
        df2 = pd.read_csv(csv_file_2_path)

        result_df = df1[~df1.isin(df2).all(axis=1)]

        # Salvar o resultado no diretório 'csv_files'
        result_file_name = 'resultado_final.csv'
        result_file_path = os.path.join(csv_directory, result_file_name)
        result_df.to_csv(result_file_path, index=False)

        # Passar os arquivos e o resultado para o contexto
        context = {
            'csv_files': {
                'csv_file_1': csv_file_1,
                'csv_file_2': csv_file_2,
                'result_file': os.path.join('csv_files', result_file_name)
            }
        }
        return render(request, 'uploadcsv/upload.html', context)

    return render(request, 'uploadcsv/upload.html')
