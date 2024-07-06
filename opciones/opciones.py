import pygame
import requests

def render_text(surface, text, position, font, color=(255, 255, 255)):
    """
    En esta funcion se encarga, de transformar los texto, en un formato adecuado, y en una posicion (x,y)
    """
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def opcion3 (screen,color):
    """
    acompañada del manejo de teclas, para esta opcion, se encarga de mostrar en pantalla lo que se esta cargando
    """
    render_text(screen.screen,"Ingrese el anio",(10,10),screen.myFont, color)
    render_text(screen.screen,screen.anio,(10,50),screen.myFont, color)
    render_text(screen.screen,"Ingrese la categoria",(10,90),screen.myFont, color)
    render_text(screen.screen,screen.categorias,(10,130),screen.myFont, color)

def manejo_tecla_opcion3(pantalla,teclado,url):
    """
    En esta funcion se utiliza para el manejo la opcion 3, para la carga de los datos
    """
    if pantalla.momento_opcion3 == "anio":
        pantalla.anio = pantalla.manejo_texto(teclado, pantalla.anio)
        if teclado == pygame.K_RETURN:
            pantalla.momento_opcion3 = "categoria"
    else:
        pantalla.categorias = pantalla.manejo_texto(teclado, pantalla.categorias)
        if teclado == pygame.K_RETURN:
            try:
                respuesta = requests.get(f'{url}/Buscar_Premio',headers={"Authorization": f"Bearer {pantalla.token}"}, params={"year":pantalla.anio,"category":pantalla.categorias})
                respuesta.raise_for_status()
                pantalla.premio = respuesta.json()
                pantalla.anio = ""
                pantalla.categorias = ""
                pantalla.etapa = "opcion 3"
            except requests.RequestException as e:
                print("Error")
                pantalla.anio = ""
                pantalla.categorias = ""
                pantalla.momento_opcion3 = "anio"

def BuscarPremio(pantalla,color):
    """
    Se encarga de mostrar el resultado correctos de la opcion 3.
    """
    y_inicial = 10
    for text in pantalla.premio:
        render_text(pantalla.screen, text, (20, y_inicial), pantalla.myFont,color)
        y_inicial += 30

def VerCategorias(pantalla,color: tuple[int,int,int]):
    """
    Se encarga de mostrar la opcion 2.
    Se espera recibir como parametros, el objeto que se encarga de manejar la pantalla, y un color, RGB.
    """
    y_offset = 10
    for categorias in pantalla.categorias:
        render_text(pantalla.screen, categorias, (10, y_offset), pantalla.myFont,color)
        y_offset += 40  # Incrementar el offset para la siguiente línea de texto

def verArchivo(pantalla, color):
    """
    Dibuja el contenido del archivo JSON en pantalla.
    """
    y_offset = 20
    for diccionario in pantalla.archivo_json["prizes"]:
        for key,values in diccionario.items():
            text = f"{key}: {values}"
            render_text(pantalla.screen, text, (20, y_offset), pantalla.myFont,color)
            y_offset += 40  # Incrementar el offset para la siguiente línea de texto

    pygame.display.flip()

def manejo_teclado_opciones(pantalla, teclado):
    """
    Esta funcion se encargar de volver al menu
    """
    if teclado == pygame.K_BACKSPACE:
        pantalla.anio = ""
        pantalla.categorias = ""
        pantalla.etapa = "menu"

def opciones(texto, url, pantalla):
    """
    Dependiendo de la opcion, se encarga de llamar las correspondientes opciones.
    """
    if texto == "1":
        try:
            respuesta = requests.get(f'{url}/Leer_Archivo', headers={"Authorization": f"Bearer {pantalla.token}"})
            respuesta.raise_for_status()
            pantalla.archivo_json = respuesta.json()
            pantalla.etapa = "opcion 1"
            print(pantalla.archivo_json)
        except requests.RequestException as e:
            print("Error al obtener el archivo:", e)
    elif texto == "2":
        try:
            respuesta  = requests.get(f'{url}/Categorias',headers={"Authorization": f"Bearer {pantalla.token}"})
            respuesta.raise_for_status()
            pantalla.categorias = respuesta.json()
            pantalla.etapa = "opcion 2"
            print(pantalla.categorias)
        except requests.RequestException as e:
            print("Error al obtener las categorias:", e)
    elif texto == "3":
        pantalla.etapa = "menu 3"
    elif texto == "4":
        pass
    elif texto == "5":
        pass
    elif texto == "6":
        pass
    elif texto == "7":
        pass