from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from blogs.forms import PostForm
from blogs.models import Post


def posts_list(request):
    """
    Lista los post publicados por fecha de publicación de forma descendente
    :param request: HttpRequest
    :return: HttResponse
    """
    #posts = Post.objects.select_related().all().order_by('-publish_at')
    posts = Post.objects.select_related().exclude(publish_at__isnull=True).order_by('-publish_at')

    context = {
        'post_objects': posts
    }
    return render(request, 'blogs/posts_list.html', context)

def blogs_list(request):
    """
    Lista los blogs de los usuarios
    :param request: HttpRequest
    :return: HttpResponse
    """
    blogs = User.objects.all().values("username").order_by('username')
    context = {
        'blog_objects': blogs
    }
    return render(request, 'blogs/blogs_list.html', context)

def user_posts_list(request, username):
    """
    Lista TODOS los post del blog de un usuario de forma descendente
    :param request: HttpRequest
    :param username: Nombre de usuario
    :return: HttpResponse
    """
    user = User.objects.filter(username=username)
    posts = Post.objects.select_related('owner').filter(owner=user).order_by('-created_at')

    context = {
        'post_objects': posts
    }
    return render(request, 'blogs/posts_list.html', context)

def user_post_detail(request, username, post_pk):
    """
    Obtiene el detalle de un post del usuario
    :param request: HttpRequest
    :param username: Nombre de usuario
    :param post_pk: Identificador del post
    :return: HttpResponse
    """
    user = User.objects.filter(username=username)
    post = Post.objects.select_related('owner').filter(owner=user).get(pk=post_pk)

    context = {
        'post_detail': post
    }
    return render(request, 'blogs/post_detail.html', context)


class NewPostView(View):

    @method_decorator(login_required)
    def get(self, request):
        """
        Muestra el formulario para publicar un nuevo post
        :param request: HttpRequest
        :return: HttpResponse
        """
        form = PostForm()
        context = {
            'form': form
        }
        return render(request, 'blogs/new_post.html', context)

    @method_decorator(login_required)
    def post(self, request):
        """
        Publicar el post
        :param request: HttpRequest
        :return: HttpResponse
        """
        # Crear el post con los datos del POST
        post = Post(owner=request.user)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post.save()

            for genre in form.cleaned_data["genres"]:
                post.genres.add(genre)

            form = PostForm()
            message = 'Publicado'
        else:
            message = 'No se ha publicado'

        context = {
            "form": form,
            "message": message
        }
        return render(request, 'blogs/new_post.html', context)
