
exclude = ['San', 'Mateo', 'County', 'Health', 'About', 'Us', 'Contact', 'Careers',
           'Español', 'Public', 'Notice', 'for', 'Daly', 'City', 'Patients', 'Find']

include = ['San Mateo County Health', 'About Us', 'Contact', 'Careers', 'Español',
           'Public Notice for Daly City Patients', 'Find a Doctor', 'Caroline A Bowker, MD',
           'Carol A. Boyd, DDS', 'Vanessa Breen, NP', 'Rosa E Brody, MD', 
           'Daniel J. Buckley, MD', 'Tho Bui, DDS', 'Janet Chaikind, MD', 'Kara Chang, DDS',
           'Crystal I Chen, OD', 'Grace Chen, MD', 'Follow us on Facebook', 
           'Follow us on Twitter', 'About', 'Careers', 'Contact', 'Directory', 
           'Patient Privacy', 'RFPs', 'San Mateo County Health', 'Health Plan of San Mateo',
           'Network of Care', 'Get Healthy SMC', 'Hospital Consortium of SMC']

#filtered = [word for word in include if '' not in exclude]
#print(filtered)
for word in include:
    if word.lower() not in ' '.join(exclude).lower():
        print(word)
    #break
