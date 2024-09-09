# Lost Pyramid
This is a very interesting CTF challenge. It's related SSTI(Server Side Template Injection) & JWT Vulnerabilites.

1. Analyze the below source code:
```python
@app.route('/kings_lair', methods=['GET'])
def kings_lair():
    token = request.cookies.get('pyramid')
    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        decoded = jwt.decode(token, PUBLICKEY, algorithms=jwt.algorithms.get_default_algorithms())
        if decoded.get("CURRENT_DATE") == KINGSDAY and decoded.get("ROLE") == "royalty":
            return render_template('kings_lair.html')
        else:
            return jsonify({"error": "Access Denied: King said he does not way to see you today."}), 403
    
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Access has expired"}), 401
    except jwt.InvalidTokenError as e:
        print(e)
        return jsonify({"error": "Invalid Access"}), 401
```
We can see that you need to provide the validated token to get the flag. The token is JWT token, `token = jwt.encode(payload, PRIVATE_KEY, algorithm="EdDSA")`  using EdDSA algorithm to encode the JWT token. The public key & private key are stored in local files.

2. Find the vulnerabilites: 
`decoded = jwt.decode(token, PUBLICKEY, algorithms=jwt.algorithms.get_default_algorithms())`
In the decode code, it doesn't explicitly claim the allowed algorithms to "EdDSA", while using JWT default algorithms. The JWT default algorithms are 'none', 'HS256', 'HS384' & 'HS512'.  We can't use 'none' algorithm, since it need to set the key parameter to None when decoding JWT token. Therefore we can use 'HS256' to produce the JWT token using PUBLICKEY as key.

3. How to obtain PUBLICKEY & KINGSDAY:
We need KINGSDAY to produce the valid payload to obtain the flag. And also need PUBLICKEY to produce the valid JWT token.
```python
{% if name %}
 <h1>Welcome to the Scarab Room:'''+ name + '''!!!</h1>
{% endif %}
```
The above code contains SSTI vulnerabilites. If you set name value to `{{PUBLICKEY}}` ,  `{{KINGSDAY}}`, you could get those value for PUBLICKEY & KINGSDAY. However, you can't set name value to `{{PRIVATE_KEY}}`, because `_` is bypassed by the kings_safelist. However, we will use "HS256" algorithm, the PUBLICKEY is enough. 

4. One note: when you prepare the JWT token using EdDSA public key as key, please use `PyJWT==2.3.0` . Since this vulnerabilites is fixed from `PyJWT>=2.4.0`
