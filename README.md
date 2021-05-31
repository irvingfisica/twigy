# Twigy 

Twigy es un módulo de python que permite hacer peticiones a la API de Twitter de forma muy eficiente. Por ahora es un módulo interno para uso exclusivo de MORLAN.

Twigy está configurado de tal manera que en las peticiones que realiza a la API de Twitter se obtenga la mayor cantidad de información posible relacionada con la petición. Los valores por defecto de Twiggy siempre son los valores máximos que uno puede utilizar en las peticiones a la API de Twitter. Por ejemplo, Twitter permite obtener 100 tweets en una petición pero el valor por default es de 10, Twigy modifica este valor po default y lo coloca en 100.

Para usar Twigy es necesario contar con un token aprobado por Twitter para hacer peticiones a su API. El token se puede obtener aplicando como developer en la plataforma de Twitter.

Twigy ocupa la versión 2.0 de la API de Twitter, la cual aún está en desarrollo. Debido a esto, algunas de las funciones que se definen en Twigy podrían quedar obsoletas.

El principal objeto en Twigy es el Requester. Este objeto es el encargado de realizar todas las peticiones. Para poder hacer peticiones es necesario crear una instancia de este objeto. Al crear la instancia es necesario nuestro Bearer Token.

```python
    from twigy import Requester

    token = 'AQUÍ_VA_EL_TOKEN'
    tw_req = Requester(token)
```

El objeto Requester se encargará de realizar las peticiones. Todas las peticiones que realiza las regresa como peticiones en crudo. Depende del usuario como procesarlas. El módulo ofrece algunas funciones extra para procesarlas. El fomrato de estas respuestas es el mismo formato que se obtiene al hacer peticiones con la librería 'requests'

Cuando el Requester realiza una petición y el resultado es un código '503' correspondiente a 'Service unavailable' por default la petición se repite una vez.

Si el código resultante de la petición es un código diferente a 200 se emite un warning informandolo. Este warning no detiene la ejecución del programa.

## Peticiones básicas a la API de Twitter
En esta sección se describen las funciones básicas de Twigy, estas funciones se corresponden con la mayoría de los endpoints en la API de Twitter, proporcionan una manera simple y eficiente de acceder a ellos. 

Como se mencionó anteriormente, las respuestas obtenidas a través de las peticiones son respuestas completas y crudas desde la API. La API de twitter limita el número de tweets y de usuarios obtenidos en una petición, sin embargo permite paginar y obtener más elementos en peticiones posteriores encadenadas. 

Si se quiere paginar a mano en la respuesta de la petición se encuentra el token de paginación necesario para realizar una nueva petición. Usualmente este token se encuentra en el objeto 'meta' de la respuesta.

No es necesario paginar a mano, Twigy proporciona funciones para llevar a cabo esta paginación de peticiones de forma automática.

### Petición de información de usuarios
La API de twitter tiene 2 endpoints actualmente para solicitar información acerca de la cuenta de un usuario.

- Petición usando el user_id
- Petición usando el username

Además estos dos endpoints tienen versiones para realizar peticiones de información de varios usuarios al mismo tiempo. Estos 4 endpoints están disponibles en Twigy.

Para pedir información de un usario usando su user_id Twigy proporciona la función:

```python
    respuesta = tw_req.user(user_id)
```

y para pedir información de un usuario usando el username Twigy proporcional la función:

```python
    respuesta = tw_req.user_by_uname(username)
```

Para pedir info de varios usuarios las funciones son:

```python
    respuesta = tw_req.users(ids)
    respuesta = tw_req.users_by_uname(unames)
```

donde `ids` y `unames` son listas de ids y de nombres de usuarios con un máximo de 100 elementos.

### Petición de información de tweets

Para realizar una petición de información correspondiente a un tweet o a un conjunto de tweets Twigy proporciona las siguientes funciones.

Para un tweet:
```python
    respuesta = tw_req.tweet(tweet_id)
```

Para un conjunto de tweets (máximo 100):
```python
    respuesta = tw_req.tweets(tweet_ids)
```

### Peticiones de timelines
Twigy tiene la capacidad de realizar peticiones de los últimos tweets emitidos por un usuario. La función con la cual se realiza esta petición es la siguiente:

```python
    respuesta = tw_req.timeline(user_id)
```
Este tipo de peticiones es paginable. La ejecución de esta función solamente regresa una instancia de la petición. Es posible paginar a mano a partir de ella. Si se busca una petición paginada Twigy proporciona funciones para realizarlas.

### Peticiones de menciones
Twigy tiene la capacidad de realizar peticiones de aquellos tweets en donde se menciona a un usuario. La función con la cual se realiza esta petición es la siguiente:

```python
    respuesta = tw_req.mentions(user_id)
```
Este tipo de peticiones es paginable. La ejecución de esta función solamente regresa una instancia de la petición. Es posible paginar a mano a partir de ella. Si se busca una petición paginada Twigy proporciona funciones para realizarlas.

### Peticiones de followers
Twigy tiene la capacidad de realizar peticiones de los usuarios que siguen a un usuario. La función con la cual se realiza esta petición es la siguiente:

```python
    respuesta = tw_req.followers(user_id)
```
Este tipo de peticiones es paginable. La ejecución de esta función solamente regresa una instancia de la petición. Es posible paginar a mano a partir de ella. Si se busca una petición paginada Twigy proporciona funciones para realizarlas.

### Peticiones de following
Twigy tiene la capacidad de realizar peticiones de los usuarios a los cuales sigue un usuario. La función con la cual se realiza esta petición es la siguiente:

```python
    respuesta = tw_req.following(user_id)
```
Este tipo de peticiones es paginable. La ejecución de esta función solamente regresa una instancia de la petición. Es posible paginar a mano a partir de ella. Si se busca una petición paginada Twigy proporciona funciones para realizarlas.

### Peticiones de liking
Twigy tiene la capacidad de realizar peticiones de los usuarios que han dado like a un tweet. La función con la cual se realiza esta petición es la siguiente:

```python
    respuesta = tw_req.liking(tweet_id)
```
Este tipo de peticiones es paginable. La ejecución de esta función solamente regresa una instancia de la petición. Es posible paginar a mano a partir de ella. Si se busca una petición paginada Twigy proporciona funciones para realizarlas.

### Peticiones de liked
Twigy tiene la capacidad de realizar peticiones de los tweets a los cuales un usuario ha dado un like. La función con la cual se realiza esta petición es la siguiente:

```python
    respuesta = tw_req.liked(user_id)
```
Este tipo de peticiones es paginable. La ejecución de esta función solamente regresa una instancia de la petición. Es posible paginar a mano a partir de ella. Si se busca una petición paginada Twigy proporciona funciones para realizarlas.

### Peticiones de búsquedas en Twitter
Twigy tiene la capacidad de realizar peticiones de búsquedas o queries en los datos de Twitter. La API de Twitter limita estas búsquedas a los últimos 7 días de actividad. 

Las queries realizadas deben satisfacer los lineamientos de construcción de queries de la API de Twitter. En este [enlace](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query) se puede saber más al respecto.

La función con la cual se realiza esta petición es la siguiente:

```python
    respuesta = tw_req.recent_search(query)
```
Este tipo de peticiones es paginable. La ejecución de esta función solamente regresa una instancia de la petición. Es posible paginar a mano a partir de ella. Si se busca una petición paginada Twigy proporciona funciones para realizarlas.

## Peticiones en bloque

Las funciones anteriores proporcionan la capacidad de acceder a los endpoints proporcionados por la API de Twitter, sin embargo usualmente la información que nos interesa rebaza los límites de elementos máximos devueltos en una petición impuestos por twitter. Para poder obtener más información es necesario paginar las peticiones.

Las siguientes funciones son funciones que realizan peticiones ya paginadas. Utilizan las funciones anteriores como bloques para construir respuestas más completas.

Es importante usarlas con cuidado, u uso indebido de estas funciones podría consumir rápidamente el número de peticiones disponibles a la API en un més que proporciona Twitter (actualmente 500,000 tweets por proyecto).

Ninguna de estas funciones regresa algún valor. Todas funcionan a través de efectos secundarios.  

Debido a que internamente se están realizando peticiones hasta satisfacer el criterio de límite los tiempos de ejecución de estas funciones pueden ser muy largos, por ejemplo para obtener todos los seguidores de una cuenta con millón y medio de seguidores se requieren aproximadamente 24 horas de ejecución. Debido a esto, las funciones utilizan efectos secundarios para guardar la información. 

Todas las funciones requieren como parámtero una lista en donde se anexarán los resultados. Si por alguna razón la función genera un error y un alto en la ejecución los datos extraídos hasta ese momento se encuentran en la lista proporcionada (Siempre y cuando el kernel siga vivo).

Todos los elementos agregados a las listas por esta función tienen el mismo formato. Las listas son obtenidas despues de procesar los elementos obtenidos en las pticiones y tienen la particularidad de que son dicts sin anidación con lo cual es posible parsearlas a un DataFrame de Pandas o guardarlas en un CSV.

Twigy proporciona las funciones con las que se procesan cada uno de los elementos.

Los elementos pueden ser del tipo:

- usuario
- tweet
- media
- poll
- lugar

Las funciones modifican por default una lista obligatoria y tienen la posibilidad de modificar listas adicionales opcionales si la petición genera información extendida en la API de Twitter.

### Petición de todos los followers de una cuenta

Twigy proporciona la siguiente función para paginar las peticiones de followers a una cuenta:

```python
    lista_usuarios = []
    respuesta = tw_req.bulk_followers(user_id, lista_usuarios)
```
donde `lista_usuarios` es la lista en donde se acumulará la información, puede ser una lista vacía o una lista con valores. Cada elemento en la lista resultante será un dict con la información de un usuario procesada.

Adicionalmente se puede agregar opcionalmente una lista de tweets para guardar la información de los tweets pinneados por los usuarios y regresados en la misma petición.

### Petición de todos los followings de una cuenta

Twigy proporciona la siguiente función para paginar las peticiones de followings a una cuenta:

```python
    lista_usuarios = []
    respuesta = tw_req.bulk_following(user_id, lista_usuarios)
```
donde `lista_usuarios` es la lista en donde se acumulará la información, puede ser una lista vacía o una lista con valores. Cada elemento en la lista resultante será un dict con la información de un usuario procesada.

Adicionalmente se puede agregar opcionalmente una lista de tweets para guardar la información de los tweets pinneados por los usuarios y regresados en la misma petición.

### Petición del timeline de un usuario

Twigy proporciona la siguiente función para paginar las peticiones de timeline a una cuenta:
```python
    lista_tweets = []
    respuesta = tw_req.bulk_timeline(user_id, lista_tweets)
```
donde `lista_tweets` es la lista en donde se acumulará la información, puede ser una lista vacía o una lista con valores. Cada elemento en la lista resultante será un dict con la información de un tweet procesada.

Este tipo de peticiones tienen un límite externo impuesto por Twitter correspondiente a 3,200 tweets. Si se requieren menos tweets se puede utilizar el parámetro max_tweets para controlar el número de tweets a extraer.

Adicionalmente se puede agregar opcionalmente una lista de usuarios para guardar la información de los usuarios que se reciban en la misma petición. De forma similar su pueden agregar listas para almacenar media, polls y lugares.

### Petición de las menciones a un usuario

Twigy proporciona la siguiente función para paginar las peticiones de timeline a una cuenta:
```python
    lista_tweets = []
    respuesta = tw_req.bulk_mentions(user_id, lista_tweets)
```
donde `lista_tweets` es la lista en donde se acumulará la información, puede ser una lista vacía o una lista con valores. Cada elemento en la lista resultante será un dict con la información de un tweet procesada.

Este tipo de peticiones tienen un límite externo impuesto por Twitter correspondiente a 800 tweets. Si se requieren menos tweets se puede utilizar el parámetro max_tweets para controlar el número de tweets a extraer.

Adicionalmente se puede agregar opcionalmente una lista de usuarios para guardar la información de los usuarios que se reciban en la misma petición. De forma similar su pueden agregar listas para almacenar media, polls y lugares.

### Petición de los tweets a los que un usuario ha dado like

Twigy proporciona la siguiente función para paginar las peticiones de liked de una cuenta:
```python
    lista_tweets = []
    respuesta = tw_req.bulk_liked(user_id, lista_tweets)
```
donde `lista_tweets` es la lista en donde se acumulará la información, puede ser una lista vacía o una lista con valores. Cada elemento en la lista resultante será un dict con la información de un tweet procesada.

Este tipo de peticiones no tienen un límite externo impuesto por Twitter por lo cual son altamente peligrosas ya que el número de tweets obtenidos se toma en cuenta para el límite de tweets en el proyecto y podría llegar a consumirlo por completo. Para evitar desbordar en tiempo de ejecución y en información la petición se utiliza un parámetro que controla el número másximo de tweets. El valor por default de este prámetro es 1,000. Si se requieren más o menos tweets se puede utilizar el parámetro max_tweets para controlar el número de tweets a extraer. Si se proporciona el valor None en este parámetro la función realizará todas las peticiones posibles.

Adicionalmente se puede agregar opcionalmente una lista de usuarios para guardar la información de los usuarios que se reciban en la misma petición. De forma similar su pueden agregar listas para almacenar media, polls y lugares.

### Petición de un query o una búsqueda

Twigy proporciona la siguiente función para paginar las peticiones de query a la API de Twitter:
```python
    lista_tweets = []
    respuesta = tw_req.bulk_recent_search(query, lista_tweets)
```
donde `lista_tweets` es la lista en donde se acumulará la información, puede ser una lista vacía o una lista con valores. Cada elemento en la lista resultante será un dict con la información de un tweet procesada.

Este tipo de peticiones no tienen un límite externo impuesto por Twitter a excepción de la limitante histórica de 7 días, por lo cual son altamente peligrosas ya que el número de tweets obtenidos se toma en cuenta para el límite de tweets en el proyecto y podría llegar a consumirlo por completo. Para evitar desbordar en tiempo de ejecución y en información la petición se utiliza un parámetro que controla el número másximo de tweets. El valor por default de este prámetro es 1,000. Si se requieren más o menos tweets se puede utilizar el parámetro max_tweets para controlar el número de tweets a extraer. Si se proporciona el valor None en este parámetro la función realizará todas las peticiones posibles.

Adicionalmente se puede agregar opcionalmente una lista de usuarios para guardar la información de los usuarios que se reciban en la misma petición. De forma similar su pueden agregar listas para almacenar media, polls y lugares.

## Ejemplo de como realizar una petición en bloque

```python
from twigy import Requester
import pandas as pd

user_id = '36121150'

users = []
tweets = []
tw_req.bulk_followers(user_id,users,lista_tweets=tweets)

users_df = pd.DataFrame(users)
tweet_df = pd.DataFrame(tweets)

users_df.to_csv(user_id + '_fl.csv', index=False)
tweet_df.to_csv(user_id + '_tw.csv', index=False)
```