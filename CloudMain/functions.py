from CloudMain.models import Account, paper_members
from flask_mail import Message
from CloudMain import mail,url_for

def get_all_members(paper_id):
    # Gathering all members in this paper.
    papers = paper_members.query.all()
    accounts = Account.query.all()
    members_list = []
    for p in papers:
        for a in accounts:
            if int(p.id_paper) == int(paper_id):
                if int(p.id_user) == int(a.id):
                    members_list.append(a)
    return members_list

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@cloudroom.com',recipients=[user.email])
    msg.body = f'''To reset your password, click the link below:
{url_for('reset_password', token=token, _external=True)}
If you didn't make this request ignore this email
'''
    mail.send(msg)