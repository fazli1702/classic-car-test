from bs4 import BeautifulSoup
from lxml import etree
import requests
import json
import os

def get_all_text(xpath_element):
    text_fragments = xpath_element[0].xpath('.//text()')
    
    # Join them together into one string
    full_text = "".join(text_fragments)
    print(full_text.strip())

def download_images(links_file, output_dir="images", start_folder=1):
    with open(links_file, "r") as f:
        content = f.read()

    groups = [
        [line.strip() for line in group.strip().splitlines() if line.strip()]
        for group in content.split("\n\n")
        if group.strip()
    ]

    for group_idx, urls in enumerate(groups, start=start_folder):
        group_dir = os.path.join(output_dir, str(group_idx))
        os.makedirs(group_dir, exist_ok=True)
        for img_idx, url in enumerate(urls, start=1):
            response = requests.get(url)
            if response.status_code == 200:
                filepath = os.path.join(group_dir, f"{img_idx}.jpg")
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"Saved {filepath}")
            else:
                print(f"Failed to download {url}. Status code: {response.status_code}")


def scrape_vehicle_img(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")
    return [img["src"] for img in img_tags if img.get("src")]

def scrape_vehicle_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    dom = etree.HTML(str(soup))

    name = dom.xpath('//*[@id="comp-ma9poniq3"]/h1/span/span')[0].text
    make = dom.xpath('//*[@id="comp-ma9poniu1"]/p/span/span')[0].text
    model = dom.xpath('//*[@id="comp-ma9qblpc"]/p/span/span')[0].text
    year = dom.xpath('//*[@id="comp-ma9qc7ai"]/p/span/span')[0].text
    price = dom.xpath('//*[@id="comp-ma9ponj0"]/p/span/span/span/span/span')[0].text
    location = dom.xpath('//*[@id="comp-mbzqioh1"]/p/span/span')[0].text
    contact = dom.xpath('//*[@id="comp-mbzqfrve"]/p/span/span')[0].text

    exterior_color = dom.xpath('//*[@id="comp-ma9qc6zn"]/p/span/span')[0].text
    interior_color = dom.xpath('//*[@id="comp-mbzq8f5x"]/p/span/span')[0].text
    licensing_scheme = dom.xpath('//*[@id="comp-mbzqcn49"]/p/span/span')[0].text

    transmission = dom.xpath('//*[@id="comp-mc12b730"]/p/span/span')[0].text
    body_type = dom.xpath('//*[@id="comp-mc12j4m3"]/p/span/span')[0].text
    air_conditioning = dom.xpath('//*[@id="comp-mc12rrnv"]/p/span/span')[0].text
    doors = dom.xpath('//*[@id="comp-mc12puqa"]/p/span/span')[0].text

    details = dom.xpath('//*[@id="comp-mc12efuy"]/p/span/span')[0].text
    restoration = dom.xpath('//*[@id="comp-mc12hb3d"]/p/span/span')[0].text

    vehicle_data = {
        "name": name,
        "make": make,
        "model": model,
        "year": year,
        "price": price,
        "location": location,
        "contact": contact,
        "exterior_color": exterior_color,
        "interior_color": interior_color,
        "licensing_scheme": licensing_scheme,
        "transmission": transmission,
        "body_type": body_type,
        "air_conditioning": air_conditioning,
        "doors": doors,
        "details": details,
        "restoration": restoration,
    }

    return vehicle_data


def scrape_toy_car_details(links_file, output_file):
    name_xpath = '//*[@id="fullscreen-view"]/div[3]/div/div/div[1]/h1'
    detail_xpath = '//*[@id="fullscreen-view"]/div[3]/div/div/div[2]/div'

    with open(links_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    toy_cars = []
    for url in urls:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        dom = etree.HTML(str(soup))

        name_elements = dom.xpath(name_xpath)
        detail_elements = dom.xpath(detail_xpath)

        name = "".join(name_elements[0].xpath('.//text()')).strip() if name_elements else ""
        detail = "".join(detail_elements[0].xpath('.//text()')).strip() if detail_elements else ""

        toy_cars.append({"name": name, "detail": detail})
        print(f"Scraped: {name}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(toy_cars, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(toy_cars)} toy cars to {output_file}")
    return toy_cars

def scrape_toy_car_images(links_file):
    
    with open(links_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    all_images = []
    for url in urls:
        imgs = scrape_vehicle_img(url)
        product_imgs = [
            src for src in imgs
            if "f85466_" in src
            and "Logo" not in src
            and src.endswith((".jpg", ".png"))
        ]
        if product_imgs:
            all_images.append(product_imgs)
            print(f"Found {len(product_imgs)} images from {url}")
        else:
            print(f"No product images found from {url}")

    return all_images


def main():
    # urls = [
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/1965-jaguar-e-type-4.2-litre",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/austin-healey-3000-mark-iii",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/marcos--gt",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/1973-volkswagen-beetle-1303-s",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/1973-bmw-e3-3.0",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/1975-mg-midget-1500",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/corvette--stingray",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/1977-ford-capri-mk2",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/1980-datsun--280zx",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/1981-mercedes-benz-200",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/1982-range--rover-",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/jaguar-xjs",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/1984-bmw-635csi",
    #     "https://www.classiccarsingapore.com/cars-dynamic-collection/lotus-esprit",
    # ]
    
    scrape_toy_car_details('scraper/toy_links.txt', 'toy_car_details.json')

    # download_images('scraper/img_links.txt', 'images', start_folder=2)
    # all_images = scrape_toy_car_images('scraper/toy_links.txt')

    # output_dir = 'toy_images'
    # for group_idx, imgs in enumerate(all_images, start=1):
    #     group_dir = os.path.join(output_dir, str(group_idx))
    #     os.makedirs(group_dir, exist_ok=True)
    #     for img_idx, url in enumerate(imgs, start=1):
    #         response = requests.get(url)
    #         if response.status_code == 200:
    #             filepath = os.path.join(group_dir, f"{img_idx}.jpg")
    #             with open(filepath, "wb") as f:
    #                 f.write(response.content)
    #             print(f"Saved {filepath}")
    #         else:
    #             print(f"Failed to download {url}. Status code: {response.status_code}")

    # vehicle_data = []
    # vehicle_imgs = []
    # for url in urls:
    #     data = scrape_vehicle_data(url)
    #     vehicle_data.append(data)

    #     imgs = scrape_vehicle_img(url)
    #     print(imgs)

    # with open("data.json", "w") as file:
    #     json.dump(vehicle_data, file, indent=4)

if __name__ == "__main__":
    main()