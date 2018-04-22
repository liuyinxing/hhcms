# PROJECT : hhcms
# TIME : 18-4-17 下午4:25
# AUTHOR : 申延刚 <Younger Shen>
# EMAIL : younger.shen@hotmail.com
# CELL : 13811754531
# WECHAT : 13811754531
from abc import abstractmethod
from django.http.response import JsonResponse, \
    DjangoJSONEncoder, \
    HttpResponsePermanentRedirect, \
    HttpResponseRedirect, \
    HttpResponseGone
from django.urls.base import reverse

from hhcms.apps.config.models import Config as ConfigModel


class RedirectResponse:
    permanent = False
    url = None
    pattern_name = None
    query_string = False

    def get_redirect_url(self, redirect_url, *args, **kwargs):
        if redirect_url:
            url = redirect_url
        elif self.url:
            url = self.url % kwargs
        elif self.pattern_name:
            url = reverse(self.pattern_name, args=args, kwargs=kwargs)
        else:
            return None

        args = self.request.META.get('QUERY_STRING', '')
        if args and self.query_string:
            url = "%s?%s" % (url, args)
        return url

    def redirect(self, url, *args, **kwargs):
        url = self.get_redirect_url(url, *args, **kwargs)
        if url:
            if self.permanent:
                return HttpResponsePermanentRedirect(url)
            else:
                return HttpResponseRedirect(url)
        else:
            return HttpResponseGone()


class Response:
    json_response = JsonResponse
    json_encoder = DjangoJSONEncoder

    def to_json(self, *args, **kwargs):
        return self.json_response(*args, **kwargs, encoder=self.json_encoder)

    def to_template(self, *args, **kwargs):
        return self.render_to_response(*args, **kwargs)

    def to_redirect(self, redirect_url=None, *args, **kwargs):
        url = redirect_url if redirect_url else self.redirect_url
        return self.redirect(url, *args, **kwargs)

    def to_xml(self):
        pass


class Permisson:

    @staticmethod
    def get_permission(request, *args, **kwargs):
        return True, None

    @staticmethod
    def post_permission(request, *args, **kwargs):
        return True, None

    @staticmethod
    def put_permission(request, *args, **kwargs):
        return True, None

    @staticmethod
    def delete_permission(request, *args, **kwargs):
        return True, None


class APIPermission(Permisson):

    def patch_permission(self, request, *args, **kwargs):
        return True, self.to_redirect()

    def head_permission(self, request, *args, **kwargs):
        return True, self.to_redirect()

    def options_permission(self, request, *args, **kwargs):
        return True, self.to_redirect()

    def trace_permission(self, request, *args, **kwargs):
        return True, self.to_redirect()


# riff code here
class Context:

    def get(self, request, *args, **kwargs):
        status, perm_response = self.get_permission(request, *args, **kwargs)
        response = self.get_context(request, *args, **kwargs) if status else perm_response
        return response

    def post(self, request, *args, **kwargs):
        status, perm_response = self.post_permission(request, *args, **kwargs)
        response = self.post_context(request, *args, **kwargs) if status else perm_response
        return response

    def put(self, request, *args, **kwargs):
        status, perm_response = self.put_permission(request, *args, **kwargs)
        response = self.put_context(request, *args, **kwargs) if status else perm_response
        return response

    def delete(self, request, *args, **kwargs):
        status, perm_response = self.delete_permission(request, *args, **kwargs)
        response = self.delete_context(request, *args, **kwargs) if status else perm_response
        return response

    @abstractmethod
    def get_context(self, request, *args, **kwargs):
        pass

    @abstractmethod
    def post_context(self, request, *args, **kwargs):
        pass

    @abstractmethod
    def put_context(self, request, *args, **kwargs):
        pass

    @abstractmethod
    def delete_context(self, request, *args, **kwargs):
        pass


class APIContext(Context):
    def patch(self, request, *args, **kwargs):
        status, perm_response = self.patch_permission(request, *args, **kwargs)
        response = self.patch_context(request, *args, **kwargs) if status else perm_response
        return response

    def head(self, request, *args, **kwargs):
        status, perm_response = self.head_permission(request, *args, **kwargs)
        response = self.head_context(request, *args, **kwargs) if status else perm_response
        return response

    def options(self, request, *args, **kwargs):
        response = self.options_context(request, *args, **kwargs)
        return response

    def trace(self, request, *args, **kwargs):
        status, perm_response = self.trace_permission(request, *args, **kwargs)
        response = self.trace_context(request, *args, **kwargs) if status else perm_response
        return response

    @abstractmethod
    def patch_context(self, request, *args, **kwargs):
        pass

    @abstractmethod
    def head_context(self, request, *args, **kwargs):
        pass

    @abstractmethod
    def options_context(self, request, *args, **kwargs):
        pass

    @abstractmethod
    def trace_context(self, request, *args, **kwargs):
        pass


class Config:
    config_names = ['site_name', 'domain_name', 'theme']

    def get_config(self):
        records = ConfigModel.objects.filter(name__in=self.config_names)
        configs = {}
        for record in records:
            configs.update({record.name: record.value})

        return configs
