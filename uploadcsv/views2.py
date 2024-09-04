from django.shortcuts import render, redirect

from .models import CSVFile
import pandas as pd
import os
from django.conf import settings

def upload_files(request):
    if request.method == 'POST':
        csv_file_1 = request.FILES['csv_file_1']
        csv_file_2 = request.FILES['csv_file_2']

        if csv_file_1 and csv_file_2:
            # Salvando os arquivos no banco de dados
            csv_files = CSVFile.objects.create(csv_file_1=csv_file_1, csv_file_2=csv_file_2)

            # carregando e processando os csvs
            csv1 = pd.read_csv(csv_files.csv_file_1)
            csv2 = pd.read_csv(csv_files.csv_file_2)

            # identificando linhas repetidas
            linhas_repetidas = pd.merge(csv1, csv2, how='inner')
            csv1_unicas = csv1.drop(linhas_repetidas.index)
            csv2_unicas = csv2.drop(linhas_repetidas.index)

            # # combinando e salvando o resultado final
            # resultado_final = pd.concat([csv1_unicas, csv2_unicas])
            # result_csv_filename = f'resultado_final_{csv_files.id}.csv'
            # result_csv_path = os.path.join('csv_files', result_csv_filename)
            # full_result_path = os.path.join(settings.MEDIA_ROOT, result_csv_path)
            # os.makedirs(os.path.dirname(full_result_path), exists_ok=True)
            # resultado_final.to_csv(full_result_path, index=False)

            # Combinando e salvando o resultado final
            resultado_final = pd.concat([csv1_unicas, csv2_unicas])
            result_csv_path = f'csv_files/resultado_final_{csv_files.id}.csv'
            resultado_final.to_csv(result_csv_path, index=False)

            # atualizando o caminho do arquivo de resultado no banco
            csv_files.result_file = result_csv_path
            csv_files.save()

            return redirect('upload_files')
    else:
        # para exibir o último arquivo enviado
        csv_files = CSVFile.objects.last()

    return render(request, 'uploadcsv/upload.html', {'csv_files': csv_files})


