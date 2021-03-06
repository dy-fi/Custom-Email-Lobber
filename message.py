from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mimetypes
import codecs
import base64

EMAIL = 'dylanfinn89@gmail.com'
def format_message(name, message_text):
    """
    Creates a message with inserted name

    Returns:
        A formatted string message.
    """
    # prevents side effects
    copy = message_text
    # replace all instances
    formatted = copy.replace("/NAME/", name)
    print('\nformatted copy: ' + formatted)
    return formatted

def create_message(to, subject, message_text):
    """
    Create a message for an email.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = EMAIL
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode() }

def create_message_with_attachment(to, subject, message_text, file):
    """Create a message for an email.

    Args:
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = EMAIL
    message['subject'] = subject

    msg = MIMEText(message_text, 'html')
    message.attach(msg)
    fp = file

    content_type, encoding = mimetypes.guess_type(fp.filename)

    if content_type is None or encoding is not None:
      content_type = 'application/octet-stream'

    fr = fp.read()
    main_type, sub_type = content_type.split('/', 1)

    if main_type == 'text':
      msg = MIMEText(fr.decode(), _subtype=sub_type)
    elif main_type == 'image':
      msg = MIMEImage(fr, _subtype=sub_type)
    elif main_type == 'audio':
      msg = MIMEAudio(fr, _subtype=sub_type)
    else:
      msg = MIMEBase(main_type, sub_type)
      msg.set_payload(fr)


    filename = fp.filename
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode() }

def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
      message = service.users().messages().send(userId=user_id, body=message).execute()
      print('Message Id: %s' % message['id'])
      print('---------------')
      return message
    except Exception as e:
      print ('An error occurred: %s' % e)