import requests
import re
import warnings
import time
from datetime import datetime, timezone

api_url = 'https://api.twitter.com/2/'

class Requester():
    """Clase para un objeto que haga peticiones a la API de twitter."""

    def __init__(self, token):
        """Crea una instancia de un objeto Requester. 
        El parámetro token debe ser un bearer token válido para usarse en la API de twitter.
        Para conseguir uno hay que volverse tweeter developer.
        
        Las peticiones que realiza este objeto tienen como parámetros por default 
        los necesarios para obtener la mayor cantidad de información disponible
        en cada una de ellas y están configuradas para funcionar con la menor
        cantidad de información posible. Es posible usarlas con únicamente nombres
        de usuarios, ids de usuarios, ids de tweets, o queries de tweets.
        
        Las peticiones son regresadas 'en crudo', son objetos de tipo response
        correspondientes al package requests"""

        self.token = token
        self.api_url = 'https://api.twitter.com/2/'

        self.header = {"Authorization": "Bearer {}".format(self.token)}

        self.last_petition = {
            "url": None,
            "header": None,
            "parametros": None,
            "status_code": None,
            "meta": None,
        }

        self.default_parameters = {
            "expansions": ['attachments.poll_ids',
                        'attachments.media_keys',
                        'author_id',
                        'entities.mentions.username',
                        'geo.place_id',
                        'in_reply_to_user_id',
                        'referenced_tweets.id',
                        'referenced_tweets.id.author_id'],
            
            "tweet.fields": ['attachments',
                        'author_id',
                        'context_annotations',
                        'conversation_id',
                        'created_at',
                        'entities',
                        'geo',
                        'id',
                        'in_reply_to_user_id',
                        'lang',
                        'public_metrics',
                        'possibly_sensitive',
                        'referenced_tweets',
                        'reply_settings',
                        'source',
                        'text'],

            "user.fields": ['created_at',
                        'description',
                        'entities',
                        'id',
                        'location',
                        'name',
                        'pinned_tweet_id',
                        'profile_image_url',
                        'protected',
                        'public_metrics',
                        'url',
                        'username',
                        'verified'],

            "media.fields": ['duration_ms',
                        'height',
                        'media_key',
                        'preview_image_url',
                        'type',
                        'url',
                        'width',
                        'public_metrics'],

            "place.fields": ['contained_within',
                        'country',
                        'country_code',
                        'full_name',
                        'geo',
                        'id',
                        'name',
                        'place_type'],

            "poll.fields": ['duration_minutes',
                        'end_datetime',
                        'id',
                        'options',
                        'voting_status'],
        }

    def set_token(self,token):
        """Permite establecer el token a usar en las peticiones."""
        self.token = token
        self.header = {"Authorization": "Bearer {}".format(self.token)}

    def construct_params(self, param_dict):
        """Procesa la lista de parámetros para las peticiones.
        Si un parámetro en el diccionario de entrada es None, 
        el valor se busca en los valores por default de los parametros.
        Estos valores por default están definidos en la instancia del objeto.
        Si el parámetro en el diccionario de entrada es None y no hay un valor por default
        el parámetro no se agrega al conjunto de parámetros para la petición."""

        parametros = {}

        for key, value in param_dict.items():
            if value is None:
                if self.default_parameters.get(key) is not None:
                    parametros[key] = ','.join(self.default_parameters[key])
            else:
                if type(value) is list:
                    parametros[key] = ','.join(value)
                else:
                    parametros[key] = value

        return parametros

    def user(self, user_id, 
             expansions = ['pinned_tweet_id'], 
             tweet_fields = None, 
             user_fields = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener la información del usuario identificado con user_id
        
        Rate limit: 300 requests per 15-minute window (app auth)
        """

        check_id(user_id)

        url = self.api_url + 'users/{}'.format(user_id)

        header = self.header

        pre_params = {
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def user_by_uname(self, username, 
                      expansions = ['pinned_tweet_id'], 
                      tweet_fields = None, 
                      user_fields = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener la información del usuario identificado con username
        
        Rate limit: 300 requests per 15-minute window (app auth)
        """

        check_uname(username)

        url = self.api_url + 'users/by/username/{}'.format(username)

        header = self.header

        pre_params = {
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def users(self, ids, 
              expansions = ['pinned_tweet_id'], 
              tweet_fields = None, 
              user_fields = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener la información de máximo 100 usuarios
        identificados con los user_ids en la lista ids
        
        Rate limit: 300 requests per 15-minute window (app auth)
        """

        users_ids_filtered = check_id_list(ids)

        url = self.api_url + 'users'

        header = self.header

        pre_params = {
            "ids": users_ids_filtered,
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def users_by_uname(self, usernames, 
                       expansions = ['pinned_tweet_id'], 
                       tweet_fields = None, 
                       user_fields = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener la información de máximo 100 usuarios
        identificados con los usernames en la lista usernames
        
        Rate limit: 300 requests per 15-minute window (app auth)
        """

        usernames_filtered = check_uname_list(usernames)

        url = self.api_url + 'users/by'

        header = self.header

        pre_params = {
            "usernames": usernames_filtered,
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def tweet(self, tweet_id, 
              expansions = None, 
              tweet_fields = None, 
              user_fields = None, 
              poll_fields = None,
              place_fields = None,
              media_fields = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener la información del tweet
        identificado con el tweet_id
        
        Rate limit: 300 requests per 15-minute window (app auth)
        """

        check_id(tweet_id)

        url = self.api_url + 'tweets/{}'.format(tweet_id)

        header = self.header

        pre_params = {
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
            "poll.fields": poll_fields,
            "place.fields": place_fields,
            "media.fields": media_fields,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def tweets(self, tweet_ids, 
              expansions = None, 
              tweet_fields = None, 
              user_fields = None, 
              poll_fields = None,
              place_fields = None,
              media_fields = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener la información de máximo 100 tweets
        identificados con los tweet_ids en la lista
        
        Rate limit: 300 requests per 15-minute window (app auth)
        """

        tweet_ids_filtered = check_id_list(tweet_ids)

        url = self.api_url + 'tweets'

        header = self.header

        pre_params = {
            "ids": tweet_ids_filtered,
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
            "poll.fields": poll_fields,
            "place.fields": place_fields,
            "media.fields": media_fields,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def timeline(self, user_id, 
              expansions = None, 
              tweet_fields = None, 
              user_fields = None, 
              poll_fields = None,
              place_fields = None,
              media_fields = None,
              end_time = None,
              exclude = None,
              max_results = '100',
              pagination_token = None,
              since_id = None,
              start_time = None,
              until_id = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener el timeline del usuario
        identificado con user_id.
        
        La petición regresa un número de tweets igual a max_results
        cuyo valor por defecto es 100. Es posible obtener más tweets
        utilizando el pagination_token obtenido en una petición previa.
        
        La petición solamente tiene acceso a los 3,200 tweets más recientes.
        
        App rate limit: 1500 requests per 15-minute window
        """

        check_id(user_id)

        url = self.api_url + 'users/{}/tweets'.format(user_id)

        header = self.header

        pre_params = {
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
            "poll.fields": poll_fields,
            "place.fields": place_fields,
            "media.fields": media_fields,
            "end_time": end_time,
            "exclude": exclude,
            "max_results": max_results,
            "pagination_token": pagination_token,
            "since_id": since_id,
            "start_time": start_time,
            "until_id": until_id,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def mentions(self, user_id, 
              expansions = None, 
              tweet_fields = None, 
              user_fields = None, 
              poll_fields = None,
              place_fields = None,
              media_fields = None,
              end_time = None,
              max_results = '100',
              pagination_token = None,
              since_id = None,
              start_time = None,
              until_id = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener las menciones al usuario
        identificado con user_id.
        
        La petición regresa un número de tweets igual a max_results
        cuyo valor por defecto es 100. Es posible obtener más tweets
        utilizando el pagination_token obtenido en una petición previa.
        
        La petición solamente tiene acceso a los 800 tweets más recientes.
        
        App rate limit: 450 requests per 15-minute window
        """

        check_id(user_id)

        url = self.api_url + 'users/{}/mentions'.format(user_id)

        header = self.header

        pre_params = {
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
            "poll.fields": poll_fields,
            "place.fields": place_fields,
            "media.fields": media_fields,
            "end_time": end_time,
            "max_results": max_results,
            "pagination_token": pagination_token,
            "since_id": since_id,
            "start_time": start_time,
            "until_id": until_id,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def followers(self, user_id, 
              expansions = ['pinned_tweet_id'], 
              tweet_fields = None, 
              user_fields = None,
              max_results = '1000',
              pagination_token = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener los followers del usuario
        identificado con user_id.
        
        La petición regresa un número de usuarios igual a max_results
        cuyo valor por defecto es 1000. Es posible obtener más tweets
        utilizando el pagination_token obtenido en una petición previa.
        
        Rate limit: 15 requests per 15-minute window (app auth)
        """

        check_id(user_id)

        url = self.api_url + 'users/{}/followers'.format(user_id)

        header = self.header

        pre_params = {
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
            "max_results": max_results,
            "pagination_token": pagination_token,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def following(self, user_id, 
              expansions = ['pinned_tweet_id'], 
              tweet_fields = None, 
              user_fields = None,
              max_results = '1000',
              pagination_token = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener los following del usuario
        identificado con user_id.
        
        La petición regresa un número de usuarios igual a max_results
        cuyo valor por defecto es 1000. Es posible obtener más tweets
        utilizando el pagination_token obtenido en una petición previa.
        
        Rate limit: 15 requests per 15-minute window (app auth)
        """

        check_id(user_id)

        url = self.api_url + 'users/{}/following'.format(user_id)

        header = self.header

        pre_params = {
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
            "max_results": max_results,
            "pagination_token": pagination_token,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def liking(self, tweet_id, 
              expansions = ['pinned_tweet_id'],
              tweet_fields = None, 
              user_fields = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener los usuarios
        que han dado un like al tweet identificado con tweet_id.
        
        La petición esta limitada a 100 usuarios por todo el lifetime del tweet.

        App rate limit: 75 requests per 15-minute window
        """

        check_id(tweet_id)

        url = self.api_url + 'tweets/{}/liking_users'.format(tweet_id)

        header = self.header

        pre_params = {
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def liked(self, user_id, 
              expansions = None, 
              tweet_fields = None, 
              user_fields = None, 
              poll_fields = None,
              place_fields = None,
              media_fields = None,
              max_results = '100',
              pagination_token = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener los tweets a los cuales
        ha dado like el usuario identificado con user_id.
        
        La petición regresa un número de tweets igual a max_results
        cuyo valor por defecto es 100. Es posible obtener más tweets
        utilizando el pagination_token obtenido en una petición previa.
        
        App rate limit: 75 requests per 15-minute window
        """

        check_id(user_id)

        url = self.api_url + 'users/{}/liked_tweets'.format(user_id)

        header = self.header

        pre_params = {
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
            "poll.fields": poll_fields,
            "place.fields": place_fields,
            "media.fields": media_fields,
            "max_results": max_results,
            "pagination_token": pagination_token,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta

    def recent_search(self, query, 
              expansions = None, 
              tweet_fields = None, 
              user_fields = None, 
              poll_fields = None,
              place_fields = None,
              media_fields = None,
              max_results = '100',
              next_token = None,
              end_time = None,
              since_id = None,
              start_time = None,
              until_id = None):
        """Realiza una petición a la API de twitter.
        La petición tiene como objetivo obtener los tweets que satisfagan
        la búsqueda introducida en query.

        La búsqueda debe seguir los operadores y lineamientos de busquedas de
        la API de twitter.
        
        La petición regresa un número de tweets igual a max_results
        cuyo valor por defecto es 100. Es posible obtener más tweets
        utilizando el pagination_token obtenido en una petición previa.
        
        App rate limit: 450 requests per 15-minute window
        """

        url = self.api_url + 'tweets/search/recent'

        header = self.header

        pre_params = {
            "query": query,
            "expansions": expansions,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
            "poll.fields": poll_fields,
            "place.fields": place_fields,
            "media.fields": media_fields,
            "max_results": max_results,
            "next_token": next_token,
            "end_time": end_time,
            "since_id": since_id,
            "start_time": start_time,
            "until_id": until_id,
        }
        parametros = self.construct_params(pre_params)

        respuesta = self.peticion(url, header, parametros)

        return respuesta


    def bulk_followers(self, user_id, lista_usuarios, pagination_token = None, 
                        lista_tweets = None):
        """Realiza peticiones secuenciales y paginadas a la API de twitter.
        La petición tiene como objetivo obtener todos los followers de la cuenta
        identificada con user_id.

        Este endpoint es lento, admite 15 peticiones cada 15 minutos, cada petición
        puede obtener hasta 1,000 usuarios. Este tipo de petición no tiene cap.

        Las peticiones se realizan secuencialmente hasta que se recibe un 
        status code 429, en ese momento la función descansa las peticiones
        900 segundos (15 minutos).

        La función no tiene regreso, los datos obtenidos se agregan a 
        lista_ususarios como efecto secundario, esto debido al tiempo 
        prolongado en el que corre esta función. Si se quiebra, lista_usuarios
        tendrá la información recabada hasta ese momento. Reanudar las peticiones
        es posible usando el token de paginación almacenado en la propiedad
        last_petition del Requester si es que fue válida la última petición.

        La función tiene la posibilidad de modificar listas extra con información
        correspondiente a las extensiones usuales de la API de twitter. En este caso
        puede acumular los pinned_tweets de los usuarios recolectados. Para
        almacenar esta información es necesario pasar alguna de las siguientes listas
        opcionales de acuerdo al tipo de información que se quiera almacenar:

        tweets - lista_tweets
        """

        flag = 0
        my_date = None
        peticiones = 0
        while pagination_token is not None or flag == 0:
            flag = 1
            respuesta = self.followers(user_id, pagination_token=pagination_token)
            my_date = datetime.now(timezone.utc)
            peticiones = peticiones + 1
            if respuesta.status_code == 429:
                print("Esperando, {} realizadas.".format(peticiones))
                time.sleep(900)
                respuesta = self.followers(user_id, pagination_token=pagination_token)
                my_date = datetime.now(timezone.utc)
                peticiones = peticiones + 1
            if (respuesta.status_code == 200) and callable(getattr(respuesta, 'json', None)):
                datos = respuesta.json().get('data')
                meta = respuesta.json().get('meta')
                includes = respuesta.json().get('includes')
                if datos is not None:
                    users_to_list(datos, lista_usuarios, my_date)
                if lista_tweets is not None and includes is not None:
                    tweets = includes['tweets']
                    if tweets is not None:
                        tweets_to_list(tweets, lista_tweets, my_date)
                if meta is not None:
                    pagination_token = meta.get('next_token')


    def bulk_following(self, user_id, lista_usuarios, pagination_token = None,
                        lista_tweets = None):
        """Realiza peticiones secuenciales y paginadas a la API de twitter.
        La petición tiene como objetivo obtener todos los followings de la cuenta
        identificada con user_id.

        Este endpoint es lento, admite 15 peticiones cada 15 minutos, cada petición
        puede obtener hasta 1,000 usuarios. Este tipo de petición no tiene cap.

        Las peticiones se realizan secuencialmente hasta que se recibe un 
        status code 429, en ese momento la función descansa las peticiones
        900 segundos (15 minutos).

        La función no tiene regreso, los datos obtenidos se agregan a 
        lista_ususarios como efecto secundario, esto debido al tiempo 
        prolongado en el que corre esta función. Si se quiebra, lista_usuarios
        tendrá la información recabada hasta ese momento. Reanudar las peticiones
        es posible usando el token de paginación almacenado en la propiedad
        last_petition del Requester si es que fue válida la última petición.

        La función tiene la posibilidad de modificar listas extra con información
        correspondiente a las extensiones usuales de la API de twitter. En este caso
        puede acumular los pinned_tweets de los usuarios recolectados. Para
        almacenar esta información es necesario pasar alguna de las siguientes listas
        opcionales de acuerdo al tipo de información que se quiera almacenar:

        tweets - lista_tweets
        """

        flag = 0
        my_date = None
        peticiones = 0
        while pagination_token is not None or flag == 0:
            flag = 1
            respuesta = self.following(user_id, pagination_token=pagination_token)
            my_date = datetime.now(timezone.utc)
            peticiones = peticiones + 1
            if respuesta.status_code == 429:
                print("Esperando, {} realizadas.".format(peticiones))
                time.sleep(900)
                respuesta = self.following(user_id, pagination_token=pagination_token)
                my_date = datetime.now(timezone.utc)
                peticiones = peticiones + 1
            if (respuesta.status_code == 200) and callable(getattr(respuesta, 'json', None)):
                datos = respuesta.json().get('data')
                meta = respuesta.json().get('meta')
                includes = respuesta.json().get('includes')
                if datos is not None:
                    users_to_list(datos, lista_usuarios, my_date)
                if lista_tweets is not None and includes is not None:
                    tweets = includes['tweets']
                    if tweets is not None:
                        tweets_to_list(tweets, lista_tweets, my_date)
                if meta is not None:
                    pagination_token = meta.get('next_token')

    def bulk_timeline(self, user_id, lista_tweets, max_tweets = None, pagination_token = None,
                        lista_users=None, 
                        lista_media=None, 
                        lista_polls=None, 
                        lista_places=None):
        """Realiza peticiones secuenciales y paginadas a la API de twitter.
        La petición tiene como objetivo obtener todos los tweets posibles
        correspondientes al timeline de la cuenta identificada con user_id.
        El número de tweets máximo obtenible de acuerdo a la documentación
        de la API es de 3,200 para una timeline. Si no se desea obtener todos
        los tweets posibles para un usuario es posible limitar el comportamiento
        usando el parámetro max_tweets.

        Este endpoint es lento, admite 1,500 peticiones cada 15 minutos, cada petición
        puede obtener hasta 100 tweets. Los tweets obtenidos con esta petición 
        cuentan para el cap total del proyecto en el API de twitter. Este cap es de 
        500,000 tweets al mes con una cuenta de tipo standard.

        Las peticiones se realizan secuencialmente hasta que se recibe un 
        status code 429, en ese momento la función descansa las peticiones
        900 segundos (15 minutos).

        La función no tiene regreso, los datos obtenidos se agregan a 
        lista_tweets como efecto secundario, esto debido al tiempo 
        prolongado en el que corre esta función. Si se quiebra, lista_tweets
        tendrá la información recabada hasta ese momento. Reanudar las peticiones
        es posible usando el token de paginación almacenado en la propiedad
        last_petition del Requester si es que fue válida la última petición.

        La función tiene la posibilidad de modificar listas extra con información
        correspondiente a las extensiones usuales de la API de twitter. Para
        almacenar esta información es necesario pasar alguna de las siguientes listas
        opcionales de acuerdo al tipo de información que se quiera almacenar:

        usuarios - lista_users
        media - lista_media
        polls - lista_polls
        places - lista_places
        """

        flag = 0
        my_date = None
        peticiones = 0
        tweets_count = 0
        while pagination_token is not None or flag == 0:
            flag = 1
            respuesta = self.timeline(user_id, pagination_token=pagination_token)
            my_date = datetime.now(timezone.utc)
            peticiones = peticiones + 1
            if respuesta.status_code == 429:
                print("Esperando, {} realizadas.".format(peticiones))
                time.sleep(900)
                respuesta = self.timeline(user_id, pagination_token=pagination_token)
                my_date = datetime.now(timezone.utc)
                peticiones = peticiones + 1
            if (respuesta.status_code == 200) and callable(getattr(respuesta, 'json', None)):
                datos = respuesta.json().get('data')
                meta = respuesta.json().get('meta')
                includes = respuesta.json().get('includes')
                if datos is not None:
                    tweets_to_list(datos, lista_tweets, my_date)
                if lista_users is not None and includes is not None:
                    usuarios = includes.get('users')
                    if usuarios is not None:
                        users_to_list(usuarios, lista_users, my_date)
                if lista_media is not None and includes is not None:
                    media = includes.get('media')
                    if media is not None:
                        media_to_list(media, lista_media, my_date)
                if lista_polls is not None and includes is not None:
                    polls = includes.get('polls')
                    if polls is not None:
                        polls_to_list(polls, lista_polls, my_date)
                if lista_places is not None and includes is not None:
                    places = includes.get('places')
                    if places is not None:
                        places_to_list(places, lista_places, my_date)
                if meta is not None:
                    pagination_token = meta.get('next_token')
            if max_tweets is not None and tweets_count >= max_tweets:
                pagination_token = None

    def bulk_mentions(self, user_id, lista_tweets, max_tweets = None, pagination_token = None,
                        lista_users=None, 
                        lista_media=None, 
                        lista_polls=None, 
                        lista_places=None):
        """Realiza peticiones secuenciales y paginadas a la API de twitter.
        La petición tiene como objetivo obtener todos los tweets posibles
        correspondientes al timeline de la cuenta identificada con user_id.
        El número de tweets máximo obtenible de acuerdo a la documentación
        de la API es de 800 para un usuario. Si no se desea obtener todos
        los tweets posibles para un usuario es posible limitar el comportamiento
        usando el parámetro max_tweets.

        Este endpoint es lento, admite 1,500 peticiones cada 15 minutos, cada petición
        puede obtener hasta 100 tweets. Los tweets obtenidos con esta petición 
        cuentan para el cap total del proyecto en el API de twitter. Este cap es de 
        500,000 tweets al mes con una cuenta de tipo standard.

        Las peticiones se realizan secuencialmente hasta que se recibe un 
        status code 429, en ese momento la función descansa las peticiones
        900 segundos (15 minutos).

        La función no tiene regreso, los datos obtenidos se agregan a 
        lista_tweets como efecto secundario, esto debido al tiempo 
        prolongado en el que corre esta función. Si se quiebra, lista_tweets
        tendrá la información recabada hasta ese momento. Reanudar las peticiones
        es posible usando el token de paginación almacenado en la propiedad
        last_petition del Requester si es que fue válida la última petición.

        La función tiene la posibilidad de modificar listas extra con información
        correspondiente a las extensiones usuales de la API de twitter. Para
        almacenar esta información es necesario pasar alguna de las siguientes listas
        opcionales de acuerdo al tipo de información que se quiera almacenar:

        usuarios - lista_users
        media - lista_media
        polls - lista_polls
        places - lista_places
        """

        flag = 0
        my_date = None
        peticiones = 0
        tweets_count = 0
        while pagination_token is not None or flag == 0:
            flag = 1
            respuesta = self.mentions(user_id, pagination_token=pagination_token)
            my_date = datetime.now(timezone.utc)
            peticiones = peticiones + 1
            if respuesta.status_code == 429:
                print("Esperando, {} realizadas.".format(peticiones))
                time.sleep(900)
                respuesta = self.mentions(user_id, pagination_token=pagination_token)
                my_date = datetime.now(timezone.utc)
                peticiones = peticiones + 1
            if (respuesta.status_code == 200) and callable(getattr(respuesta, 'json', None)):
                datos = respuesta.json().get('data')
                meta = respuesta.json().get('meta')
                includes = respuesta.json().get('includes')
                if datos is not None:
                    tweets_to_list(datos, lista_tweets, my_date)
                if lista_users is not None and includes is not None:
                    usuarios = includes.get('users')
                    if usuarios is not None:
                        users_to_list(usuarios, lista_users, my_date)
                if lista_media is not None and includes is not None:
                    media = includes.get('media')
                    if media is not None:
                        media_to_list(media, lista_media, my_date)
                if lista_polls is not None and includes is not None:
                    polls = includes.get('polls')
                    if polls is not None:
                        polls_to_list(polls, lista_polls, my_date)
                if lista_places is not None and includes is not None:
                    places = includes.get('places')
                    if places is not None:
                        places_to_list(places, lista_places, my_date)
                if meta is not None:
                    pagination_token = meta.get('next_token')
            if max_tweets is not None and tweets_count >= max_tweets:
                pagination_token = None

    def bulk_liked(self, user_id, lista_tweets, max_tweets = 1000, pagination_token = None,
                        lista_users=None, 
                        lista_media=None, 
                        lista_polls=None, 
                        lista_places=None):
        """Realiza peticiones secuenciales y paginadas a la API de twitter.
        La petición tiene como objetivo obtener todos los tweets a los cuales
        les ha dado like la cuenta identificada con user_id.
        No hay un número aparente de tweets máximos a obtener con este endpoint,
        por esta razón la función limita por default el comportamiento a 1,000 tweets. 
        Si se desea cambiar este número es posbile hacerlo con el parámetro max_tweets.
        Si se coloca None en este parámetro la función obtendrá todos los tweets posibles.

        Este endpoint es lento, admite 75 peticiones cada 15 minutos, cada petición
        puede obtener hasta 100 tweets. Los tweets obtenidos con esta petición 
        cuentan para el cap total del proyecto en el API de twitter. Este cap es de 
        500,000 tweets al mes con una cuenta de tipo standard.

        Las peticiones se realizan secuencialmente hasta que se recibe un 
        status code 429, en ese momento la función descansa las peticiones
        900 segundos (15 minutos).

        La función no tiene regreso, los datos obtenidos se agregan a 
        lista_tweets como efecto secundario, esto debido al tiempo 
        prolongado en el que corre esta función. Si se quiebra, lista_tweets
        tendrá la información recabada hasta ese momento. Reanudar las peticiones
        es posible usando el token de paginación almacenado en la propiedad
        last_petition del Requester si es que fue válida la última petición.

        La función tiene la posibilidad de modificar listas extra con información
        correspondiente a las extensiones usuales de la API de twitter. Para
        almacenar esta información es necesario pasar alguna de las siguientes listas
        opcionales de acuerdo al tipo de información que se quiera almacenar:

        usuarios - lista_users
        media - lista_media
        polls - lista_polls
        places - lista_places
        """

        flag = 0
        my_date = None
        peticiones = 0
        tweets_count = 0
        while pagination_token is not None or flag == 0:
            flag = 1
            respuesta = self.liked(user_id, pagination_token=pagination_token)
            my_date = datetime.now(timezone.utc)
            peticiones = peticiones + 1
            if respuesta.status_code == 429:
                print("Esperando, {} realizadas.".format(peticiones))
                time.sleep(900)
                respuesta = self.liked(user_id, pagination_token=pagination_token)
                my_date = datetime.now(timezone.utc)
                peticiones = peticiones + 1
            if (respuesta.status_code == 200) and callable(getattr(respuesta, 'json', None)):
                datos = respuesta.json().get('data')
                tweets_count = tweets_count + len(datos)
                meta = respuesta.json().get('meta')
                includes = respuesta.json().get('includes')
                if datos is not None:
                    tweets_to_list(datos, lista_tweets, my_date)
                if lista_users is not None and includes is not None:
                    usuarios = includes.get('users')
                    if usuarios is not None:
                        users_to_list(usuarios, lista_users, my_date)
                if lista_media is not None and includes is not None:
                    media = includes.get('media')
                    if media is not None:
                        media_to_list(media, lista_media, my_date)
                if lista_polls is not None and includes is not None:
                    polls = includes.get('polls')
                    if polls is not None:
                        polls_to_list(polls, lista_polls, my_date)
                if lista_places is not None and includes is not None:
                    places = includes.get('places')
                    if places is not None:
                        places_to_list(places, lista_places, my_date)
                if meta is not None:
                    pagination_token = meta.get('next_token')
            if max_tweets is not None and tweets_count >= max_tweets:
                pagination_token = None

    def bulk_recent_search(self, query, lista_tweets, max_tweets = 1000, pagination_token = None,
                        lista_users=None, 
                        lista_media=None, 
                        lista_polls=None, 
                        lista_places=None):
        """Realiza peticiones secuenciales y paginadas a la API de twitter.
        La petición tiene como objetivo obtener todos los tweets que satisfagan 
        el query proporcionado. El query debe seguir los lineamientos de twitter
        con respecto a queries y acepta los operadores habilitados en la cuenta 
        de developer. El endpoint solo es capaz de obtener tweets de los últimos 7 días.
        El número total de tweets a obtener no está limitado, debido a esto la función 
        limita por default el comportamiento a 1,000 tweets. Si se desea cambiar 
        este número es posbile hacerlo con el parámetro max_tweets.
        Si se coloca None en este parámetro la función obtendrá todos los tweets posibles.

        Este endpoint es lento, admite 450 peticiones cada 15 minutos, cada petición
        puede obtener hasta 100 tweets. Los tweets obtenidos con esta petición 
        cuentan para el cap total del proyecto en el API de twitter. Este cap es de 
        500,000 tweets al mes con una cuenta de tipo standard.

        Las peticiones se realizan secuencialmente hasta que se recibe un 
        status code 429, en ese momento la función descansa las peticiones
        900 segundos (15 minutos).

        La función no tiene regreso, los datos obtenidos se agregan a 
        lista_tweets como efecto secundario, esto debido al tiempo 
        prolongado en el que corre esta función. Si se quiebra, lista_tweets
        tendrá la información recabada hasta ese momento. Reanudar las peticiones
        es posible usando el token de paginación almacenado en la propiedad
        last_petition del Requester si es que fue válida la última petición.

        La función tiene la posibilidad de modificar listas extra con información
        correspondiente a las extensiones usuales de la API de twitter. Para
        almacenar esta información es necesario pasar alguna de las siguientes listas
        opcionales de acuerdo al tipo de información que se quiera almacenar:

        usuarios - lista_users
        media - lista_media
        polls - lista_polls
        places - lista_places
        """

        flag = 0
        my_date = None
        peticiones = 0
        tweets_count = 0
        while pagination_token is not None or flag == 0:
            flag = 1
            respuesta = self.recent_search(query, next_token=pagination_token)
            my_date = datetime.now(timezone.utc)
            peticiones = peticiones + 1
            if respuesta.status_code == 429:
                print("Esperando, {} realizadas.".format(peticiones))
                time.sleep(900)
                respuesta = self.recent_search(query, next_token=pagination_token)
                my_date = datetime.now(timezone.utc)
                peticiones = peticiones + 1
            if (respuesta.status_code == 200) and callable(getattr(respuesta, 'json', None)):
                datos = respuesta.json().get('data')
                tweets_count = tweets_count + len(datos)
                meta = respuesta.json().get('meta')
                includes = respuesta.json().get('includes')
                if datos is not None:
                    tweets_to_list(datos, lista_tweets, my_date)
                if lista_users is not None and includes is not None:
                    usuarios = includes.get('users')
                    if usuarios is not None:
                        users_to_list(usuarios, lista_users, my_date)
                if lista_media is not None and includes is not None:
                    media = includes.get('media')
                    if media is not None:
                        media_to_list(media, lista_media, my_date)
                if lista_polls is not None and includes is not None:
                    polls = includes.get('polls')
                    if polls is not None:
                        polls_to_list(polls, lista_polls, my_date)
                if lista_places is not None and includes is not None:
                    places = includes.get('places')
                    if places is not None:
                        places_to_list(places, lista_places, my_date)
                if meta is not None:
                    pagination_token = meta.get('next_token')
            if max_tweets is not None and tweets_count >= max_tweets:
                pagination_token = None


    def peticion(self, url, header, parametros):
        """Realiza una petición a la API de twitter.
        La petición es una petición a url, con header y parametros
        indicados como input.
        
        Si la petición regresa un status_code igual a 503 la función espera 15 segundos
        y vuelve a realizar la petición una segunda vez."""

        twreq = requests.request("GET", url, headers=header, params=parametros)

        if twreq.status_code == 503:
            time.sleep(15)
            twreq = requests.request("GET", url, headers=header, params=parametros)

        if twreq.status_code != 200:
            warnings.warn("El código de status de la respuesta a la petición no es 200.")

        self.last_petition['url'] = url
        self.last_petition['header'] = header
        self.last_petition['parametros'] = parametros
        self.last_petition['status_code'] = twreq.status_code
        if twreq.status_code == 200:
            self.last_petition['meta'] = twreq.json().get('meta')
        else:
            self.last_petition['meta'] = None

        return twreq

def check_id(user_id):
    """Checa que la cadena user_id cumpla con 
    el patrón especificado para ids en la API de twitter '^[0-9]{1,19}$'"""

    test = bool(re.match("^[0-9]{1,19}$", user_id))
    if not test:
        raise Exception("El id no satisface el patrón especificado por la API de twitter '^[0-9]{1,19}$'")

def check_uname(username):
    """Checa que la cadena username cumpla con 
    el patrón especificado para usernames en la API de twitter '^[A-Za-z0-9_]{1,15}$'"""

    test = bool(re.match("^[A-Za-z0-9_]{1,15}$", username))
    if not test:
        raise Exception("El id no satisface el patrón especificado por la API de twitter '^[A-Za-z0-9_]{1,15}$'")

def check_id_list(users_ids):
    """filtra una lista de cadenas a aquellas que cumplan con 
    el patrón especificado para ids en la API de twitter '^[0-9]{1,19}$'"""

    if len(users_ids) > 100:
        raise Exception("El número de ids es mayor que 100")

    users_ids_filtered = list(filter(lambda x: bool(re.match("^[0-9]{1,19}$", x)), users_ids))

    if len(users_ids_filtered) == 0:
        raise Exception("Ninguno de los ids satisface el patrón especificado por la API de twitter '^[0-9]{1,19}$'")

    if len(users_ids) != len(users_ids_filtered):
        warnings.warn("Alguno de los ids no satisface el patrón especificado por la API de twitter '^[0-9]{1,19}$'")

    return users_ids_filtered

def check_uname_list(usernames):
    """filtra una lista de cadenas a aquellas que cumplan con 
    el patrón especificado para usernames en la API de twitter '^[A-Za-z0-9_]{1,15}$'"""

    if len(usernames) > 100:
        raise Exception("El número de ids es mayor que 100")

    usernames_filtered = list(filter(lambda x: bool(re.match("^[A-Za-z0-9_]{1,15}$", x)), usernames))

    if len(usernames_filtered) == 0:
        raise Exception("Ninguno de los ids satisface el patrón especificado por la API de twitter '^[A-Za-z0-9_]{1,15}$'")

    if len(usernames) != len(usernames_filtered):
        warnings.warn("Alguno de los ids no satisface el patrón especificado por la API de twitter '^[A-Za-z0-9_]{1,15}$'")

    return usernames_filtered

def process_user(user,date=None):
    """Procesa la información de un usuario entregando solamente info desanidada.
    El objetivo es obtener estructuras de datos que pueden procesarse en un DataFrame
    o exportarse en un CSV.
    
    Tiene la capacidad de agregar una fecha a la info de cada usuario. Esta fecha
    tiene como objetivo almacenar la fecha en la que se realizó la petición."""

    salida = {}
    salida['id'] = user.get('id')
    salida['name'] = user.get('name',"").replace("\n", " ").replace("\t", " ").replace("\r", " ")
    salida['username'] = user.get('username',"").replace("\n", " ").replace("\t", " ").replace("\r", " ")
    salida['created_at'] = user.get('created_at')
    salida['description'] = user.get('description',"").replace("\n", " ").replace("\t", " ").replace("\r", " ")
    salida['location'] = user.get('location',"").replace("\n", " ").replace("\t", " ").replace("\r", " ")
    salida['pinned_tweet_id'] = user.get('pinned_tweet_id')
    salida['protected'] = user.get('protected')
    metrics = user.get('public_metrics')
    if metrics is not None:
        salida['followers'] = metrics.get('followers_count')
        salida['following'] = metrics.get('following_count')
        salida['tweets'] = metrics.get('tweet_count')
        salida['listed'] = metrics.get('listed_count')
    salida['fecha_peticion'] = date
    return salida

def users_to_list(user_list,lista,date=None):
    """Agrupa y procesa una petición con información de usuarios en una lista.
    El objetivo es obtener estructuras de datos que pueden procesarse en un DataFrame
    o exportarse en un CSV.
    
    Recibe directamente el dict con la información de los usuarios.
    
    Tiene la capacidad de agregar una fecha a la info de cada usuario. Esta fecha
    tiene como objetivo almacenar la fecha en la que se realizó la petición."""

    for usuario in user_list:
        temp = process_user(usuario,date)
        lista.append(temp)

def process_tweet(tweet,date=None):
    """Procesa la información de un tweet entregando solamente info desanidada.
    El objetivo es obtener estructuras de datos que pueden procesarse en un DataFrame
    o exportarse en un CSV.
    
    Tiene la capacidad de agregar una fecha a la info de cada tweet. Esta fecha
    tiene como objetivo almacenar la fecha en la que se realizó la petición."""

    salida = {}
    salida['id'] = tweet.get('id')
    salida['text'] = tweet.get('text','').replace("\n", " ").replace("\t", " ").replace("\r", " ")
    salida['author_id'] = tweet.get('author_id')
    salida['conversation_id'] = tweet.get('conversation_id')
    salida['created_at'] = tweet.get('created_at')
    salida['in_reply_to_user_id'] = tweet.get('in_reply_to_user_id')
    salida['lang'] = tweet.get('lang')
    salida['source'] = tweet.get('source')
    salida['x'] = None
    salida['y'] = None
    geo = tweet.get('geo')
    if geo is not None:
        coords = geo.get('coordinates')
        if coords is not None:
            salida['x'] = coords['coordinates'][0]
            salida['y'] = coords['coordinates'][1]
    metrics = tweet.get('public_metrics')
    if metrics is not None:
        salida['retweet_count'] = metrics.get('retweet_count')
        salida['reply_count'] = metrics.get('reply_count')
        salida['like_count'] = metrics.get('like_count')
        salida['quote_count'] = metrics.get('quote_count')
    salida['fecha_peticion'] = date
    return salida

def tweets_to_list(tweets_list,lista,date=None):
    """Agrupa y procesa una petición con información de tweets en una lista.
    El objetivo es obtener estructuras de datos que pueden procesarse en un DataFrame
    o exportarse en un CSV.
    
    Recibe directamente el dict con la información de los tweets.
    
    Tiene la capacidad de agregar una fecha a la info de cada tweet. Esta fecha
    tiene como objetivo almacenar la fecha en la que se realizó la petición."""

    for tweet in tweets_list:
        temp = process_tweet(tweet,date)
        lista.append(temp)

def process_media(media,date=None):
    """Procesa la información de un media entregando solamente info desanidada.
    El objetivo es obtener estructuras de datos que pueden procesarse en un DataFrame
    o exportarse en un CSV.
    
    Tiene la capacidad de agregar una fecha a la info de cada media. Esta fecha
    tiene como objetivo almacenar la fecha en la que se realizó la petición."""

    salida = {}
    salida['media_key'] = media.get('media_key')
    salida['type'] = media.get('type')
    salida['duration_ms'] = media.get('duration_ms')
    metrics = media.get('public_metrics')
    if metrics is not None:
        salida['view_count'] = metrics.get('view_count')
    salida['fecha_peticion'] = date
    return salida

def media_to_list(media_list,lista,date=None):
    """Agrupa y procesa una petición con información de media en una lista.
    El objetivo es obtener estructuras de datos que pueden procesarse en un DataFrame
    o exportarse en un CSV.
    
    Recibe directamente el dict con la información de los media.
    
    Tiene la capacidad de agregar una fecha a la info de cada media. Esta fecha
    tiene como objetivo almacenar la fecha en la que se realizó la petición."""

    for media in media_list:
        temp = process_media(media,date)
        lista.append(temp)

def process_poll(poll,date=None):
    """Procesa la información de un poll entregando solamente info desanidada.
    El objetivo es obtener estructuras de datos que pueden procesarse en un DataFrame
    o exportarse en un CSV.
    
    Tiene la capacidad de agregar una fecha a la info de cada poll. Esta fecha
    tiene como objetivo almacenar la fecha en la que se realizó la petición."""

    salida = {}
    salida['id'] = poll.get('id')
    salida['duration_minutes'] = poll.get('duration_minutes')
    salida['end_datetime'] = poll.get('end_datetime')
    salida['voting_status'] = poll.get('voting_status')
    options = poll.get('options')
    salida['fecha_peticion'] = date
    if options is not None:
        for option in options:
            position = str(option.get("position"))
            label = option.get("label","").replace("\n", " ").replace("\t", " ").replace("\r", " ")
            votos = option.get("votes")
            llave = "label-" + position
            llvot = "votos-" + position
            salida[llave] = label
            salida[llvot] = votos
    return salida

def polls_to_list(poll_list,lista,date=None):
    """Agrupa y procesa una petición con información de polls en una lista.
    El objetivo es obtener estructuras de datos que pueden procesarse en un DataFrame
    o exportarse en un CSV.
    
    Recibe directamente el dict con la información de los polls.
    
    Tiene la capacidad de agregar una fecha a la info de cada poll. Esta fecha
    tiene como objetivo almacenar la fecha en la que se realizó la petición."""

    for poll in poll_list:
        temp = process_poll(poll,date)
        lista.append(temp)

def process_place(place,date=None):
    """Procesa la información de un lugar entregando solamente info desanidada.
    El objetivo es obtener estructuras de datos que pueden procesarse en un DataFrame
    o exportarse en un CSV.
    
    Tiene la capacidad de agregar una fecha a la info de cada lugar. Esta fecha
    tiene como objetivo almacenar la fecha en la que se realizó la petición."""

    salida = {}
    salida['id'] = place.get('id')
    salida['full_name'] = place.get('full_name',"").replace("\n", " ").replace("\t", " ").replace("\r", " ")
    salida['name'] = place.get('name',"").replace("\n", " ").replace("\t", " ").replace("\r", " ")
    salida['country'] = place.get('country',"").replace("\n", " ").replace("\t", " ").replace("\r", " ")
    salida['country_code'] = place.get('country_code')
    salida['place_type'] = place.get('place_type')
    salida['fecha_peticion'] = date
    return salida

def places_to_list(place_list,lista,date=None):
    """Agrupa y procesa una petición con información de lugares en una lista.
    El objetivo es obtener estructuras de datos que pueden procesarse en un DataFrame
    o exportarse en un CSV.
    
    Recibe directamente el dict con la información de los lugares.
    
    Tiene la capacidad de agregar una fecha a la info de cada lugar. Esta fecha
    tiene como objetivo almacenar la fecha en la que se realizó la petición."""

    for place in place_list:
        temp = process_place(place,date)
        lista.append(temp)    

