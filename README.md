**Backend code for android web development class**

# API
## initiate
---
### GET
>**/initiate**  
>```
>response: {
    'success': true,
>   'session_id': '$session_id'
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
>   'message': 'logout successful' 
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
>   'message': 'login successful'|'invalid login credentials'|'invalid request'|'method not allowed'
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
>   'message': 'signup successful'|'clashing unique fields'|'invalid request'|'method not allowed'
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