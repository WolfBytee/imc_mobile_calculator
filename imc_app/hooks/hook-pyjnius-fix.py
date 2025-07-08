import os

def apply_patch_to_pyjnius(build_dir):
    # Caminho provável onde o pyjnius está extraído durante o build
    pyjnius_dir = os.path.join(build_dir, 'other_builds', 'pyjnius-sdl2')

    if not os.path.isdir(pyjnius_dir):
        print("Pyjnius directory não encontrado no build, ignorando patch.")
        return

    # Vamos percorrer subdiretórios para encontrar os arquivos .pxi
    for root, dirs, files in os.walk(pyjnius_dir):
        for filename in files:
            if filename.endswith('.pxi'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    content = f.read()

                # Substituir "isinstance(arg, long)" por "isinstance(arg, int)"
                new_content = content.replace('isinstance(arg, long)', 'isinstance(arg, int)')

                if new_content != content:
                    print(f"Aplicando patch em: {filepath}")
                    with open(filepath, 'w') as f:
                        f.write(new_content)

def hook(ctx):
    build_dir = ctx.build_dir
    apply_patch_to_pyjnius(build_dir)
