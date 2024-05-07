from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'acy9ehb7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:acy9ehb7@localhost:3306/cadastros'
db = SQLAlchemy(app)

class Cargo(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(40), nullable=True)

    def __str__(self):
        return f'Cargo{self.nome}'

class Setor(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(40), nullable=True)

    def __str__(self):
        return f'Setor{self.nome}'

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(40), nullable=False)
    sobrenome = db.Column(db.String(40), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    status_funcionario = db.Column(db.Integer, nullable=False)
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id'), nullable=False)
    setor = db.relationship('Setor', backref=db.backref('funcionarios', lazy=True))
    cargo = db.relationship('Cargo', backref=db.backref('funcionarios', lazy=True))

    def __str__(self):
        return f"('Funcionario{self.nome}', '{self.sobrenome}', '{self.status_funcionario}')"
    
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    funcionarios = Funcionario.query.all()
    return render_template('index.html', funcionarios=funcionarios)

@app.route('/cadastrar_funcionario', methods=['GET', 'POST'])
def cadastrar_funcionarios():
    if request.method == 'POST':
        
        nome = request.form['nome'].capitalize()
        sobrenome = request.form['sobrenome'].capitalize()
        data_admissao = request.form['data_admissao']
        status_funcionario = request.form.get('status_funcionario', False)
        id_setor = request.form['id_setor']
        id_cargo = request.form['id_cargo']
        
        novo_funcionario = Funcionario(
            nome=nome,
            sobrenome=sobrenome,
            data_admissao=data_admissao,
            status_funcionario=status_funcionario,
            id_setor=id_setor,
            id_cargo=id_cargo
        )
        
        db.session.add(novo_funcionario)
        db.session.commit()
        session['funcionario_cadastrado'] = True
        return redirect('/cadastrar_funcionario')
    
    setores = Setor.query.all()
    cargos = Cargo.query.all()
    return render_template('cadastrar_funcionarios.html', setores=setores, cargos=cargos)

@app.route('/setor', methods=['GET', 'POST'])
def setor():
    if request.method == 'POST':
        nome = request.form['setor'].capitalize()
        novo_setor = Setor(nome=nome)
        db.session.add(novo_setor)
        db.session.commit()
        return redirect('/setor')
    
    setores = Setor.query.all()
    return render_template('setor.html', setores=setores)

@app.route('/cargo', methods=['GET', 'POST'])
def cargo():
    if request.method == 'POST':
        nome = request.form['cargo'].capitalize()
        novo_cargo = Cargo(nome=nome)
        db.session.add(novo_cargo)
        db.session.commit()
        return redirect('/cargo')
    
    setores = Setor.query.all()
    return render_template('cargo.html', setores=setores)

@app.route('/excluir_funcionario/<int:funcionario_id>', methods=['POST'])
def excluir_funcionario(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)
    db.session.delete(funcionario)
    db.session.commit()
    return redirect('/')

@app.route('/voltar', methods=['GET'])
def voltar():
    return redirect('/')

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)