from django.core.management.base import BaseCommand
from decimal import Decimal
from carrito.models import Product


PRODUCTS = [
    {
        "name": "Camiseta Titular Authentic River Plate 24/25",
        "description": "Camiseta oficial Adidas River Plate 2024/2025.",
        "price": "$89.999",
        "category": "camiseta",
        "brand": "Adidas",
        "stock": 50,
    },
    {
        "name": "Camiseta Titular Argentina 24",
        "description": "Camiseta oficial Adidas Selección Argentina 2024.",
        "price": "$79.999",
        "category": "camiseta",
        "brand": "Adidas",
        "stock": 50,
    },
    {
        "name": "Camiseta Aniversario 50 Años Selección Argentina",
        "description": "Camiseta edición especial Adidas por el 50 aniversario de la Selección Argentina.",
        "price": "$109.999",
        "category": "camiseta",
        "brand": "Adidas",
        "stock": 50,
    },
    {
        "name": "Camiseta Retro Argentina Vintage Calidad Premium #10",
        "description": "Camiseta retro Argentina, calidad premium, número 10. Diseño vintage ideal para coleccionistas y fanáticos.",
        "price": "$99.999",
        "category": "retro",
        "brand": "Retro",
        "stock": 20,
    },
    {
        "name": "Camiseta Titular Boca Juniors 25/26",
        "description": "Camiseta oficial Adidas Boca Juniors 2023/2024, tecnología AEROREADY.",
        "price": "$109.999",
        "category": "camiseta",
        "brand": "Adidas",
        "stock": 40,
    },
    {
        "name": "Camiseta Puma Independiente Titular 24/25 de Hombre",
        "description": "Camiseta oficial Puma Independiente 2023/2024, tela dryCELL.",
        "price": "$69.999",
        "category": "camiseta",
        "brand": "Puma",
        "stock": 30,
    },
    {
        "name": "Botines Adidas Predator League FG",
        "description": "Botines Adidas Predator League para césped natural. Parte superior sintética con textura para mayor control del balón.",
        "price": "$199.999",
        "category": "botines",
        "brand": "Adidas",
        "stock": 25,
    },
    {
        "name": "Botines Nike Mercurial Vapor 16 Elite",
        "description": "Botines Fútbol Nike Mercurial Vapor 16 Elite FG Hombre.",
        "price": "$199.999",
        "category": "botines",
        "brand": "Nike",
        "stock": 25,
    },
    {
        "name": "Botines Puma Future 7 Pro FG/AG",
        "description": "Botines Puma Future 7 Pro para césped natural y sintético. Ajuste adaptable y excelente tracción.",
        "price": "$149.999",
        "category": "botines",
        "brand": "Puma",
        "stock": 30,
    },
    {
        "name": "Botines Adidas F50 Elite - Terreno Firme (Coral)",
        "description": "Botines Adidas F50 Elite para césped natural, diseño ligero y máxima velocidad.",
        "price": "$299.999",
        "category": "botines",
        "brand": "Adidas",
        "stock": 15,
    },
    {
        "name": "Botines Adidas F50 Elite - Terreno Firme (Lila/Verde)",
        "description": "Botines Adidas F50 Elite para césped natural, máxima velocidad, colores vibrantes.",
        "price": "$299.999",
        "category": "botines",
        "brand": "Adidas",
        "stock": 15,
    },
    {
        "name": "Botines Nike Phantom 6 Low Elite (Verde/Negro)",
        "description": "Botines de Pasto Natural Unisex FG Nike Phantom para precisión y control élite.",
        "price": "$399.999",
        "category": "botines",
        "brand": "Nike",
        "stock": 10,
    },
    {
        "name": "Botines Nike Phantom 6 Low Elite (Blanco/Rojo)",
        "description": "Botines de Pasto Natural Unisex FG Nike Phantom para precisión y control élite.",
        "price": "$379.999",
        "category": "botines",
        "brand": "Nike",
        "stock": 10,
    },
    {
        "name": "Camiseta Titular Real Madrid 24/25",
        "description": "Camiseta oficial Adidas Real Madrid temporada 2024/2025.",
        "price": "$109.999",
        "category": "camiseta",
        "brand": "Adidas",
        "stock": 40,
    },
    {
        "name": "Camiseta adidas Suplente River Plate 25/26",
        "description": "Camiseta oficial Adidas Suplente River Plate 2025/2026",
        "price": "$89.999",
        "category": "camiseta",
        "brand": "Adidas",
        "stock": 40,
    },
    {
        "name": "Camiseta adidas Titular River Plate 25/26",
        "description": "Camiseta adidas Titular River Plate 25/26 - BLANCO / ROJO",
        "price": "$119.999",
        "category": "camiseta",
        "brand": "Adidas",
        "stock": 40,
    },
    {
        "name": "Camiseta Retro Boca Juniors 1981",
        "description": "Camiseta retro Boca Juniors 1981, homenaje a la era de Maradona.",
        "price": "$89.999",
        "category": "retro",
        "brand": "Retro",
        "stock": 20,
    },
    {
        "name": "Camiseta Retro AC Milan 1994",
        "description": "Camiseta retro AC Milan 1994, campeón de Europa.",
        "price": "$79.999",
        "category": "retro",
        "brand": "Retro",
        "stock": 20,
    },
    {
        "name": "Camiseta Titular Brasil 2024",
        "description": "Camiseta oficial Nike Brasil 2024, tecnología Dri-FIT.",
        "price": "$79.999",
        "category": "camiseta",
        "brand": "Nike",
        "stock": 35,
    },
    {
        "name": "Camiseta Retro Francia 1998",
        "description": "Camiseta retro Francia 1998, campeón del mundo.",
        "price": "$89.999",
        "category": "camiseta",
        "brand": "Retro",
        "stock": 20,
    },
    {
        "name": "Pelota adidas Fifa Club World Cup Pro 2025",
        "description": "Pelota adidas Fifa Club World Cup Pro 2025.",
        "price": "$19.999",
        "category": "pelota",
        "brand": "Adidas",
        "stock": 60,
    },
    {
        "name": "Pelota adidas Ucl Training - VERDE / BLANCO",
        "description": "Pelota oficial Adidas UEFA Champions League 2023/2024, máxima calidad y rendimiento.",
        "price": "$39.999",
        "category": "pelota",
        "brand": "Adidas",
        "stock": 60,
    },
    {
        "name": "Pelota Premier League Academy",
        "description": "Pelota oficial Nike Flight Premier League 2024, tecnología Aerowsculpt para vuelo preciso.",
        "price": "$29.999",
        "category": "pelota",
        "brand": "Nike",
        "stock": 60,
    },
    {
        "name": "Pelota Nike Ordem Copa América 2024",
        "description": "Pelota oficial Nike Ordem Copa América 2024, diseño exclusivo para el torneo.",
        "price": "$39.999",
        "category": "pelota",
        "brand": "Nike",
        "stock": 60,
    },
    {
        "name": "Pelota Trionda Competition de la Copa Mundial de la FIFA 2026",
        "description": "Pelota oficial Adidas Trionda Competition de la Copa Mundial de la FIFA 2026, diseño de alto rendimiento.",
        "price": "$99.999",
        "category": "pelota",
        "brand": "Adidas",
        "stock": 30,
    },
]


def parse_price(value):
    """Convierte cadenas tipo "$89.999" a Decimal("89999.00")."""
    if value is None:
        return Decimal('0.00')
    s = str(value).strip()
    # eliminar signo $ y puntos de miles
    s = s.replace('$', '').replace('.', '').replace(',', '')
    try:
        return Decimal(s)
    except Exception:
        return Decimal('0.00')


# Mapeo de imágenes por nombre (tomadas del frontend `Home.js`).
IMAGE_MAP = {
    "Camiseta Titular Authentic River Plate 24/25": "https://essential.vtexassets.com/arquivos/ids/1515816-1200-auto?v=638821480754000000&width=1200&height=auto&aspect=true",
    "Camiseta Titular Argentina 24": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/c4c8dee7623f4209b76dfd333a68c812_9366/Camiseta_Titular_Argentina_24_Blanco_IP8400_01_laydown.jpg",
    "Camiseta Aniversario 50 Años Selección Argentina": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/cae76a03cc30414289c3c82a238ad6ed_9366/Camiseta_Aniversario_50_Anos_Seleccion_Argentina_Azul_JF0395_01_laydown.jpg",
    "Camiseta Retro Argentina Vintage Calidad Premium #10": "https://http2.mlstatic.com/D_NQ_NP_2X_642238-MLA84972378273_052025-F.webp",
    "Camiseta Titular Boca Juniors 25/26": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/3d8da5516ef14b4297b562d673589641_9366/Camiseta_Titular_Boca_Juniors_25-26_Azul_JJ4286_01_laydown.jpg",
    "Camiseta Puma Independiente Titular 24/25 de Hombre": "https://www.dexter.com.ar/on/demandware.static/-/Sites-365-dabra-catalog/default/dw77b9ad27/products/PU693681-01/PU693681-01-1.JPG",
    "Botines Adidas Predator League FG": "https://production.cdn.vaypol.com/variants/anwzc7it4acm4w1wnck315nywcih/e82c8d6171dd25bb538f2e7263b5bc7dfc6a79352d85923074be76df53fbc6f4",
    "Botines Nike Mercurial Vapor 16 Elite": "https://www.dexter.com.ar/on/demandware.static/-/Sites-365-dabra-catalog/default/dw4350bb95/products/NIFQ1457-800/NIFQ1457-800-1.JPG",
    "Botines Puma Future 7 Pro FG/AG": "https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa/global/107715/01/sv01/fnd/ARG/w/1000/h/1000/fmt/png/Botines-FUTURE-7-Pro-FG/AG",
    "Botines Adidas F50 Elite - Terreno Firme (Coral)": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/1eb82bc423a3494fb622aa9791fdeed3_9366/Botines_F50_Elite_para_terreno_firme_Naranja_JH7618_HM1.jpg",
    "Botines Adidas F50 Elite - Terreno Firme (Lila/Verde)": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/91f142e473404e57bc06ace8ab1101c5_9366/Botines_F50_Elite_terreno_firme_Violeta_JH7615_HM1.jpg",
    "Botines Nike Phantom 6 Low Elite (Verde/Negro)": "https://nikearprod.vtexassets.com/arquivos/ids/1548257-1200-1200?width=1200&height=1200&aspect=true",
    "Botines Nike Phantom 6 Low Elite (Blanco/Rojo)": "https://nikearprod.vtexassets.com/arquivos/ids/1548306-1200-1200?width=1200&height=1200&aspect=true",
    "Camiseta Titular Real Madrid 24/25": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcRogaCIKvwRzYHX6Hlj3S7I7miNLTwM6c3OMmZBwGaA3aEH1aSwk8gL-q7g2c2D_9xtdFBA-N2OEWbYxfOmLRDBiuQaPb1_-zppyKNhBhsL67eoggu3eIFrj0GM-pUx1VqFgokuHKClpk8&usqp=CAc",
    "Camiseta adidas Suplente River Plate 25/26": "https://sportline.vtexassets.com/arquivos/ids/1605448-1200-auto?v=638853912797670000&width=1200&height=auto&aspect=true",
    "Camiseta adidas Titular River Plate 25/26": "https://production.cdn.vaypol.com/variants/gs29wghpjb9j3lz4apn7aedt2025/e82c8d6171dd25bb538f2e7263b5bc7dfc6a79352d85923074be76df53fbc6f4",
    "Camiseta Retro Boca Juniors 1981": "https://http2.mlstatic.com/D_NQ_NP_2X_709650-MLA76757391603_052024-F.webp",
    "Camiseta Retro AC Milan 1994": "https://http2.mlstatic.com/D_970411-MLA84005601119_042025-C.jpg",
    "Camiseta Titular Brasil 2024": "https://www.ole.com.ar/images/2023/12/28/sHplKNs1ai_720x0__1.jpg",
    "Camiseta Retro Francia 1998": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuxtahL8ESkvUkT6__9hS3FQg3xLaoC-_DBA&s",
    "Pelota adidas Fifa Club World Cup Pro 2025": "https://www.dexter.com.ar/on/demandware.static/-/Sites-365-dabra-catalog/default/dwae33f67e/products/ADJE8770/ADJE8770-1.JPG",
    "Pelota adidas Ucl Training - VERDE / BLANCO": "https://production.cdn.vaypol.com/variants/3zn4ommy34tdjj7s0qnjts2n9xqw/e82c8d6171dd25bb538f2e7263b5bc7dfc6a79352d85923074be76df53fbc6f4",
    "Pelota Premier League Academy": "https://nikearprod.vtexassets.com/arquivos/ids/1066925-1200-1200?width=1200&height=1200&aspect=true",
    "Pelota Nike Ordem Copa América 2024": "https://acdn-us.mitiendanube.com/stores/003/924/927/products/pelota-copa-americaa-ac8eefef652195eb1c17171891252189-480-0.jpg",
    "Pelota Trionda Competition de la Copa Mundial de la FIFA 2026": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/3a5965320eeb418bb674cc98e81c7f6a_9366/Pelota_Trionda_Competition_de_la_Copa_Mundial_de_la_FIFA_2026tm_Blanco_JD8031_01_00_standard.jpg",
}


class Command(BaseCommand):
    help = 'Seed inicial de productos desde lista embebida (usa Home.js como origen)'

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for p in PRODUCTS:
            name = p.get('name')
            description = p.get('description', '')
            price = parse_price(p.get('price'))
            category = p.get('category', '')
            brand = p.get('brand', '')
            stock = p.get('stock', 10)

            obj, was_created = Product.objects.update_or_create(
                name=name,
                defaults={
                    'description': description,
                    'price': price,
                    'category': category,
                    'brand': brand,
                    'stock': stock,
                    'image': IMAGE_MAP.get(name, ''),
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'Seed completo. Productos creados: {created}, actualizados: {updated}'))
