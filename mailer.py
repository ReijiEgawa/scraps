def send_content_mail(title="test", contents=test_contents):
    smtp_host = 'smtp.gmail.com'  # メールサーバ
    smtp_port = 587  # メールサーバのポート
    from_email = mail_address
    to_email = to_address
    username = from_email
    password = mail_password

    msg = message.EmailMessage()
    asparagus_cid = make_msgid()

    contents_html = ""
    content_base = ""
    with open("./app/template/content.html", "r") as f:
        content_template = f.read()

    for content in contents:
        content_description: str = content['detail']

        if len(content_description) > 100:
            content_description = content_description[:100] + "... 続きは"
        else:
            content_description = content_description + "続きは"

        contents_html += content_template.format(
            title=content['title'],
            image_url=content['thumbnail'],
            description=content_description,
            article_url=content['url']
        )

    layout = ""
    with open("./app/template/layout.html", "r") as f:
        layout = f.read()

    send_content = layout.format(
        article_count=len(contents),
        content=contents_html
    )

    msg.add_alternative(send_content, subtype='html')
    msg['Subject'] = title
    msg['From'] = formataddr(("Yojaニュース", from_email))
    msg['To'] = to_email

    with smtplib.SMTP(smtp_host, smtp_port) as smtpobj:
        smtpobj.starttls()
        smtpobj.login(username, password)
        smtpobj.send_message(msg)
