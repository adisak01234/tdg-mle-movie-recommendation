from app import create_app


app = create_app()
app.config['TESTING'] = True
client = app.test_client()

response = client.get('/recommendations?user_id=18')
print(response.json)

response = client.get('/recommendations?user_id=18&returnMetadata=true')
print(response.json)
