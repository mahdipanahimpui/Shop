from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    
    # override the create_user()
    def create_user(self, phone_number, email, full_name, password):

    # the field is come by order USERNAME_FIELD, REQUIRED FIELD AND PASSWORD
        self.validate(phone_number, email, full_name, password)

        user = self.model(
            phone_number = phone_number,
            email = self.normalize_email(email), # to validate email field
            full_name = full_name
        )

        user.set_password(password)
        user.save(using=self._db) # using=self._db  IS NOT REQUIRED
        return user
    
    def create_superuser(self, phone_number, email, full_name, password):
        user = self.create_user(
            phone_number = phone_number,
            email = email,
            full_name = full_name,
            password = password
        )

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



    

    def validate(self, phone_number, email, full_name, password):

        # NOTE overwrite by switch/case

        if not phone_number:
            raise ValueError('enter phone number')
        
        if not email:
            raise ValueError('enter email')
        
        if not full_name:
            raise ValueError('enter full name')
        
        if not password:
            raise ValueError('enter password')


    




