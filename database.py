import json
from storage import getmount

class PasswordDatabase:
	def __init__(self, filename):
		self.filename = filename
		self.data = self.load_data()

	def load_data(self):
		try:
			with open(self.filename, "r") as file:
				data = json.load(file)
		except Exception as e:
			data = {}
		return data

	def save_data(self):
		if getmount("/").readonly:
			return
		with open(self.filename, "w") as file:
			json.dump(self.data, file)

	def add_password(self, website, username, password):
		if website not in self.data:
			self.data[website] = {}
		self.data[website][username] = password
		self.save_data()

	def get_username(self, website, index=0):
		if website in self.data:
			return list(self.data[website].keys())[index]
		return None
 
	def get_password(self, website, username):
		if website in self.data and username in self.data[website]:
			return self.data[website][username]
		return None

	def remove_password(self, website, username):
		if website in self.data and username in self.data[website]:
			del self.data[website][username]
			self.save_data()