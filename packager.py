import os
import subprocess

# Adjust these settings as needed
ENTRY_POINT = 'main.py'
EXCLUDE_DIRS = {'.git', '__pycache__', 'dist', 'build', 'venv'}  # directories to ignore
INCLUDE_EXTENSIONS = {'.csv', '.xlsx', '.pdf', '.docx', '.ipynb', '.txt'}  # file types to include

def generate_datas_list(root='.'):
    datas = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip unwanted directories
        if any(excluded in dirpath.split(os.sep) for excluded in EXCLUDE_DIRS):
            continue
        for file in filenames:
            ext = os.path.splitext(file)[1].lower()
            # Skip Python source files; include only desired file types
            if ext in INCLUDE_EXTENSIONS:
                source = os.path.join(dirpath, file)
                # Preserve folder structure relative to the project root
                target = os.path.relpath(dirpath, root)
                datas.append((source, target))
    return datas

def generate_spec_file(datas, entry_point=ENTRY_POINT):
    # Build the spec file content
    lines = []
    lines.append("block_cipher = None")
    lines.append("")
    lines.append("a = Analysis([r'{}'],".format(entry_point))
    lines.append("             pathex=[],")
    lines.append("             binaries=[],")
    lines.append("             datas=[")
    for source, target in datas:
        # Using raw strings to avoid issues with backslashes
        lines.append("                      (r'{}', r'{}'),".format(source, target))
    lines.append("                      ],")
    lines.append("             hiddenimports=[],")
    lines.append("             hookspath=[],")
    lines.append("             runtime_hooks=[],")
    lines.append("             excludes=[],")
    lines.append("             win_no_prefer_redirects=False,")
    lines.append("             win_private_assemblies=False,")
    lines.append("             cipher=block_cipher)")
    lines.append("pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)")
    lines.append("exe = EXE(pyz,")
    lines.append("          a.scripts,")
    lines.append("          exclude_binaries=True,")
    lines.append("          name='main',")
    lines.append("          debug=False,")
    lines.append("          bootloader_ignore_signals=False,")
    lines.append("          strip=False,")
    lines.append("          upx=True,")
    lines.append("          console=True )")
    lines.append("coll = COLLECT(exe,")
    lines.append("               a.binaries,")
    lines.append("               a.zipfiles,")
    lines.append("               a.datas,")
    lines.append("               strip=False,")
    lines.append("               upx=True,")
    lines.append("               upx_exclude=[],")
    lines.append("               name='main')")
    return "\n".join(lines)

def main():
    datas = generate_datas_list()
    spec_content = generate_spec_file(datas)
    
    spec_filename = 'main.spec'
    with open(spec_filename, 'w') as f:
        f.write(spec_content)
    print(f"Spec file generated as {spec_filename}")

    # Optionally, run PyInstaller with the generated spec file.
    # This call will block until PyInstaller finishes building your executable.
    subprocess.run(['pyinstaller', spec_filename])

if __name__ == '__main__':
    main()