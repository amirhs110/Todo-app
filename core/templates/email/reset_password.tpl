{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reset Your Password
{% endblock %}

{% block html %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset Your Password</title>
</head>
<body>
    <div class="container">
        <h2>Hello {{ user.email }},</h2>
        <p>We received a request to reset your password for your account.</p>
        <p><strong>If you requested this password reset</strong>, click the link below to set a new password:</p>
        <p><a href="{{reset_url}}" class="reset-link">Reset Your Password</a></p>
        <p>If you did not request a password reset, please ignore this email. Your password will remain unchanged.</p>
        <p class="footer">If you have any questions or need help, feel free to contact our support team.</p>
        <p class="footer">Thank you,<br>Your Company Team</p>
    </div>
</body>
</html>
{% endblock %}
