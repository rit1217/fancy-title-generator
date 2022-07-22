from .api import model

for res in model.predict('Pom'):
    print(res['title'], res['score'])


# app.run(use_reloader=True, host='0.0.0.0', port=3000)