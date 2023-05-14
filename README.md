**Backend code for android web development class**

# API

### GET
>**/get_session**
>```
>response: {
>   'session_id': '$session_id',
>   'session_expiry_date': $session expiry_date'
>}
>```
>**/get_csrf**
>```
>response: {
>   'csrf_token': $csrf_token
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
>   'message': 'logout successful'
>}
>```
><br>

>**/users/reqlogin**
>```
>response: {
>   'username': '$username'
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
>   'message': 'signup successful'|'fields cannot be empty'|'clashing unique fields'|'invalid request'|'method not allowed'
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