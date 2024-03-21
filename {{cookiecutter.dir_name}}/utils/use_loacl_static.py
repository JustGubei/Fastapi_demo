import sys


def use_local_static():
    # 覆盖原有方法，使得swagger从本地加载静态资源
    sys.modules["fastapi.applications"].get_swagger_ui_html.__kwdefaults__[
        "swagger_js_url"] = "/static/swagger/swagger-ui-bundle.js"
    sys.modules["fastapi.applications"].get_swagger_ui_html.__kwdefaults__[
        "swagger_css_url"] = "/static/swagger/swagger-ui.css"
    sys.modules["fastapi.applications"].get_swagger_ui_html.__kwdefaults__[
        "swagger_favicon_url"] = "/static/swagger/favicon.jpg"
    sys.modules["fastapi.applications"].get_redoc_html.__kwdefaults__[
        "redoc_js_url"] = "/static/swagger/redoc.standalone.js"
    sys.modules["fastapi.applications"].get_redoc_html.__kwdefaults__[
        "redoc_favicon_url"] = "/static/swagger/favicon.png"
