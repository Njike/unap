from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



# create a users table
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False) 
    is_staff = db.Column(db.Boolean, nullable=False)
    is_client = db.Column(db.Boolean, nullable=False)
    client = db.relationship("Client", backref="user", lazy=True)
    staff = db.relationship("Staff", backref="user", lazy=True)
    super_user = db.Column(db.Boolean)
    # password is to be restricted to only staffs
    # def __str__(self):
    #     return self.first_name


    

class Portfolio(db.Model):
    __tablename__ = "portfolio"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    details = db.Column(db.Text, nullable=True)
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(30), nullable=True)
    # portfolio id
    # category id : foreign key
    # client {hopes to be a different table}
    # location 
    # date which the job was conducted
    # project details : text,  title


class PortfolioCategory(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    portfolio = db.relationship("Portfolio", backref="portfolioType", lazy=True) 

    def __str__(self):
        return f"{self.name.capitalize()}"
    

class Testimonial(db.Model):
    __tablename__ = "testimonials"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)

class Client(db.Model):
    __tablename__ = "clients"
    is_private = db.Column(db.Boolean, nullable=False)
    is_cooperate = db.Column(db.Boolean, nullable=False)
    portfolio = db.relationship("Portfolio", backref="client", lazy=True)
    private = db.relationship("Private", backref="client", lazy=True)
    company = db.relationship("Company", backref="client", lazy=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id")) # null entry implies that the client belongs to the company

    def __str__(self):
        return f"{self.user.last_name.capitalize()} {self.user.first_name.capitalize()}"
    


class Staff(db.Model):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #one to one relationship
    testimonial = db.relationship("Testimonial", backref="author", lazy=True)
    def __str__(self):
        return f"{self.user.last_name.capitalize()} {self.user.first_name.capitalize()}"
    
    
class Private(db.Model):
    __tablename__ = "private"
    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    def __str__(self):
       return f"{self.client.user.last_name.capitalize()} {self.client.user.first_name.capitalize()}"
    

    
class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(20), nullable=False)
    staff = db.Column(db.Integer, db.ForeignKey("clients.id")) ## one to one relationship
    

    def __str__(self):
        return self.company_name