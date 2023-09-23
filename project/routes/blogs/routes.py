from datetime import datetime

from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy import func

from project.extensions import db

from project.routes.blogs import bp

from project.models.user import User
from project.models.blog import Blog, Category, Comment


# Global variable
global_all_category_num = None
global_all_category_name = None

def get_all_categories():
    global global_all_category_num, global_all_category_name
    all_category_info = db.session.query(Category.category_id, Category.category_name)
    all_category_info = list(all_category_info)

    global_all_category_num, global_all_category_name = zip(*all_category_info)


@bp.route("/blogs")
def blogs():
    # if current_user.is_authenticated and current_user.confirmed:
    #     return render_template("blogs/view_blog.html")
    return redirect(url_for('blogs.list_all_blogs'))

@bp.route("/createBlog", methods=['GET', 'POST'])
@login_required
def create_blog():
    if request.method == 'POST':
        category_id = request.form.get("category_id")
        blog_text = request.form.get("blog_text")
        today = datetime.now()
        blog_user_id = current_user.id
        blog_read_count = 0
        blog_rating_count = 0
        
        newBlog = Blog(category_id=category_id,
                       blog_user_id=blog_user_id,
                       blog_text=blog_text,
                       blog_creation_date=today,
                       blog_read_count=blog_read_count,
                       blog_rating_count=blog_rating_count)
        
        db.session.add(newBlog)
        db.session.commit()
        return redirect("blogs")
    else:
        return render_template("blogs/create_blog.html", all_category_id=global_all_category_num, all_category_name=global_all_category_name)
    
@bp.route("/viewBlog")
@login_required
def view_blogs():
    all_self_blogs = Blog.objects(Blog.blog_user_id == current_user.id)
    return render_template("blogs/view_blog.html", all_self_blogs=all_self_blogs, all_categories=global_all_category_name)

@bp.route("/self_blog_detail/<int:blog_model_id>/<string:blog_model_category>", methods=["GET", "POST"])
@login_required
def self_blog_detail(blog_model_id, blog_model_category):
    blog_model = Blog.query.get(blog_model_id)
    if request.method == "POST":
        if request.form['action'] == 'Update':
            blog_model.blog_text = request.form.get('blog_text')
        elif request.form['action'] == 'Delete':
            Blog.query.filter_by(id=blog_model_id).delete()
        db.session.commit()
        return redirect('/viewBlog')
    return render_template("blogs/self_blog_detail.html", blog_text=blog_model.blog_text)

@bp.route("/listAllBlogs")
def list_all_blogs():
    all_blogs = Blog.objects.find()
    all_users = User.objects.find()
    return render_template('blogs/list_all_blogs.html', all_blogs=all_blogs, all_users=all_users, all_categories=global_all_category_name)

@bp.route('/blogDetail/<int:blog_model_id>/<string:username>/<string:blog_model_category>', methods=["GET", "POST"])
@login_required
def blog_detail(blog_model_id, username, blog_model_category):
    blog_model = Blog.query.get(blog_model_id)
    
    if request.method == 'GET':
        if current_user.id != blog_model.blog_user_id:
            blog_model.blog_read_count += 1
            db.session.commit()
        rating = db.session.query(func.avg(Comment.blog_rating)).filter(Comment.blog_id == int(blog_model_id)).first()[0]
        return render_template('blogs/blog_detail.html', blog=blog_model, rating=rating, author=username, category=blog_model_category)
    else:
        rate = request.form.get('rating')
        comment = request.form.get('comment')
        blog_id = request.form.get('blog_id')
        print("Comment: ", comment)
        
        old_comment = Comment.query.filter(Comment.blog_id == blog_model_id).filter(Comment.comment_user_id == current_user.id).first()
        print("Old Comment: ", old_comment.blog_comment)
        today = datetime.now()
        
        if old_comment is None:
            blog_model.blog_rating_count += 1
            
            new_comment = Comment(
                blog_id=blog_model_id,
                comment_user_id=current_user.id,
                blog_comment=comment,
                blog_rating=rate,
                blog_comment_date=today)
            db.session.add(new_comment)
        else:
            old_comment.blog_comment = comment
            old_comment.blog_rating = rate
        db.session.commit()
        return redirect('/blogs')
