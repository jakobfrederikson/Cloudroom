from CloudMain.models import Account, paper_members

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