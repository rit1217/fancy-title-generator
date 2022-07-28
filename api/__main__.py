from .api import model


# app.run(use_reloader=True, host='0.0.0.0', port=3000)
for res in model.predict('A', 'lingerie bottoms'):
    print(res)