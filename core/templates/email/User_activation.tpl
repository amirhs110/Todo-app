{% extends "mail_templated/base.tpl" %}

{% block subject %}
User Activation
{% endblock %}


{% block html %}
Hello {{user.email}}</br>
This is an <strong>User Activation</strong> Email.</br>
pls click on this url:
http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{token}}
{% endblock %}