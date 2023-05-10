Backend code for android web development class

API
users
-----GET-----
users/logout
response: {'success': True, 'message': 'Logout successful'}

-----POST-----
users/login
request: {'username':'$username', 'password':'$password'}
response: {'success': true|false, 'message': 'Login successful'|'Invalid login credentials'|'Invalid request'|'Method not allowed'}

users/signup
request: {'username':'$username', 'password':'$password'}
response: {'success': true|false, 'message': 'Signup successful'|'Clashing unique fields'|'Invalid request'|'Method not allowed'}