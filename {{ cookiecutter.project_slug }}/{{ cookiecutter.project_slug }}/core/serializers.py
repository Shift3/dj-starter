from rest_framework import serializers

def serialize_email(email, to):
    email.render()
    return dict(
        to=to,
        cc=email.cc,
        from_email=email.from_email,
        subject=email.subject,
        body=email.body,
        attachments=email.attachments,
        extra_header=email.extra_headers,
        alternatives=email.alternatives,
    )


class NullSerializer(serializers.Serializer):
    pass
