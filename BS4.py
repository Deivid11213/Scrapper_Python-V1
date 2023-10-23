import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin



base_url = 'https://www.neobyte.es'



# # Obtener todos los enlaces de una URL
def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith(('http', 'https')):
            links.append(href)
    
    return links


# Rastrear todas las URL
def crawl_site(base_url):
    visited = set()
    to_visit = set([base_url])

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue

        print(f'Visitando: {url}')
        try:
            download_all_tags(url)
            visited.add(url)
            links = get_all_links(url)
            links = [urljoin(base_url, link) for link in links]
            to_visit.update(links)
        except Exception as e:
            print(f'Error al visitar {url}: {str(e)}')


# Descargar información de etiquetas seleccionadas

def download_all_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    # NOMBRES DE LOS PRODUCTOS
    try:
        product_name_tag = soup.find('span', class_='h3 product-title')

        product_name = product_name_tag.text.strip()

        if product_name:
            product_dir = f'products/{product_name}'
            os.makedirs(product_dir, exist_ok=True)

            with open(f'{product_dir}/{product_name}/name_product.txt', 'w', encoding='utf-8') as file:
                file.write(product_name + '\n')

            print(f'El nombre del producto se ha escrito en el archivo "nombre_producto.txt": {product_name}')
    except:
        print('No se encontró ningún nombre del producto o se ha encontrado un nombre que no corresponde a un producto.\n')


    # PRICES

    try:

        price_tags = soup.find_all('span', class_='product-price')

        
        if price_tags:
            os.makedirs(f'{product_dir}/prices', exist_ok=True)

            with open(f'{product_dir}/prices/prices.txt', 'a') as price_file:
                for price in price_tags:
                    price_text = price.text.strip()

                    price_file.write(f'{price_text}\n')
            
            print('OK, Prices getted')
        else:
            print('No se encontraron precios en la página.\n')
    except:
        print('No se encontraron la clase "product-price".\n')


    #CARACTERÍSTICAS DESTACADAS

    try:
        bullets_text = soup.find(id='bullets_text')

        if bullets_text:
            os.makedirs(f'{product_dir}/features', exist_ok=True)

            with open(f'{product_dir}/features/features.txt', 'w', encoding='utf-8') as file:
                spans = bullets_text.find_all('span')

                for span in spans:
                    contenido = span.get_text(strip=True)
                    if contenido:  # Verificar si el contenido no está vacío
                        file.write(contenido + '\n')

            print('Las características destacadas se han escrito en el archivo "caracteristicas_destacadas.txt".\n')
    except:
        print('No se encontró el contenedor de "bullets_text".\n')


    # DESCRIPTION PRODUCTOS

    try:
        product_description = soup.find_all('span', class_='h3 product-title') # Cambiar clase correcta o id
        

        if product_description:

            product_description = soup.find_all('span')

            os.makedirs(f'{product_dir}/description', exist_ok=True)

            with open(f'{product_dir}/description/descripcion_producto.txt', 'w', encoding='utf-8') as file:
                # Find 'p' & 'li' in 'product-description'
                paragraphs = product_description.find_all(['p', 'li', 'ul', 'span'])

                for paragraph in paragraphs:
                    contenido = paragraph.get_text(strip=True)
                    if contenido:  # Verificar si el contenido no está vacío
                        file.write(contenido + '\n')

            print('El contenido de "product description" se ha escrito en el archivo "descripcion_producto.txt".\n')
    except:
        print('No se encontraron etiquetas p o li o ul o span.\n')


    # CALIFICACIONES Y COMENTARIOS


    try:
        reviews = soup.find_all('h4',class_='testimonial-box')
        

        
        if reviews:
            os.makedirs(f'{product_dir}/ratings', exist_ok=True)

            with open(f'{product_dir}/ratings/ratings.txt', 'w', encoding='utf-8') as file:
                # Find relevant information in each review
                for review in reviews:
                    # Num Stars
                    rating_tags = review.find_all(class_='testimonial-star')
                    num_stars = len(rating_tags)

                    # Name User
                    author_tag = review.find(itemprop='testimonial-name')
                    username = author_tag.text.strip()

                    # Comment if exist
                    comment_tag = review.find(itemprop='testimonial-text')
                    comment = comment_tag.text.strip() if comment_tag else ''

                    # Escribir la información en el archivo
                    file.write(f'Número de estrellas: {num_stars}\n')
                    file.write(f'Título comentario: {username}\n')
                    file.write(f'Comentario: {comment}\n\n')

        print('Las revisiones se han escrito en el archivo "ratings.txt".\n')
    except:
        print('No se encontró el contenedor de "ratings".\n')


    # IMAGEN

    try:
        # Find all 'img' tags
        image_tags = soup.find_all('a', class_='thumbnail product-thumbnail')  # Cambiar clase correcta o id

        if img_class:
            os.makedirs(f'{product_dir}/product_images', exist_ok=True)

            for i, img_tag in enumerate(img_tags):
                img_url = img_tag['src']
                img_data = requests.get(img_url).content

                # Extraer la extensión del archivo de la URL
                img_extension = img_url.split('.')[-1]

                # Generar un nombre de archivo único basado en el índice
                img_name = f'product_image_{i}.{img_extension}'

                with open(f'{product_dir}/product_images/{img_name}', 'wb') as img_file:
                    img_file.write(img_data)

                print(f'OK: Downloaded "{img_name}"')
                
    except:
        print('No se encontraron imágenes en la página.\n')


if __name__ == '__main__':
    os.makedirs('products', exist_ok=True)
    crawl_site(base_url)
    print('Descarga completada.\n')
