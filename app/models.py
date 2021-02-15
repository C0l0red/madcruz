from . import db, r, mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


#class Base:
    
#    def __repr__(self):
#        return f"{}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    used_passwords = db.relationship("Password",backref="user", lazy=True)

    profile = db.relationship("Profile", lazy="joined", uselist=False, back_populates="user") 

    def __init__(self, **kwargs):
        password = kwargs["password"]
        self.set_password(password)
        self.profile = Profile()

        remainder = {key:val for key,val in kwargs.items() if key != "password"}
        super().__init__(**remainder)
    
    def set_password(self, password):
        # if password in self.used_passwords:
        #     return False
        for entry in self.used_passwords:
            if entry.verify_password(password):
                return False

        _hash = generate_password_hash(password, method="sha256")
        #self.used_passwords.append()
        self.password = _hash

        new_password = Password(password=self.password)
        self.used_passwords.append(new_password)
        return True

    def send_email(self, subject, body):
        msg = Message(subject, body)
        mail.send(msg)

        return True

    @classmethod
    def send_bulk_email(cls, subject, body, recipients):

        return True
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.email}>"
    
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
    
    notifications = db.relationship("Notification", backref="profile", lazy="dynamic")
    devices = db.relationship("Device", backref="profile", lazy="select")
    stores = db.relationship("Store", backref="profile", lazy="select")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="profile", uselist=False)
    permissions = db.relationship("Permissions", backref="profile", uselist=False, lazy="joined")

    naira_wallet = db.relationship("NairaWallet", backref="profile", uselist=False, lazy="joined")
    apple_account = db.relationship("AppleAccount", backref="profile", uselist=False, lazy="select")
    google_account = db.relationship("GoogleAccount", backref="profile", uselist=False, lazy="select")

    is_verified_email = db.Column(db.Boolean, default=False)
    is_verified_phone = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        self.permissions = Permissions()

        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Profile User {self.user.email}>"

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<Password {self.date} User {self.user.email}>"

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

    def __repr__(self):
        return f"<Permissions User {self.profile.user.email}>"

class AppleAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user = db.relationship("User", backref="")
    apple_id = db.Column(db.String(80))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))

    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))

    def __repr__(self):
        return f"<AppleAccount User {self.profile.user.email}>"

class GoogleAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(80))

    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))

    def __repr__(self):
        return f"<GoogleAccount User {self.profile.user.email}>"

#class FacebookAccount(db.Model):
#    id = db.Column(db.Integer, primary_key=True)

class NairaWallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))

    def __repr__(self):
        return f"<NairaWallet User {self.profile.user.email}>"
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    viewed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Notification {self.id} User {self.profile.user.email}>"
    
class Device(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ip_address = db.Column(db.String(15))
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))

    def __repr__(self):
        return f"<Device {self.name} User {self.profile.user.email}>"

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    items = db.relationship("Item", back_populates="store", lazy="dynamic")
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))

    def __repr__(self):
        return f"<Store {self.name} User {self.profile.user.email}>"
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    price = db.Column(db.Integer)
    store = db.relationship("Store", back_populates="items")
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    # profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))

    def __repr__(self):
        return f"<Item {self.name} User {self.store.profile.user.email}>"
    
    
    
    
    
    
    
    
    
    
     