# Importação de bibliotecas necessárias
import customtkinter as ctk  # Biblioteca para criar interfaces gráficas modernas
from sympy import symbols, diff, integrate, sympify  # Ferramentas para cálculos matemáticos simbólicos
import re  # Biblioteca para manipulação de expressões regulares

# Configuração da aparência da interface
ctk.set_appearance_mode("dark")  # Define o modo escuro para a interface
ctk.set_default_color_theme("blue")  # Define o tema de cor azul
fonte_titulo = ("Arial", 18, "bold")  # Fonte para títulos
fonte_padrao = ("Arial", 16)  # Fonte padrão para textos
fonte_menor = ("Arial", 14)  # Fonte para textos menores

# Criação da janela principal
janela = ctk.CTk()  # Inicializa a janela principal da interface
janela.title("Calculadora de Derivada e Integral")  # Define o título exibido na barra superior
janela.geometry("440x800")  # Define as dimensões iniciais da janela

# Declaração da variável simbólica para cálculos matemáticos
x = symbols('x')  # Variável padrão usada nos cálculos

# Mapeamento para converter expoentes entre formatos normal e sobrescrito
sobrescritos = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    '-': '⁻'
}
sobrescritos_para_normais = {v: k for k, v in sobrescritos.items()}  # Inversão do mapeamento

# Função para pré-processar a entrada do usuário
def preprocessar_entrada(expr):
    """
    Formata a entrada do usuário para cálculos:
    - Remove espaços desnecessários.
    - Substitui "^" por "**" (sintaxe de potência no Python).
    - Converte expoentes sobrescritos para o formato padrão.
    - Adiciona multiplicações implícitas ausentes (ex: 2x -> 2*x).
    """
    expr = expr.replace(" ", "").replace("^", "**")
    expr = re.sub(
        r'([a-zA-Z])([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)',
        lambda m: m.group(1) + '**' + ''.join(sobrescritos_para_normais.get(c, c) for c in m.group(2)),
        expr
    )
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expr)
    return expr

# Função para formatar expressões para exibição amigável
def formatar_expressao(expr_str):
    """
    Converte a expressão processada para um formato mais legível:
    - Aplica sobrescritos para expoentes.
    - Remove símbolos de multiplicação desnecessários.
    """
    expr_str = expr_str.replace(" ", "")
    expr_str = re.sub(r'([a-zA-Z])\*\*([\-]?\d+)',
                      lambda m: m.group(1) + ''.join(sobrescritos.get(c, c) for c in m.group(2)), expr_str)
    expr_str = re.sub(r'(\d)\*(?=[a-zA-Z])', r'\1', expr_str)
    expr_str = re.sub(r'([a-zA-Z])\*([a-zA-Z])', r'\1\2', expr_str)
    return expr_str

# Função para calcular derivadas de ordens específicas
def derivar(ordem):
    """
    Calcula a derivada da função inserida pelo usuário.
    - Ordem da derivada é definida pelo parâmetro `ordem`.
    - Exibe o resultado formatado na interface.
    """
    entrada_raw = entrada.get().strip()
    if not entrada_raw:
        resultado_label.configure(text="❗ Digite uma função antes de derivar.")
        return
    try:
        expr = preprocessar_entrada(entrada_raw)
        funcao = sympify(expr)
        derivada = funcao
        for _ in range(ordem):
            derivada = diff(derivada, x)
        resultado_label.configure(text=f"Derivada de ordem {ordem}:\n{formatar_expressao(str(derivada))}")
    except Exception as e:
        resultado_label.configure(text=f"Erro: {e}")

# Função para calcular a integral indefinida
def integrar():
    """
    Calcula a integral indefinida da função inserida.
    - Exibe o resultado formatado na interface.
    """
    entrada_raw = entrada.get().strip()
    if not entrada_raw:
        resultado_label.configure(text="❗ Digite uma função antes de integrar.")
        return
    try:
        expr = preprocessar_entrada(entrada_raw)
        funcao = sympify(expr)
        integral = integrate(funcao, x)
        resultado_label.configure(text=f"Integral:\n{formatar_expressao(str(integral))} + C")
    except Exception as e:
        resultado_label.configure(text=f"Erro: {e}")

# Função para calcular a integral definida
def integrar_definida():
    """
    Calcula a integral definida entre limites inferiores e superiores.
    - Exige que os limites sejam fornecidos pelo usuário.
    """
    entrada_raw = entrada.get().strip()
    limite_inferior = limite_inf.get().strip()
    limite_superior = limite_sup.get().strip()

    if not entrada_raw or not limite_inferior or not limite_superior:
        resultado_label.configure(text="❗ Digite a função e os limites inferior e superior.")
        return

    try:
        expr = preprocessar_entrada(entrada_raw)
        funcao = sympify(expr)
        limite_inferior = float(limite_inferior)
        limite_superior = float(limite_superior)
        integral_definida = integrate(funcao, (x, limite_inferior, limite_superior))
        resultado_label.configure(text=f"Integral definida:\n{round(float(integral_definida), 2)}")
    except Exception as e:
        resultado_label.configure(text=f"Erro: {e}")

# Função para exibir instruções e exemplos de entrada
def mostrar_ajuda():
    """
    Exibe uma janela de ajuda com exemplos e instruções para o usuário.
    """
    ajuda = ctk.CTkToplevel(janela)
    ajuda.title("Ajuda - Exemplos de entrada")
    ajuda.geometry("300x600")
    ajuda.attributes('-topmost', True)

    texto = """
Objetivo do Programa:
Este programa calcula derivadas e integrais de funções matemáticas.

Instruções Gerais:
• Use 'x' como variável principal.
• Para potências, use ^, **, ou sobrescritos (², ³, etc.).
• Evite usar espaços desnecessários na entrada.

Exemplos Válidos:
• x² + 2x + 1
• x³ - 4x² + x - 7
• x^2 + 3x
• x**3 + 5

Integral Definida:
• Digite a função no campo principal.
• Insira o limite inferior no campo correspondente.
• Insira o limite superior no campo correspondente.

Erros Comuns:
• 'Digite uma função antes de derivar': Nenhuma expressão foi inserida para o cálculo.
• 'Digite a função e os limites inferior e superior': Alguma informação necessária para a integral definida está faltando.

Para outras dúvidas:
Consulte a documentação ou peça ajuda ao desenvolvedor.
"""
    ctk.CTkLabel(ajuda, font=fonte_menor, text=texto, justify="left", wraplength=280).pack(padx=10, pady=10)

def limpar_tudo():
    entrada.delete(0, 'end')
    limite_inf.delete(0, 'end')
    limite_sup.delete(0, 'end')
    resultado_label.configure(text="")

# Configuração da interface gráfica
frame_input = ctk.CTkFrame(janela, fg_color="transparent")
frame_input.pack(pady=35)

entrada = ctk.CTkEntry(frame_input, width=315, height=40,font=fonte_menor, placeholder_text="Digite a função...")  # Campo de entrada para a função
entrada.pack(side="left", padx=22)

botao_ajuda = ctk.CTkButton(frame_input, font=fonte_padrao, height=40 , width=40, text="?", command=mostrar_ajuda)  # Botão para mostrar ajuda
botao_ajuda.pack(side="left")

resultado_label = ctk.CTkLabel(janela, font=fonte_titulo, height=40, width=315, text="")  # Rótulo para exibir resultados
resultado_label.pack(pady=35)

# Botões para operações matemáticas
ctk.CTkButton(janela, width=160, height=40, text="Derivar 1ª ordem", command=lambda: derivar(1), font=fonte_padrao).pack(pady=5)
ctk.CTkButton(janela, width=160, height=40, text="Derivar 2ª ordem", command=lambda: derivar(2), font=fonte_padrao).pack(pady=5)
ctk.CTkButton(janela, width=160, height=40, text="Derivar 3ª ordem", command=lambda: derivar(3), font=fonte_padrao).pack(pady=5)
ctk.CTkButton(janela, width=160, height=40, text="Integral Indefinida", command=integrar, font=fonte_padrao).pack(pady=5)

# Configuração para entrada de limites
frame_limites = ctk.CTkFrame(janela, fg_color="transparent")
frame_limites.pack(pady=10)

limite_inf = ctk.CTkEntry(frame_limites, width=75, height=40, font=fonte_menor, placeholder_text="Limite Inf.")
limite_inf.pack(side="left", padx=5)

limite_sup = ctk.CTkEntry(frame_limites, width=75, height=40, font=fonte_menor, placeholder_text="Limite Sup.")
limite_sup.pack(side="left", padx=5)

ctk.CTkButton(janela, width=160, height=40, text="Integral Definida", command=integrar_definida, font=fonte_padrao).pack(pady=5)

ctk.CTkButton(janela, width=160, height=40, text="🧹 Limpar Tudo", command=limpar_tudo, font=fonte_padrao).pack(pady=10)

# Inicia o loop principal da interface
janela.mainloop()