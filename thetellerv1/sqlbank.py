from sqlalchemy import create_engine

engine = create_engine('sqlite:////home/pythonprojects/thetellerv1/bank.db', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from sqlalchemy import Column, Integer, String, Boolean

import random

class Patron(Base):
	__tablename__ = 'patrons'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	balance = Column(Integer)
	discord_id = Column(Integer)

	def __repr__(self):
		return "<Patron(name='%s', discord_id = '%d' balance='%d'>" %(self.name, self.discord_id, self.balance)


class Deathrollentry(Base):
	__tablename__ = 'deathrollentries'

	id = Column(Integer, primary_key=True)
	challenger_id = Column(Integer) 
	challengee_id = Column(Integer)
	accepted = Column(Boolean)
	wager = Column(Integer)
	outcome = Column(String)


	def __repr__(self):
		return "<Deathrollentry(challenger_id='%d', challengee_id='%d',accepted='%d',wager='%d'>" %(self.challenger_id, self.challengee_id, self.accepted, self.wager)

Base.metadata.create_all(engine)



from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


def get_patron(discord_id):
	for patron in session.query(Patron).filter(Patron.discord_id == discord_id): 
		return patron

def patron_exists(discord_id):
	p = None
	for patron in session.query(Patron).filter(Patron.discord_id == discord_id):
		p = patron
	return p

def create_patron(discord_id):
	p = Patron(name='Testsubject',
		          balance=random.randint(1, 1337),
		          discord_id = discord_id)
	p = session.add(p)
	session.commit()
	return session.query(Patron).filter(Patron.discord_id == discord_id)[0]

def check_outstanding(challenger_id, challengee_id):
	entry = session.query(Deathrollentry).filter(Deathrollentry.challenger_id == challenger_id,
		                     Deathrollentry.challengee_id == challengee_id, 
		                     Deathrollentry.accepted      == 0)

	try:
		entry = entry[0]
	except:
		return False

	
	
	entry.accepted = True
	session.add(entry)
	session.commit()
	return entry
	

def create_challenge(challenger_id, challengee_id, wager):
	d = Deathrollentry(challenger_id=challenger_id,\
					   challengee_id=challengee_id,\
					   accepted=False,\
					   wager=wager)
	session.add(d)
	session.commit()

def withdrawl(discord_id, wager):
	p = get_patron(discord_id)
	p.balance -= wager
	session.add(p)
	session.commit()

def deposit(discord_id, wager):
	p = get_patron(discord_id)
	p.balance += wager
	session.add(p)
	session.commit()



"""
def create_dummy():
	Mikey = Patron(name='Mikey', balance=10)
	Hudson = Patron(name='Hudson', balance=25)
	Connor = Patron(name='Connor', balance=140)
	Jonah = Patron(name='Jonah', balance=25)

	session.add_all([Patron(name='Mikey', balance=10),
				 Patron(name='Hudson', balance=25),
 				 Patron(name='Connor', balance=140),
				 Patron(name='Jonah', balance=25),])

	session.commit()
"""

"""
how to gib money

p = get_patron('Connor')
p.balance += 1337
session.add(p)
session.commit()
"""

"""
command examples

[+] Mikey.id
[+] Mikey.name
[+] Mikey.balance

be sure to commit any updates
"""
