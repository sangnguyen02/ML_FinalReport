


#@markdown # Convert PDF to PNG
#@markdown ## Setting
#@markdown Please select the image format.
extension = 'JPEG' #@param ["JPEG", "PNG"]
#@markdown Please enter the DPI.
dpi = 200 #@param {type:"slider", min:100, max:500, step:10}

print('Loading...')


import os
import shutil
import zipfile
from time import time

from google.colab import files
from IPython.display import Image, display
from pdf2image import convert_from_bytes, convert_from_path
from tqdm import tqdm

print('\nPlease upload PDF files.')
uploaded = files.upload()

for fn in uploaded.keys():
    print(f'Converting {fn}...')
    currentDir = f'tmp_{int(time()*1000)}'
    os.makedirs(currentDir, exist_ok=True)
    pdfDir = os.path.join(currentDir, fn)
    shutil.move(fn, pdfDir)
    if(pdfDir.lower()[-4:] != '.pdf'):
        print(f'{fn} is not PDF file!')
        continue
    images = convert_from_bytes(uploaded[fn], dpi=dpi, thread_count=os.cpu_count())
    zipDir = os.path.join(currentDir, f'{fn[:-4]}.zip')
    with zipfile.ZipFile(zipDir, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
        with tqdm(images, unit='p') as pbar:
            for number, page in enumerate(pbar, 1):
                name = f'{fn[:-4]}_{number}.{extension.lower()}'
                name = os.path.join(currentDir, name)
                page.save(name, extension)
                new_zip.write(name, arcname=os.path.basename(name))
                pbar.set_postfix_str(f'{os.path.getsize(zipDir):,} bytes')
    print('Convert completed.', 'The download will start...', sep='\n')
    files.download(zipDir)
print('Finished.')
     