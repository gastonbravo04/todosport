# programacion-1
proyecto final
# 🏋️‍♂️ Todosport - Backend

**Todosport** es un sistema backend desarrollado en Django para una tienda eCommerce especializada en la venta de ropa y artículos deportivos. Este proyecto proporciona una API RESTful que permite la gestión de productos, clientes, pedidos y carritos de compras.

## Tecnologías utilizadas

* Python 3.x
* Django 5.1.7
* MySQL / MariaDB
* Django REST Framework (si está en uso)
* Matplotlib y OpenCV (si se usan para análisis o procesamiento)

## Estructura del proyecto

* `manage.py`: Script principal para tareas administrativas de Django.
* `django_api/`: Carpeta raíz de configuración del proyecto Django.
* `app/`: Carpeta esperada para las aplicaciones (productos, usuarios, pedidos, etc).
* `.gitignore`, `.gitattributes`: Archivos de control de Git.
* `requirements.txt`: Lista de dependencias necesarias.

## Modelos principales

### `User`

Modelo base del sistema. Puede ser administrador, cliente u otro rol. Se encarga del manejo de autenticación y permisos.

### `Supplier`

Representa a los proveedores que ofrecen los productos. Contiene información como nombre, contacto, y dirección.

### `Product`

Contiene los productos que se venden en la tienda. Cada producto tiene nombre, descripción, precio, stock y un proveedor asociado.

### `Customer`

Representa a los clientes registrados en la plataforma. Incluye datos personales, dirección de envío, historial de compras, etc.

### `Order`

Registro de pedidos realizados por los clientes. Incluye productos comprados, fecha, estado del pedido, y total.

### `Cart`

Carrito de compras. Almacena los productos seleccionados por el usuario antes de confirmar la compra. Puede estar vinculado a un `Customer`.

## Endpoints (si usás DRF)

Documentalos usando herramientas como Postman, Swagger o ReDoc. Ejemplos esperados:

* `GET /api/products/`
* `POST /api/orders/`
* `GET /api/cart/`

## Funcionalidades clave

* Gestión de productos deportivos y prendas de vestir
* Registro y autenticación de usuarios
* Carrito de compras y procesamiento de pedidos
* Gestión de proveedores
* Integración con base de datos relacional

## To-Do

* [ ] Documentar todos los endpoints
* [ ] Implementar autenticación JWT o Token
* [ ] Crear pruebas unitarias
* [ ] Integrar Swagger para documentación

Autor: Gaston Bravo
Universidad de mendoza


