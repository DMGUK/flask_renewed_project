from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.todo import todo
from app.todo.forms import ToDoForm
from app.todo.models import Todo


@todo.route('/todo_list')
@login_required
def todo_list():
    todolist = db.session.query(Todo).all()
    return render_template("todo.html", todo_list=todolist, active="ToDo", title="ToDo")

@todo.route('/view_todo/<int:todo_id>')
def view_todo(todo_id):
    todo = Todo.query.get(todo_id)
    return render_template("view_todo.html", todo=todo)

@todo.route("/add_todo", methods=["POST"])
def add_todo():
    todo_form = ToDoForm()
    if todo_form.validate_on_submit():
        title = todo_form.title.data
        description = todo_form.description.data
        new_todo = Todo(title=title, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        flash("Todo task has been successfully added", category='flash-success')
        return redirect(url_for("todo.todo_list"))
    flash("Error adding todo task", category='flash-error')
    return redirect(url_for("todo.todo_list"))

@todo.route("/update_todo/<int:todo_id>")
@login_required
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo.view_todo", todo_id=todo_id))

@todo.route("/delete_todo/<int:todo_id>")
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash("Todo task has been successfully deleted", category='flash-success')
    return redirect(url_for("todo.todo_list"))

@todo.route("/create_todo")
@login_required
def create_todo():
    todo_form = ToDoForm()
    return render_template("create_todo.html", todo_form=todo_form)