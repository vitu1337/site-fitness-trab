from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 1. Página Inicial
@app.route('/')
def index():
    return render_template('index.html')

# 2. Página Sobre
@app.route('/about')
@app.route('/sobre')
def about():
    return render_template('sobre.html')

# 3. Tela de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', 'maykol@gmail.com')
        return redirect(url_for('profile', nome=usuario, email=usuario, idade=25, peso=70.5, altura=1.75))
    return render_template('login.html')

# 4. Perfil do Usuário
@app.route('/profile')
@app.route('/perfil')
def profile():
    nome = request.args.get('nome', 'maykol@gmail.com')
    email = request.args.get('email', 'maykol@gmail.com')
    idade = request.args.get('idade', 25, type=int)
    peso = request.args.get('peso', 70.5, type=float)
    altura = request.args.get('altura', 1.75, type=float)
    return render_template('profile.html', nome=nome, email=email, idade=idade, peso=peso, altura=altura)

# 5. Cálculos Matemáticos
@app.route('/math/<op>/<float:a>/<float:b>')
@app.route('/math/<op>/<int:a>/<int:b>')
def math_route(op, a, b):
    operacoes = {
        'soma': ('Soma', '+'),
        'subtracao': ('Subtração', '-'),
        'multiplicacao': ('Multiplicação', '×'),
        'divisao': ('Divisão', '÷')
    }
    
    nome_op, simbolo = operacoes.get(op.lower(), ('Operação', '?'))
    
    if op.lower() == 'divisao' and b == 0:
        resultado = "Erro: Divisão por zero"
    else:
        if op.lower() == 'soma': resultado = a + b
        elif op.lower() == 'subtracao': resultado = a - b
        elif op.lower() == 'multiplicacao': resultado = a * b
        elif op.lower() == 'divisao': resultado = round(a / b, 2)
        else: resultado = "Operação inválida"

    return render_template('matem.html', nome_op=nome_op, simbolo=simbolo, a=a, b=b, resultado=resultado)

@app.route('/calcular_math', methods=['POST'])
def calcular_math():
    op = request.form.get('operacao', 'soma')
    num1 = request.form.get('num1', 0)
    num2 = request.form.get('num2', 0)
    return redirect(url_for('math_route', op=op, a=num1, b=num2))

# 6. Calculadora de IMC
@app.route('/imc/<float:peso>/<float:altura>', methods=['GET'])
@app.route('/imc', methods=['GET'])
def imc_route(peso=None, altura=None):
    if peso is None:
        peso = request.args.get('peso', 70.0, type=float)
    if altura is None:
        altura = request.args.get('altura', 1.75, type=float)

    idade = request.args.get('idade', 25, type=int)
    sexo = request.args.get('sexo', 'Outro')

    if altura <= 0 or peso <= 0:
        return redirect(url_for('index'))

    # Cálculo do IMC
    imc = round(peso / (altura ** 2), 2)

    # Faixa do IMC
    if imc < 18.5:
        faixa = 'Magreza'
    elif 18.5 <= imc < 25:
        faixa = 'Normal'
    elif 25 <= imc < 30:
        faixa = 'Sobrepeso'
    else:
        faixa = 'Obesidade'

    # Peso Ideal (IMC entre 18.5 e 24.9)
    peso_ideal_min = round(18.5 * (altura ** 2), 1)
    peso_ideal_max = round(24.9 * (altura ** 2), 1)

    # Estimativa de Gordura Corporal (Deurenberg)
    sexo_val = 1 if sexo == 'Masculino' else 0
    gordura = round((1.20 * imc) + (0.23 * idade) - (10.8 * sexo_val) - 5.4, 1)

    if sexo == 'Masculino':
        if gordura < 6: faixa_gordura = 'Essencial'
        elif gordura < 14: faixa_gordura = 'Atleta'
        elif gordura < 18: faixa_gordura = 'Fitness'
        elif gordura < 25: faixa_gordura = 'Aceitável'
        else: faixa_gordura = 'Obesidade'
    else:
        if gordura < 14: faixa_gordura = 'Essencial'
        elif gordura < 21: faixa_gordura = 'Atleta'
        elif gordura < 25: faixa_gordura = 'Fitness'
        elif gordura < 32: faixa_gordura = 'Aceitável'
        else: faixa_gordura = 'Obesidade'

    # Posição da régua (0% a 100%)
    posicao_regua = max(0, min(100, int(((imc - 10) / (40 - 10)) * 100)))

    return render_template(
        'imc.html',
        peso=peso,
        altura=altura,
        sexo=sexo,
        idade=idade,
        imc=imc,
        faixa=faixa,
        peso_ideal_min=peso_ideal_min,
        peso_ideal_max=peso_ideal_max,
        gordura=gordura,
        faixa_gordura=faixa_gordura,
        posicao_regua=posicao_regua
    )

@app.route('/calcular_imc', methods=['POST'])
def calcular_imc():
    peso = request.form.get('peso', 70.0, type=float)
    altura = request.form.get('altura', 1.75, type=float)
    sexo = request.form.get('sexo', 'Outro')
    idade = request.form.get('idade', 25, type=int)
    
    return redirect(url_for('imc_route', peso=peso, altura=altura, idade=idade, sexo=sexo))

if __name__ == '__main__':
    app.run(debug=True)