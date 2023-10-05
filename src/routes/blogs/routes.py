import json
import datetime
from flask_user import (
    login_required,
    current_user
)
from flask import (
    render_template,
    redirect,
    url_for,
    request
)
from src.models.user import User
from src.models.blog import Blog, Category, Comment
from src.routes.blogs import bp


# Global variable
global_all_category_num = []
global_all_category_name = []


def get_all_categories():
    global global_all_category_num, global_all_category_name

    for cat in Category.objects.all():
        dict_cat = json.loads(cat.to_json())
        global_all_category_num.append(dict_cat['_id']['$oid'])
        global_all_category_name.append(dict_cat['category_name'])


@bp.route("/blogs")
def blogs():
    return redirect(url_for('blogs.list_all_blogs'))


# CRUD for Blogs
@bp.route("/listAllBlogs")
def list_all_blogs():
    all_blogs = reversed(Blog.objects.all())  # reverse to display recent ones on the top
    all_users = User.objects.all()
    all_categories = Category.objects.all()
    return render_template('blogs/list_all_blogs.html', all_blogs=all_blogs, all_users=all_users, all_categories=all_categories)


@bp.route("/createBlog", methods=['GET', 'POST'])
@login_required
def create_blog():
    if request.method == 'POST':
        category_id = request.form.get("category_id")
        blog_text = request.form.get("blog_text")
        today = datetime.datetime.utcnow()
        blog_user_id = current_user.id
        blog_read_count = 0
        blog_rating_count = 0

        newBlog = Blog(category_id=category_id,
                       blog_user_id=blog_user_id,
                       blog_text=blog_text,
                       blog_creation_date=today,
                       blog_read_count=blog_read_count,
                       blog_rating_count=blog_rating_count)

        newBlog.save()
        return redirect("blogs")
    else:
        print(global_all_category_num)
        print(global_all_category_name)
        return render_template("blogs/create_blog.html", all_category_id=global_all_category_num, all_category_name=global_all_category_name)


@bp.route("/viewBlog")
@login_required
def view_blogs():
    all_categories = Category.objects.all()
    
    user = User.objects.filter(id=current_user.id).all()[0]
    if user.username == 'admin':
        all_self_blogs = Blog.objects.all()
    else:
        all_self_blogs = Blog.objects.filter(blog_user_id=current_user.id).all()

    all_self_blogs = reversed(all_self_blogs)  # reverse to display recent ones on the top
    return render_template("blogs/view_blog.html", all_self_blogs=all_self_blogs, all_categories=all_categories)


@bp.route("/self_blog_detail/<string:blog_id>/<string:blog_category>", methods=["GET", "POST"])
@login_required
def self_blog_detail(blog_id, blog_category):
    blog = Blog.objects.filter(id=blog_id).first()
    if request.method == "POST":
        if request.form['action'] == 'Update':
            blog.blog_text = request.form.get('blog_text')
        elif request.form['action'] == 'Delete':
            Blog.objects.filter(id=blog_id).first().delete()
        blog.save()
        return redirect('/viewBlog')
    return render_template("blogs/self_blog_detail.html", blog_text=blog.blog_text)


@bp.route('/blogDetail/<string:blog_id>/<string:username>/<string:blog_category>', methods=["GET", "POST"])
@login_required
def blog_detail(blog_id, username, blog_category):
    blog = Blog.objects.filter(id=blog_id).first()
    if request.method == 'GET':
        if current_user.id != blog.blog_user_id:
            blog.blog_read_count += 1
            blog.save()

        blog_rating = None
        avg_ratings = list(Comment.objects.aggregate([{'$group': {'_id': '$blog_id', 'avgRating': {'$avg': '$blog_rating'}}}]))
        for rating in avg_ratings:
            if str(list(rating.values())[0]) == blog_id:
                blog_rating = list(rating.values())[1]

        return render_template('blogs/blog_detail.html', blog=blog, rating=blog_rating, author=username, category=blog_category)
    else:
        rate = request.form.get('rating')
        comment = request.form.get('comment')
        blog_id = request.form.get('blog_id')

        old_comment = Comment.objects.filter(blog_id=blog_id).filter(comment_user_id=current_user.id).first()
        today = datetime.datetime.utcnow()

        if old_comment is None:
            blog.blog_rating_count += 1
            blog.save()

            new_comment = Comment(
                blog_id=blog_id,
                comment_user_id=current_user.id,
                blog_comment=comment,
                blog_rating=rate,
                blog_comment_date=today)
            new_comment.save()
        else:
            old_comment.blog_comment = comment
            old_comment.blog_rating = rate
            old_comment.save()
        return redirect('/blogs')
