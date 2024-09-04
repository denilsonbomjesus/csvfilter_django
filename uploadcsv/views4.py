from django.shortcuts import render

from .models import CSVFile
import pandas as pd
import os
from django.conf import settings

def upload_files(request):
    if request.method == 'POST':
        # Verificar se o diretório 'csv_files' dentro de MEDIA_ROOT existe, caso contrário, criá-lo
        csv_directory = os.path.join(settings.MEDIA_ROOT, 'csv_files')
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)
        
        # Salvar os arquivos CSV no diretório 'csv_files'
        csv_file_1 = request.FILES['csv_file_1']
        csv_file_2 = request.FILES['csv_file_2']

        if csv_file_1 and csv_file_2:
            # Salvando os arquivos no banco de dados
            csv_files = CSVFile.objects.create(csv_file_1=csv_file_1, csv_file_2=csv_file_2)

            # # carregando e processando os csvs
            # csv1 = pd.read_csv(csv_files.csv_file_1)
            # csv2 = pd.read_csv(csv_files.csv_file_2)

            # # identificando linhas repetidas
            # linhas_repetidas = pd.merge(csv1, csv2, how='inner')
            # csv1_unicas = csv1.drop(linhas_repetidas.index)
            # csv2_unicas = csv2.drop(linhas_repetidas.index)

            # # Salvar o resultado no diretório 'csv_files'
            # resultado_final = pd.concat([csv1_unicas, csv2_unicas])
            # result_file_path = os.path.join(csv_directory, f'resultado_final_{csv_files.id}.csv')
            # resultado_final.to_csv(result_file_path, index=False)

            csv_file_1_path = os.path.join(csv_directory, csv_file_1.name)
            csv_file_2_path = os.path.join(csv_directory, csv_file_2.name)

            # Carregar os arquivos CSV e realizar o filtro
            df1 = pd.read_csv(csv_file_1_path)
            df2 = pd.read_csv(csv_file_2_path)

            resultado_final = df1[~df1.isin(df2).all(axis=1)]

            # Salvar o resultado no diretório 'csv_files'
            result_file_path = os.path.join(csv_directory, f'resultado_final_{csv_files.id}.csv')
            resultado_final.to_csv(result_file_path, index=False)

            # Passar os arquivos e o resultado para o contexto
            context = {
                'csv_files': {
                    'csv_file_1': csv_file_1,
                    'csv_file_2': csv_file_2,
                    'resultado_final': os.path.join('media', 'csv_files', 'resultado_final_{csv_files.id}.csv')
                }
            }
            return render(request, 'uploadcsv/upload.html', context)

        return render(request, 'uploadcsv/upload.html')


    #         # Combinando e salvando o resultado final
    #         resultado_final = pd.concat([csv1_unicas, csv2_unicas])
    #         result_csv_path = f'csv_files/resultado_final_{csv_files.id}.csv'
    #         resultado_final.to_csv(result_csv_path, index=False)

    #         # atualizando o caminho do arquivo de resultado no banco
    #         csv_files.result_file = result_csv_path
    #         csv_files.save()

    #         return redirect('upload_files')
    # else:
    #     # para exibir o último arquivo enviado
    #     csv_files = CSVFile.objects.last()

    # return render(request, 'uploadcsv/upload.html', {'csv_files': csv_files})


