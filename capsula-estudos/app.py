import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection, init_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-de-desenvolvimento-local-nao-use-em-producao")

init_db()  # cria as tabelas no banco se ainda não existirem


def login_required(f):
    """Decorator que bloqueia o acesso à rota se o usuário não estiver logado."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Faça login para continuar.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ---------- páginas públicas ----------

@app.route("/")
def home():
    return render_template("index.html")


# ---------- cadastro ----------

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        if not nome or not email or not senha:
            flash("Preencha todos os campos.")
            return redirect(url_for("cadastro"))

        senha_hash = generate_password_hash(senha)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha_hash)
            )
            conn.commit()
        except Exception:
            # email já cadastrado (campo é UNIQUE)
            flash("Esse email já está cadastrado.")
            conn.close()
            return redirect(url_for("cadastro"))

        conn.close()
        flash("Conta criada com sucesso! Faça login.")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


# ---------- login ----------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario is None or not check_password_hash(usuario["senha"], senha):
            flash("Email ou senha incorretos.")
            return redirect(url_for("login"))

        # login certo: guarda o id e o nome do usuário na sessão
        session["user_id"] = usuario["id"]
        session["user_nome"] = usuario["nome"]

        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ---------- logout ----------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ---------- dashboard (área logada) ----------

@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    # total de matérias do usuário
    cursor.execute("SELECT COUNT(*) AS total FROM subjects WHERE user_id = ?", (session["user_id"],))
    total_materias = cursor.fetchone()["total"]

    # total de tópicos e quantos estão pendentes (join com subjects pra filtrar por usuário)
    cursor.execute("""
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN topics.status = 'pendente' THEN 1 ELSE 0 END) AS pendentes
        FROM topics
        JOIN subjects ON subjects.id = topics.subject_id
        WHERE subjects.user_id = ?
    """, (session["user_id"],))
    resultado = cursor.fetchone()
    total_topicos = resultado["total"] or 0
    topicos_pendentes = resultado["pendentes"] or 0

    # próxima revisão (data mais próxima entre os tópicos pendentes com data marcada)
    cursor.execute("""
        SELECT topics.titulo, topics.data_revisao, subjects.nome AS materia_nome
        FROM topics
        JOIN subjects ON subjects.id = topics.subject_id
        WHERE subjects.user_id = ?
          AND topics.status = 'pendente'
          AND topics.data_revisao IS NOT NULL
          AND topics.data_revisao != ''
        ORDER BY topics.data_revisao ASC
        LIMIT 1
    """, (session["user_id"],))
    proxima_revisao = cursor.fetchone()

    conn.close()

    return render_template(
        "dashboard.html",
        nome=session["user_nome"],
        total_materias=total_materias,
        total_topicos=total_topicos,
        topicos_pendentes=topicos_pendentes,
        proxima_revisao=proxima_revisao
    )


def get_materia_do_usuario(materia_id):
    """Busca uma matéria garantindo que ela pertence ao usuário logado. Retorna None se não encontrar."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM subjects WHERE id = ? AND user_id = ?",
        (materia_id, session["user_id"])
    )
    materia = cursor.fetchone()
    conn.close()
    return materia


# ---------- matérias ----------

@app.route("/materias")
@login_required
def materias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subjects WHERE user_id = ? ORDER BY nome", (session["user_id"],))
    lista_materias = cursor.fetchall()
    conn.close()

    return render_template("materias.html", materias=lista_materias)


@app.route("/materias/nova", methods=["GET", "POST"])
@login_required
def nova_materia():
    if request.method == "POST":
        nome = request.form["nome"].strip()

        if not nome:
            flash("Digite o nome da matéria.")
            return redirect(url_for("nova_materia"))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO subjects (user_id, nome) VALUES (?, ?)",
            (session["user_id"], nome)
        )
        conn.commit()
        conn.close()

        flash("Matéria criada com sucesso!")
        return redirect(url_for("materias"))

    return render_template("nova_materia.html")


@app.route("/materias/<int:materia_id>/editar", methods=["GET", "POST"])
@login_required
def editar_materia(materia_id):
    materia = get_materia_do_usuario(materia_id)

    if materia is None:
        flash("Matéria não encontrada.")
        return redirect(url_for("materias"))

    if request.method == "POST":
        nome = request.form["nome"].strip()

        if not nome:
            flash("Digite o nome da matéria.")
            return redirect(url_for("editar_materia", materia_id=materia_id))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE subjects SET nome = ? WHERE id = ? AND user_id = ?",
            (nome, materia_id, session["user_id"])
        )
        conn.commit()
        conn.close()

        flash("Matéria atualizada com sucesso!")
        return redirect(url_for("materias"))

    return render_template("editar_materia.html", materia=materia)


@app.route("/materias/<int:materia_id>/apagar", methods=["POST"])
@login_required
def apagar_materia(materia_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM subjects WHERE id = ? AND user_id = ?",
        (materia_id, session["user_id"])
    )
    conn.commit()
    conn.close()

    flash("Matéria apagada.")
    return redirect(url_for("materias"))


# ---------- tópicos ----------

@app.route("/materias/<int:materia_id>/topicos")
@login_required
def topicos(materia_id):
    materia = get_materia_do_usuario(materia_id)

    if materia is None:
        flash("Matéria não encontrada.")
        return redirect(url_for("materias"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM topics WHERE subject_id = ? ORDER BY status, data_revisao",
        (materia_id,)
    )
    lista_topicos = cursor.fetchall()
    conn.close()

    return render_template("topicos.html", materia=materia, topicos=lista_topicos)


@app.route("/materias/<int:materia_id>/topicos/novo", methods=["GET", "POST"])
@login_required
def novo_topico(materia_id):
    materia = get_materia_do_usuario(materia_id)

    if materia is None:
        flash("Matéria não encontrada.")
        return redirect(url_for("materias"))

    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        resumo = request.form.get("resumo", "").strip()
        dificuldade = request.form.get("dificuldade", "1")
        data_revisao = request.form.get("data_revisao", "").strip()

        if not titulo:
            flash("Digite o título do tópico.")
            return redirect(url_for("novo_topico", materia_id=materia_id))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO topics (subject_id, titulo, resumo, dificuldade, data_revisao, status)
               VALUES (?, ?, ?, ?, ?, 'pendente')""",
            (materia_id, titulo, resumo, int(dificuldade), data_revisao or None)
        )
        conn.commit()
        conn.close()

        flash("Tópico criado com sucesso!")
        return redirect(url_for("topicos", materia_id=materia_id))

    return render_template("novo_topico.html", materia=materia)


def get_topico_da_materia(topico_id, materia_id):
    """Busca um tópico garantindo que ele pertence a uma matéria do usuário logado."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT topics.* FROM topics
           JOIN subjects ON subjects.id = topics.subject_id
           WHERE topics.id = ? AND topics.subject_id = ? AND subjects.user_id = ?""",
        (topico_id, materia_id, session["user_id"])
    )
    topico = cursor.fetchone()
    conn.close()
    return topico


@app.route("/materias/<int:materia_id>/topicos/<int:topico_id>/editar", methods=["GET", "POST"])
@login_required
def editar_topico(materia_id, topico_id):
    materia = get_materia_do_usuario(materia_id)
    if materia is None:
        flash("Matéria não encontrada.")
        return redirect(url_for("materias"))

    topico = get_topico_da_materia(topico_id, materia_id)
    if topico is None:
        flash("Tópico não encontrado.")
        return redirect(url_for("topicos", materia_id=materia_id))

    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        resumo = request.form.get("resumo", "").strip()
        dificuldade = request.form.get("dificuldade", "1")
        data_revisao = request.form.get("data_revisao", "").strip()

        if not titulo:
            flash("Digite o título do tópico.")
            return redirect(url_for("editar_topico", materia_id=materia_id, topico_id=topico_id))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE topics SET titulo = ?, resumo = ?, dificuldade = ?, data_revisao = ?
               WHERE id = ?""",
            (titulo, resumo, int(dificuldade), data_revisao or None, topico_id)
        )
        conn.commit()
        conn.close()

        flash("Tópico atualizado com sucesso!")
        return redirect(url_for("topicos", materia_id=materia_id))

    return render_template("editar_topico.html", materia=materia, topico=topico)


@app.route("/materias/<int:materia_id>/topicos/<int:topico_id>/apagar", methods=["POST"])
@login_required
def apagar_topico(materia_id, topico_id):
    materia = get_materia_do_usuario(materia_id)
    if materia is None:
        flash("Matéria não encontrada.")
        return redirect(url_for("materias"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM topics WHERE id = ? AND subject_id = ?", (topico_id, materia_id))
    conn.commit()
    conn.close()

    flash("Tópico apagado.")
    return redirect(url_for("topicos", materia_id=materia_id))


@app.route("/materias/<int:materia_id>/topicos/<int:topico_id>/alternar-status", methods=["POST"])
@login_required
def alternar_status_topico(materia_id, topico_id):
    materia = get_materia_do_usuario(materia_id)
    if materia is None:
        flash("Matéria não encontrada.")
        return redirect(url_for("materias"))

    topico = get_topico_da_materia(topico_id, materia_id)
    if topico is None:
        flash("Tópico não encontrado.")
        return redirect(url_for("topicos", materia_id=materia_id))

    novo_status = "feito" if topico["status"] == "pendente" else "pendente"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE topics SET status = ? WHERE id = ?", (novo_status, topico_id))
    conn.commit()
    conn.close()

    return redirect(url_for("topicos", materia_id=materia_id))


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    modo_debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=porta, debug=modo_debug)
