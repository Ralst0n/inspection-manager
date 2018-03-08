teams = [
        {'p': 'TRC', 's': ['Prudent', 'RIG', 'Navarro']}, 
        {'p': 'Pennoni', 's': ['sub1', 'sub2', 'sub3']}
    ]

for dictionary in teams:
    for p, s in dictionary.items():
        print(s)
        for sub in s:
            print(f"")



for dictionary in teams:
    for sub in dictionary['s']:
        print(f"{dictionary['p']} teamed with {sub}")


for team in teams:
    print(f"{team['p']} is the prime")
    for sub in team['s']:
        print(f"{sub} is a sub")



def sub_wins_teams(sub_name, district):
    '''
    count of teams with this firm as sub
    ProjectTeam.objects.all().filter(sub=BusinessPartner.objects.get(name="Prudent Engineering LLP")).count()
    
    receive a sub name return the number of wins that sub had,
    the percentage of the total that number is,
    and the percentage of teams that sub was on
    '''
    ProjectTeam.objects.filter(agreement_number__winner=prime).filter(agreement_number__district=district).filter(sub='RIG Consulting, Inc.').count()

    ProjectTeam.objects.filter(sub=BusinessPartner.objects.get(name='Pennoni Associates Incorporated')).count()



# COUNT OF WINS BY PRIME NAME
LetProject.objects.all().filter(winner=BusinessPartner.objects.get(name="Construction Methods and Coordination, Inc., dba CMC Engineering")).count()

def dba(name):
    '''make it easier to return the queryset based onwinner name rather than having to dig for it each time'''
    return BusinessPartner.objects.get(name=name)

def pnum(agreement_number):
    '''dba for projects'''
    return LetProject.objects.get(agreement_number=agreement_number)

def sub_wins_by_district(sub_name, district):
    ''' far more complex than i imagined '''
    sub_win_count = 0   
    # First figure out who won the projects in that district and save their name and the agreement_number
    winning_primes = []
    for proj in LetProject.objects.filter(district=district):
        winning_primes.append([proj.winner, proj.agreement_number])
    # Add up the totals for each combo that also includes the sub in question
    for combo in winning_primes:
        try:
            sub_win_count += ProjectTeam.objects.filter(agreement_number=pnum(combo[1])).filter(prime=dba(combo[0])).filter(sub=dba(sub_name)).count()
        except:
            sub_win_count += 0
    return sub_win_count


def sub_teams_by_district(sub_name, district):
    return ProjectTeam.objects.filter(sub=dba(sub_name)).filter(agreement_number__district=district).count()

def prime_mates(prime_name, district):
    '''Who does a prime team with most'''
    mates = {}
    for pairing in ProjectTeam.objects.filter(prime=dba(prime_name)).filter(agreement_number__district=district):
        if str(pairing.sub) in mates:
            mates[str(pairing.sub)] += 1
        else:
            mates[str(pairing.sub)] = 1
    return mates



def tried_for_project(business_partner, project):
    '''Did the business partner try for this project'''
    if pnum(project).projectteam_set.filter(sub=dba(business_partner)).count() > 0:
        return True
    return False


def tried_for_prime(business_partner, project):
    '''Did the business partner try for this project'''
    if pnum(project).projectteam_set.filter(prime=dba(business_partner)).count() > 0:
        return True
    return False

def prime_proposal_count(bp, district):
    count = 0
    for agreement_number in LetProject.objects.filter(district=district):
        if tried_for_prime(bp, agreement_number):
            count += 1
    return count

def jobs_applied_by_district(bp, district):
    count = 0
    for agreement_number in LetProject.objects.filter(district=district):
        if tried_for_project(bp, agreement_number):
            count += 1
    return count

def primes_by_wins(district):
    ''' List out prime wins by district. Filter for just the partners that win, then count the wins of those partners in the district
        return a dict with each winners total wins'''
    partner_wins = {}
    partners = []
    for project in LetProject.objects.filter(district=district):
        partners.append(project.winner)
    for partner in partners:
        bp_wins = LetProject.objects.all().filter(district=district).filter(winner=partner).count()
        partner_wins[partner.name] = bp_wins
    return partner_wins


def partner_placements(partner, district):
    '''Get the first seconds and thirds of a partner in a given district'''
    first_place = LetProject.objects.all().filter(district=district).filter(winner=dba(partner)).count()
    second_place = LetProject.objects.all().filter(district=district).filter(second_place=dba(partner)).count()
    third_place = LetProject.objects.all().filter(district=district).filter(third_place=dba(partner)).count()
    return {
        'wins': first_place,
        '2nds': second_place,
        '3rds': third_place
    }

def district_subs(district):
    '''Return a dictionary of the subs in a district and how many contracts they've won'''
    sub_list = {}
    for sub in BusinessPartner.objects.all():
        wins = sub_wins(sub.name, district)
        if wins > 0:
            sub_list[sub.name] = wins
    return sub_list





    district revenue

   zed = list(Invoice.objects.filter(end_date__year=datetime(2017,3,4).year).filter(project__office="King of Prussia").aggregate('total_cost').values())