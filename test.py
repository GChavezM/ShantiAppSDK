from config import initialize_app
import auth
import util

if __name__ == "__main__":
    print('Start')
    app = initialize_app()
    api_key = app.options.get('apiKey')
    image = util.get_image_base64("image.jpg")
    token = auth.get_token(api_key)
    url = 'http://localhost:5000/shantiapp-4eae1/us-central1/uploadImage'
    data = {
        'image': image,
        'location': 'test'
    }
    result = util.fetch_cloud_functions(token, url, data)
    print(result)
    print('End')
