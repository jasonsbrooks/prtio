# from main import db
# from sqlalchemy import func
# from sqlalchemy.orm import validates
# import datetime
# from passlib.apps import custom_app_context as pwd_context
# # import sqlalchemy


# class User(db.Model):
#     # __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password_hash = db.Column(db.String(32), index=True)
#     firstname = db.Column(db.String(80))
#     lastname = db.Column(db.String(80))

#     def hash_password(self, password):
#     	self.password_hash = pwd_context.encrpyt(password)

#     def verify_password(self, password):
#     	return pwd_context.verify(password, self.password_hash)

#     # def __init__(self, zoho_contactid, firstname, lastname, tf_login, password, role, *args, **kwargs):
#     #     super(User, self).__init__(tf_login=tf_login, password=password, *args, **kwargs)
#     #     if (password is not None) and (not self.id):
#     #         self.created_asof = datetime.datetime.utcnow()
#     #         # Initialize and encrypt password before first save.
#     #         self.set_and_encrypt_password(password)
#     #     self.zoho_contactid = zoho_contactid  # TODO
#     #     self.firstname = firstname
#     #     self.lastname = lastname
#     #     self.tf_login = tf_login  # TODO -- change to tf_login
#     #     self.role = role

#     def __repr__(self):
#         return '#%d: First Name: %s   Last Name: %s' % (self.id, self.firstname, self.lastname)

#     # def __getstate__(self):
#     #     return {
#     #         'id': self.id,
#     #         'tf_login': self.tf_login,
#     #         'firstname': self.firstname,
#     #         'lastname': self.lastname,
#     #         'role': self.role,
#     #         'created_asof': self.created_asof,
#     #     }

#     # def __eq__(self, o):
#     #     return o.id == self.id

#     # @classmethod
#     # def load_current_user(cls, apply_timeout=True):
#     #     data = get_current_user_data(apply_timeout)
#     #     if not data:
#     #         return None
#     #     return cls.query.filter(cls.email == data['email']).one()


# # class Enrollment(db.Model, AuthUser):
# #     __tablename__ = 'enrollments'
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
# #     user = db.relationship('User', backref='enrollments')
# #     curriculum_version_id = db.Column(db.Integer, db.ForeignKey('curriculum_versions.id'))
# #     curriculumversion = db.relationship('Curriculum_Version', backref='enrollments')
# #     cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'))
# #     cohort = db.relationship('Cohort', backref='enrollments')

# #     def __repr__(self):
# #         return '#%d User ID: %s Version ID: %s, Cohort ID: %s' % (self.id, self.user_id, self.curriculum_version_id, self.cohort_id)


# # class Cohort(db.Model, AuthUser):
# #     __tablename__ = 'cohorts'
# #     id = db.Column(db.Integer, primary_key=True)
# #     start_date = db.Column(db.DateTime)
# #     course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
# #     course = db.relationship('Course', backref='cohorts')

# #     def __repr__(self):
# #         return '#%d Start Date: %s, Course: %s' % (self.id, self.start_date, self.course.course_code)


# # class Curriculum_Version(db.Model, AuthUser):
# #     __tablename__ = 'curriculum_versions'
# #     id = db.Column(db.Integer, primary_key=True)
# #     version_number = db.Column(db.String(6))
# #     date_implemented = db.Column(db.DateTime)
# #     course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
# #     course = db.relationship('Course', backref='curriculum_versions')

# #     def __repr__(self):
# #         return '#%d Version Number: %s, Date Implemented: %s' % (self.id, self.version_number, self.date_implemented)


# # class Course(db.Model, AuthUser):
# #     __tablename__ = 'courses'
# #     id = db.Column(db.Integer, primary_key=True)
# #     course_code = db.Column(db.String(20))
# #     course_name = db.Column(db.String(50))

# #     def __repr__(self):
# #         return '#%d Course Code: %s, Course Name: %s' % (self.id, self.course_code, self.course_name)

# #     def __eq__(self, o):
# #         return o.id == self.id