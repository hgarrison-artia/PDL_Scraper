block_cipher = None

a = Analysis([r'main.py'],
             pathex=[],
             binaries=[],
             datas=[
                      (r'./drugs.csv', r'.'),
                      (r'./GA/GA_PDL.csv', r'GA'),
                      (r'./GA/GA_non_pdl_output.xlsx', r'GA'),
                      (r'./GA/GA.pdf', r'GA'),
                      (r'./GA/GA_completed_output.xlsx', r'GA'),
                      (r'./GA/GA_skipped_output.xlsx', r'GA'),
                      (r'./MS/MS.pdf', r'MS'),
                      (r'./MS/MS_completed_output.xlsx', r'MS'),
                      (r'./MS/MS.docx', r'MS'),
                      (r'./MS/MS_non_pdl_output.xlsx', r'MS'),
                      (r'./MS/MS_PDL.csv', r'MS'),
                      (r'./MS/MS_skipped_output.xlsx', r'MS'),
                      (r'./AK/AK_PDL.csv', r'AK'),
                      (r'./AK/AK_output_data.csv', r'AK'),
                      (r'./AK/AK_data.csv', r'AK'),
                      (r'./AK/AK_skipped_data.csv', r'AK'),
                      (r'./AK/AK.pdf', r'AK'),
                      (r'./CO/CO.docx', r'CO'),
                      (r'./CO/CO_non_pdl_output.xlsx', r'CO'),
                      (r'./CO/CO_PDL.csv', r'CO'),
                      (r'./CO/CO_completed_output.xlsx', r'CO'),
                      (r'./CO/CO_skipped_output.xlsx', r'CO'),
                      (r'./CO/CO_test.ipynb', r'CO'),
                      (r'./CO/.ipynb_checkpoints/CO_test-checkpoint.ipynb', r'CO/.ipynb_checkpoints'),
                      (r'./IA/IA_non_pdl_output.xlsx', r'IA'),
                      (r'./IA/IA.xlsx', r'IA'),
                      (r'./IA/IA_completed_output.xlsx', r'IA'),
                      (r'./IA/IA.ipynb', r'IA'),
                      (r'./IA/IA_skipped_output.xlsx', r'IA'),
                      (r'./IA/IA.pdf', r'IA'),
                      (r'./IA/readme.txt', r'IA'),
                      (r'./IA/IA_PDL.csv', r'IA'),
                      (r'./FL/FL.xlsx', r'FL'),
                      (r'./FL/FL_completed_output.xlsx', r'FL'),
                      (r'./FL/FL_non_pdl_output.xlsx', r'FL'),
                      (r'./FL/FL.pdf', r'FL'),
                      (r'./FL/FL.ipynb', r'FL'),
                      (r'./FL/readme.txt', r'FL'),
                      (r'./FL/FL_skipped_output.xlsx', r'FL'),
                      (r'./FL/FL_PDL.csv', r'FL'),
                      (r'./myenv/lib/python3.12/site-packages/pandas-2.2.3.dist-info/entry_points.txt', r'myenv/lib/python3.12/site-packages/pandas-2.2.3.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pillow-11.1.0.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/pillow-11.1.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/tabula_py-2.10.0.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/tabula_py-2.10.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/python_docx-1.1.2.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/python_docx-1.1.2.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info/CC-BY-4.0.txt', r'myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info/LicenseRef-PdfiumThirdParty.txt', r'myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info/entry_points.txt', r'myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info/BSD-3-Clause.txt', r'myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info/Apache-2.0.txt', r'myenv/lib/python3.12/site-packages/pypdfium2-4.30.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/openpyxl-3.1.5.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/openpyxl-3.1.5.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pip-24.0.dist-info/entry_points.txt', r'myenv/lib/python3.12/site-packages/pip-24.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pip-24.0.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/pip-24.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pip-24.0.dist-info/LICENSE.txt', r'myenv/lib/python3.12/site-packages/pip-24.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pip-24.0.dist-info/AUTHORS.txt', r'myenv/lib/python3.12/site-packages/pip-24.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/et_xmlfile-2.0.0.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/et_xmlfile-2.0.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/et_xmlfile-2.0.0.dist-info/AUTHORS.txt', r'myenv/lib/python3.12/site-packages/et_xmlfile-2.0.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/rapidfuzz-3.12.2.dist-info/entry_points.txt', r'myenv/lib/python3.12/site-packages/rapidfuzz-3.12.2.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/lxml-5.3.1.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/lxml-5.3.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/lxml-5.3.1.dist-info/LICENSE.txt', r'myenv/lib/python3.12/site-packages/lxml-5.3.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/lxml-5.3.1.dist-info/LICENSES.txt', r'myenv/lib/python3.12/site-packages/lxml-5.3.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/cffi-1.17.1.dist-info/entry_points.txt', r'myenv/lib/python3.12/site-packages/cffi-1.17.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/cffi-1.17.1.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/cffi-1.17.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pdfminer.six-20231228.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/pdfminer.six-20231228.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/ma/API_CHANGES.txt', r'myenv/lib/python3.12/site-packages/numpy/ma'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/include/numpy/random/LICENSE.txt', r'myenv/lib/python3.12/site-packages/numpy/_core/include/numpy/random'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log2.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arcsinh.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arctanh.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-sin.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-cos.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-cbrt.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arctan.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-cosh.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-README.txt', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-expm1.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-sinh.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-tanh.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log10.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arcsin.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arccos.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log1p.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-log.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-exp2.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-arccosh.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-tan.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/_core/tests/data/umath-validation-set-exp.csv', r'myenv/lib/python3.12/site-packages/numpy/_core/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/random/tests/data/philox-testset-1.csv', r'myenv/lib/python3.12/site-packages/numpy/random/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/random/tests/data/philox-testset-2.csv', r'myenv/lib/python3.12/site-packages/numpy/random/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/random/tests/data/sfc64-testset-1.csv', r'myenv/lib/python3.12/site-packages/numpy/random/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/random/tests/data/sfc64-testset-2.csv', r'myenv/lib/python3.12/site-packages/numpy/random/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/random/tests/data/mt19937-testset-2.csv', r'myenv/lib/python3.12/site-packages/numpy/random/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/random/tests/data/mt19937-testset-1.csv', r'myenv/lib/python3.12/site-packages/numpy/random/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/random/tests/data/pcg64-testset-1.csv', r'myenv/lib/python3.12/site-packages/numpy/random/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/random/tests/data/pcg64-testset-2.csv', r'myenv/lib/python3.12/site-packages/numpy/random/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/random/tests/data/pcg64dxsm-testset-1.csv', r'myenv/lib/python3.12/site-packages/numpy/random/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/numpy/random/tests/data/pcg64dxsm-testset-2.csv', r'myenv/lib/python3.12/site-packages/numpy/random/tests/data'),
                      (r'./myenv/lib/python3.12/site-packages/pdfplumber-0.11.5.dist-info/entry_points.txt', r'myenv/lib/python3.12/site-packages/pdfplumber-0.11.5.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pdfplumber-0.11.5.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/pdfplumber-0.11.5.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pdfplumber-0.11.5.dist-info/LICENSE.txt', r'myenv/lib/python3.12/site-packages/pdfplumber-0.11.5.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pip/_vendor/vendor.txt', r'myenv/lib/python3.12/site-packages/pip/_vendor'),
                      (r'./myenv/lib/python3.12/site-packages/thefuzz-0.22.1.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/thefuzz-0.22.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/thefuzz-0.22.1.dist-info/LICENSE.txt', r'myenv/lib/python3.12/site-packages/thefuzz-0.22.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/python_dateutil-2.9.0.post0.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/python_dateutil-2.9.0.post0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/charset_normalizer-3.4.1.dist-info/entry_points.txt', r'myenv/lib/python3.12/site-packages/charset_normalizer-3.4.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/charset_normalizer-3.4.1.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/charset_normalizer-3.4.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/tzdata-2025.1.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/tzdata-2025.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pycparser-2.22.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/pycparser-2.22.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/jpype1-1.5.2.dist-info/entry_points.txt', r'myenv/lib/python3.12/site-packages/jpype1-1.5.2.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/jpype1-1.5.2.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/jpype1-1.5.2.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/distro-1.9.0.dist-info/entry_points.txt', r'myenv/lib/python3.12/site-packages/distro-1.9.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/distro-1.9.0.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/distro-1.9.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/fuzzywuzzy-0.18.0.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/fuzzywuzzy-0.18.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/fuzzywuzzy-0.18.0.dist-info/LICENSE.txt', r'myenv/lib/python3.12/site-packages/fuzzywuzzy-0.18.0.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/readme.txt', r'myenv/lib/python3.12/site-packages/lxml/isoschematron/resources/xsl/iso-schematron-xslt1'),
                      (r'./myenv/lib/python3.12/site-packages/pytz-2025.1.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/pytz-2025.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/pytz-2025.1.dist-info/LICENSE.txt', r'myenv/lib/python3.12/site-packages/pytz-2025.1.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/docx/templates/default.docx', r'myenv/lib/python3.12/site-packages/docx/templates'),
                      (r'./myenv/lib/python3.12/site-packages/numpy-2.2.3.dist-info/entry_points.txt', r'myenv/lib/python3.12/site-packages/numpy-2.2.3.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/numpy-2.2.3.dist-info/LICENSE.txt', r'myenv/lib/python3.12/site-packages/numpy-2.2.3.dist-info'),
                      (r'./myenv/lib/python3.12/site-packages/six-1.17.0.dist-info/top_level.txt', r'myenv/lib/python3.12/site-packages/six-1.17.0.dist-info'),
                      (r'./IL/IL.ipynb', r'IL'),
                      (r'./IL/IL_PDL.csv', r'IL'),
                      (r'./IL/IL_non_pdl_output.xlsx', r'IL'),
                      (r'./IL/IL_completed_output.xlsx', r'IL'),
                      (r'./IL/IL.xlsx', r'IL'),
                      (r'./IL/readme.txt', r'IL'),
                      (r'./IL/IL_skipped_output.xlsx', r'IL'),
                      (r'./LA/LA_skipped_data.csv', r'LA'),
                      (r'./LA/LA_output_data.csv', r'LA'),
                      (r'./LA/LA.pdf', r'LA'),
                      (r'./LA/LA_PDL.csv', r'LA'),
                      (r'./LA/LA.ipynb', r'LA'),
                      (r'./LA/LA.docx', r'LA'),
                      (r'./LA/LA_data.csv', r'LA'),
                      (r'./LA/readme.txt', r'LA'),
                      (r'./TN/Tenncare-PDL.pdf', r'TN'),
                      (r'./TN/TN.docx', r'TN'),
                      (r'./TN/~$nncare-PDL.pdf', r'TN'),
                      (r'./TN/TN-1.docx', r'TN'),
                      (r'./TN/TN.ipynb', r'TN'),
                      ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')