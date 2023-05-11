**Backend code for android web development class**

# API
## initiate
---
### GET
>**/initiate**  
>```
>response: {
>   'csrf_token': '$csrf_token'
>}
>```
><br>
---

<br>

## users
---
### GET
>**/users/logout**  
>```
>response: {
>   'success': true,
>   'message': 'Logout successful' 
>}
>```
><br>

<br>

### POST
>**/users/login**  
>```
>request: {
>   'username':'$username',
>   'password':'$password'
>}  
>
>response: {
>   'success': true|false, 
>   'message': 'Login successful'|'Invalid login credentials'|'Invalid request'|'Method not allowed'
>}
>```
><br>

>**/users/signup**  
>```
>request: {
>   'username':'$username',
>   'password':'$password'
>}  
>
>response: {
>   'success': true|false, 
>   'message': 'Signup successful'|'Clashing unique fields'|'Invalid request'|'Method not allowed'
>}
>```
><br>
---

## static
### GET
>**/static/images/***  
>response: $IMAGE

>**/static/videos/***  
>response: $VIDEO