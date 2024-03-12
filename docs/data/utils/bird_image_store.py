import os
import boto3
import json
import requests
from urllib.parse import quote
from PIL import Image
import io


def get_s3_client():
    session = (
        boto3
        .Session(
            aws_access_key_id=os.environ["FREEBIRD_AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["FREEBIRD_AWS_SECRET_ACCESS_KEY"],
            region_name=os.environ["FREEBIRD_REGION_NAME"]
        )
    )
    s3_client = session.client('s3')
    return s3_client


def load_store():
    BIRD_IMAGE_STORE_PREFIX = os.environ["FREEBIRD_BIRD_IMAGE_STORE_PREFIX"]
    s3_client = get_s3_client()

    response = s3_client.list_objects_v2(
        Bucket=os.environ["FREEBIRD_WWW_BUCKET_NAME"],
        Prefix=BIRD_IMAGE_STORE_PREFIX
    )

    keys_in_bucket = list(map(lambda x: x["Key"], response["Contents"]))

    birds_in_bucket = list(map(lambda x: x.lstrip(f"{BIRD_IMAGE_STORE_PREFIX}/").rstrip(".jpg"), keys_in_bucket))
    return birds_in_bucket


def get_image(sciName):
    search_url = (
        "https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key="
        + os.environ["FREEBIRD_FLICKR_API_KEY"]
        + "&text=\""
        + quote(sciName)
        + "\"&license=2%2C3%2C4%2C5%2C6%2C9&sort=relevance&per_page=1&format=json&nojsoncallback=1"
    )
    search_response = requests.get(search_url)

    image_dict = json.loads(search_response.text)["photos"]["photo"][0]
    image_url = f"https://farm{image_dict['farm']}.static.flickr.com/{image_dict['server']}/{image_dict['id']}_{image_dict['secret']}.jpg"
    image_response = requests.get(image_url)
    return image_response.content


def resize_image(image):
    pil_image = Image.open(io.BytesIO(image))

    width, height = pil_image.size
    square_size = min(height, width)
    crop_direction = 'h' if height > width else 'w'

    if crop_direction == 'h':
        trim = int(0.5 * (height - square_size))
        crop_box = (
            0, # Left
            trim, # Upper
            width, # Right
            height - trim # Lower
        )
    else:
        trim = int(0.5 * (width - square_size))
        crop_box = (
            trim, # Left
            0, # Upper
            width - trim, # Right
            height # Lower
        )

    cropped_pil_image = pil_image.crop(box=crop_box)
    cropped_and_resize_pil_image = cropped_pil_image.resize((120, 120))

    image_buffer = io.BytesIO()
    cropped_and_resize_pil_image.save(image_buffer, format='JPEG')
    image_buffer.seek(0)
    output_image_data = image_buffer.read()
    return output_image_data


def put_image(image, sciName):
    BIRD_IMAGE_STORE_PREFIX = os.environ["FREEBIRD_BIRD_IMAGE_STORE_PREFIX"]
    s3_client = get_s3_client()
    
    s3_client.put_object(
        Bucket=os.environ["FREEBIRD_WWW_BUCKET_NAME"],
        Key=f"{BIRD_IMAGE_STORE_PREFIX}/{sciName}.jpg",
        Body=image
    )

    pass