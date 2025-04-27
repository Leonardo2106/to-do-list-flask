from flask_bcrypt import check_password_hash

from app import app, db, bcrypt
from flask import render_template, request, session, redirect, url_for, flash
from app.utils.helpers import UsuarioForm, TarefaForm
from app.models import Usuarios, Tarefas


@app.route('/')
def index():
    usuario = None
    if 'usuario_logado' in session:
        usuario = Usuarios.query.filter_by(email=session['usuario_logado']).first()
    nickname = usuario.nickname if usuario else None
    return render_template('index.html', titulo='Home', nickname=nickname, usuario=usuario)

@app.route('/login')
def login():
    form = UsuarioForm()
    usuario = None
    if 'usuario_logado' in session:
        usuario = Usuarios.query.filter_by(email=session['usuario_logado']).first()
    proxima = request.args.get('proxima')
    if not proxima:
        if usuario:
            proxima = url_for('perfil', nickname=usuario.nickname)
        else:
            proxima = url_for('index')
    return render_template('login.html', titulo='Login', proxima=proxima, form=form, usuario=usuario)

@app.route('/auth', methods=['POST', ])
def auth():
    form = UsuarioForm(request.form)
    usuario = Usuarios.query.filter_by(email=form.email.data).first()

    if usuario and check_password_hash(usuario.senha, form.senha.data):
        session['usuario_logado'] = usuario.email
        session['usuario_nickname'] = usuario.nickname
        flash(f'{usuario.nickname} logado com sucesso!')
        proxima_pagina = request.form.get('proxima')
        if not proxima_pagina:
            proxima_pagina = url_for('perfil', nickname=usuario.nickname)
        return redirect(proxima_pagina)
    else:
        flash('email ou senha incorretos!')
        return redirect(url_for('login'))

@app.route('/registrar')
def registrar():
    form = UsuarioForm()
    return render_template('registrar.html', titulo='Registar',form=form)

@app.route('/criar-conta', methods=['POST'])
def criar_conta():
    form = UsuarioForm(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('index'))

    nome = form.nome.data
    nickname = form.nickname.data
    email = form.email.data
    senha = form.senha.data
    confirmar_senha = form.confirmar_senha.data

    if senha != confirmar_senha: # pegando a senha crua
        flash('As senhas não estão iguais!')
        return redirect(url_for('registrar'))

    senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8') #criptografando

    if Usuarios.query.filter_by(email=email).first():
        flash('Esse email já está registrado!')
        return redirect(url_for('registrar'))

    if Usuarios.query.filter_by(nickname=nickname).first():
        flash('Esse nickname já está sendo utilizado!')
        return redirect(url_for('registrar'))

    novo_usuario = Usuarios(nome=nome, nickname=nickname, email=email, senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()

    session['usuario_logado'] = email
    session['usuario_nickname'] = nickname
    flash(f'{nickname} registrado com sucesso!')

    return redirect(url_for('perfil', nickname=nickname))

@app.route('/logout')
def logout():
    if 'usuario_logado' in session:
        session.pop('usuario_logado')
    flash('Logout feito com sucesso!')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar_perfil(id):
    Usuarios.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Perfil deletado com sucesso!')
    return redirect(url_for('logout'))

@app.route('/perfil/<string:nickname>')
def perfil(nickname):
    usuario = Usuarios.query.filter_by(nickname=nickname).first()
    return render_template('perfil.html', titulo='Perfil', nickname=usuario.nickname ,usuario=usuario)

@app.route('/editar-perfil/<string:nickname>')
def editar_perfil(nickname):
    usuario = Usuarios.query.filter_by(nickname=nickname).first()

    form = UsuarioForm(obj=usuario)
    form.nome.data = usuario.nome
    form.nickname.data = usuario.nickname
    form.email.data = usuario.email

    return render_template('editar_perfil.html', titulo='Editar perfil', form=form, nickname=nickname, usuario=usuario)

@app.route('/atualizar-perfil', methods=['POST'])
def atualizar_perfil():
    form = UsuarioForm()
    usuario = Usuarios.query.filter_by(id=request.form['id']).first()
    if not usuario:
        return redirect(url_for('index'))
    if request.method == 'POST' and form.validate():
        usuario.nome = form.nome.data
        usuario.nickname = form.nickname.data
        usuario.email = form.email.data
        if form.senha.data:
            if form.senha.data == form.confirmar_senha.data:
                usuario.senha = bcrypt.generate_password_hash(form.senha.data).decode('utf8')
            else:
                flash('As senhas não estão iguais!')
                return redirect(url_for('editar_perfil', nickname=usuario.nickname))

        db.session.add(usuario)
        db.session.commit()

        flash('Perfil atualizado com sucesso!')
        return redirect(url_for('perfil', nickname=usuario.nickname))
    else:
        flash('Erro ao atualizar perfil!')
        print("Form errors:", form.errors)
        return redirect(url_for('editar_perfil', nickname=usuario.nickname))

@app.route('/tarefas/<string:nickname>')
def tarefas(nickname):
    usuario = Usuarios.query.filter_by(nickname=nickname).first()
    tarefas = Tarefas.query.filter_by(usuario_id=usuario.id).all()
    proxima = url_for('tarefas', nickname=usuario.nickname)

    return render_template('tarefas.html', titulo='Tarefas', nickname=usuario.nickname, usuario=usuario, tarefas=tarefas, proxima=proxima)

@app.route('/criar-tarefa/<string:nickname>', methods=['POST', 'GET'])
def criar_tarefa(nickname):
    usuario = Usuarios.query.filter_by(nickname=nickname).first()

    if request.method == 'POST':
        form = TarefaForm(request.form)
        if form.validate_on_submit():
            titulo = form.titulo.data
            tarefa = form.tarefa.data
            importante = form.importante.data
            prazo = form.prazo.data

            if importante == 'True':
                importante = True
            else:
                importante = False

            nova_tarefa = Tarefas(titulo=titulo, tarefa=tarefa, importante=importante, prazo=prazo, usuario_id=usuario.id)
            db.session.add(nova_tarefa)
            db.session.commit()

            flash(f'Tarefa {nova_tarefa.titulo} criada com sucesso!')
            return redirect(url_for('tarefas', nickname=usuario.nickname))

    form = TarefaForm()
    return render_template('criar_tarefa.html', titulo='Criar Tarefa', form=form, nickname=usuario.nickname, usuario=usuario)

@app.route('/editar-tarefa/<string:nickname>/<int:id>')
def editar_tarefa(nickname, id):
    tarefa = Tarefas.query.filter_by(id=id).first()
    usuario = Usuarios.query.filter_by(nickname=nickname).first()

    form = TarefaForm()
    form.titulo.data = tarefa.titulo
    form.tarefa.data = tarefa.tarefa
    form.importante.data = tarefa.importante
    form.prazo.data = tarefa.prazo

    return render_template('editar_tarefa.html', titulo='Editando Tarefa', form=form, nickname=usuario.nickname, usuario=usuario, id=tarefa.id)

@app.route('/atualizar-tarefa', methods=['POST', 'GET'])
def atualizar_tarefa():
    usuario = Usuarios.query.filter_by(email=session['usuario_logado']).first()
    if request.method == 'POST':
        form = TarefaForm(request.form)
        if form.validate_on_submit():
            tarefa = Tarefas.query.filter_by(id=request.form['id']).first()
            tarefa.titulo = form.titulo.data
            tarefa.tarefa = form.tarefa.data
            tarefa.importante = form.importante.data
            tarefa.prazo = form.prazo.data

            if tarefa.importante == 'True':
                tarefa.importante = True
            else:
                tarefa.importante = False

            db.session.add(tarefa)
            db.session.commit()

            flash(f'Tarefa atualizada com sucesso!')
            return redirect(url_for('tarefas', nickname=usuario.nickname))

    form = TarefaForm()
    return render_template('editar_tarefa.html', titulo='Editando Tarefa', form=form, nickname=usuario.nickname, usuario=usuario)

@app.route('/deletar-tarefa/<int:id>')
def deletar_tarefa(id):
    usuario = Usuarios.query.filter_by(email=session['usuario_logado']).first()
    Tarefas.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Tarefa deletada com sucesso!')

    return redirect(url_for('tarefas', titulo='Tarefas', nickname=usuario.nickname, id=id))

