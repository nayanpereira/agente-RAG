import os
import glob
import markdown
from xhtml2pdf import pisa

def converter_md_para_pdf(pasta_alvo):
    # Busca todos os arquivos .md na pasta
    arquivos_md = glob.glob(os.path.join(pasta_alvo, "*.md"))
    
    if not arquivos_md:
        print(f"Nenhum arquivo .md encontrado na pasta '{pasta_alvo}'.")
        return

    for arquivo_md in arquivos_md:
        arquivo_pdf = arquivo_md.replace('.md', '.pdf')
        print(f"Convertendo: {arquivo_md} -> {arquivo_pdf}")
        
        # 1. Lê o conteúdo do arquivo Markdown
        with open(arquivo_md, 'r', encoding='utf-8') as f:
            texto_md = f.read()
            
        # 2. Converte MD para HTML (com suporte a tabelas)
        html = markdown.markdown(texto_md, extensions=['tables'])
        
        # 3. Adiciona um estilo CSS básico para a tabela do balanço financeiro ficar legível
        html_completo = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Helvetica, Arial, sans-serif; font-size: 12px; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 15px; }}
                th, td {{ border: 1px solid #000; padding: 6px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # 4. Gera o arquivo PDF
        with open(arquivo_pdf, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(html_completo, dest=result_file)
            
        if pisa_status.err:
            print(f"[Erro] Falha ao gerar o PDF para {arquivo_md}")
        else:
            print(f"[Sucesso] Criado: {arquivo_pdf}")
            
    print("\nProcesso finalizado!")

if __name__ == "__main__":
    PASTA = "./documentos_base"
    converter_md_para_pdf(PASTA)