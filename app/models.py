from . import db, r
from werkzeug.security import generate_password_hash, check_password_hash


#class Base:
    
#    def __repr__(self):
#        return f"{}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    used_passwords = db.relationship("Password", lazy=True)

    profile = db.relationship("Profile", lazy="joined", uselist=False, back_populates="user")  
    
    def set_password(self, password):
        if password in self.used_passwords:
            return False
        _hash = generate_password_hash(password, method="sha256")
        #self.used_passwords.append()
        self.password = _hash
        return True
        
    def verify_password(password):
        return check_password_hash(self.password, password)
    
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    middle_names = db.Column(db.String(40))
    last_name = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(15))
    citizenship = db.Column(db.String(30))
    bvn = db.Column(db.String(11))
    nin = db.Column(db.String(11))
    
    notifications = db.relationship("Notification", backref="profile" lazy="dynamic")
    devices = db.relationship("Device", backref="profile", lazy="select")
    stores = db.relationship("Store", backref="profile", lazy="select")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="profile", uselist=False)
    permissions = db.relationship("Permissions", backref="profile", lazy="joined")

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    buy_crypto = db.Column(db.Boolean, default=False)
    sell_crypto = db.Column(db.Boolean, default=False)
    receive_crypto = db.Column(db.Boolean, default=False)
    fund_crypto_wallet = db.Column(db.Boolean, default=False)
    fund_naira_wallet = db.Column(db.Boolean, default=False)
    withdraw_crypto = db.Column(db.Boolean, default=False)
    withdraw_naira = db.Column(db.Boolean, default=False)
    view_market = db.Column(db.Boolean, default=True)

    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))

class AppleAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user = db.relationship("User", backref="")
    apple_id = db.Column(db.String(80))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))

    profile = db.Column(db.Integer, db.ForeignKey("profile.id"))

class GoogleAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(80))

    profile = db.Column(db.Integer, db.ForeignKey("profile.id"))

#class FacebookAccount(db.Model):
#    id = db.Column(db.Integer, primary_key=True)

class NairaWallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    
class Device(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ip_address = db.Column(db.String(15))
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    items = db.relationship("Item", back_populates="store", lazy="dynamic")
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    price = db.Column(db.Integer)
    store = db.relationship("Store", back_populates="items")
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    
    
    
    
    
    
    
    
    
    
     