## anza
A Django web app.

### Apps
- Users  
- Business  
- Orders  
- Products  

### Users
- Handles user registration, login & logout
- Routes - /signup, /login, /logout
- /<str: username> to get user details
- Uses default auth_views login view

### Business
- Handles business registration, display
- Routes - /create, /update, /delete
- /<int: business_id> to get business details
