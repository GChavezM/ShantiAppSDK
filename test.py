from config import initialize_app
import auth
import util

if __name__ == "__main__":
    print('Start')
    app = initialize_app()
    api_key = app.options.get('apiKey')
    image = util.get_image_base64("image.jpg")
    token = auth.get_token(api_key)
    url = 'https://us-central1-shantiapp-4eae1.cloudfunctions.net/uploadImage'
    data = {
        'image': image,
        'location': 'test'
    }
    result = util.fetch_cloud_functions(token, url, data, fetch_type='get')
    print(result)
    print(result.get('imagePath'))
    print('End')
