class Patron:
	def __init__(self, name):

		#look up existing patron or initialize new
		self.balance = 0
		self.name = name
		
		
	def deposit(self, amount):
		
		self.balance += amount #self.balance = self.balance + amount

		return self.balance

		

	def withdrawl(self, amount):

		if self.balance - amount < 0:
			return None

		self.balance -= amount

		return self.balance
		

		

	def check_balance(self):

		return self.balance

	def __repr__(self):
		return "Patron: %s, Amount: %d" %(self.name, self.balance)


def findaccount(patrons, name):
	for p in patrons:
		if p.name == name:
			return p
	return None

Ledger = [('nzcek', 30000),
          ('dummy1',30000),
          ('dummy2',30000),
          ('dummy3',30000),
          ('dummy4',30000)]

patrons = []

for entry in Ledger: 
	p = Patron(entry[0])
	p.deposit(entry[1])
	patrons.append(p)

for patron in patrons:
	print("[+] patron: %s balance %d" %(patron.name, patron.check_balance()))
