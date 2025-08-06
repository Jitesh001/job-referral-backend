import mimetypes

from django.core.mail import EmailMultiAlternatives


def send_email(  # noqa
    subject="",
    body="",
    from_email=None,
    to=None,
    bcc=None,
    connection=None,
    attachments=None,
    headers=None,
    alternatives=None,
    cc=None,
    reply_to=None,
):
    if bcc is None:
        bcc = []
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to,
        cc=cc,
        bcc=bcc,
        connection=connection,
        headers=headers,
        alternatives=alternatives,
        reply_to=reply_to,
    )

    if attachments and len(attachments):
        for attachment in attachments:
            if hasattr(attachment, "file"):
                file_name = attachment.file.name.split("/")[-1]
                file_content = attachment.file.read()
                mime_type, _ = mimetypes.guess_type(file_name)
            else:
                file_name = attachment.get("name", "attachment")
                file_content = attachment.get("content")
                mime_type = attachment.get("mimetype", "application/octet-stream")

            email.attach(
                file_name, file_content, mime_type or "application/octet-stream"
            )

    email.send(fail_silently=False)
