{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activate Your Account
{% endblock %}

{% block html %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Activate Your Account</title>
</head>
<body>
    <div class="container">
        <h2>Hello {{ user.email }},</h2>
        <p>Welcome to our platform! We're excited to have you on board.</p>
        <p><strong>Please activate your account</strong> by clicking the link below:</p>
        <p><a href="http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{ token }}" class="activation-link">Activate Your Account</a></p>
        <p>If you did not create an account with us, please ignore this email.</p>
        <p class="footer">If you have any questions or need help, feel free to contact our support team.</p>
        <p class="footer">Thank you,<br>Your Company Team</p>
    </div>
</body>
</html>
{% endblock %}
