# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

import logging
import json
import random
import os
import boto3


role_arn = "arn:aws:iam::579700122166:role/StitchesPerm" 
table_name = 'MedidasClientes'

sts_client = boto3.client('sts')
assumed_role_object=sts_client.assume_role(RoleArn=role_arn, RoleSessionName='Session1')
credentials=assumed_role_object['Credentials']

dynamodb = boto3.resource('dynamodb',
                  aws_access_key_id=credentials['AccessKeyId'],
                  aws_secret_access_key=credentials['SecretAccessKey'],
                  aws_session_token=credentials['SessionToken'],
                  region_name='us-east-1')


table = dynamodb.Table(table_name)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        return (
            handler_input.response_builder
                .speak("Bienvenido a Stitches! Puedes agregar las medidas de clientes, así como modificarlas, eliminarlas o consultarlas. Dime, qué necesitas?")
                .ask("Quieres continuar?")
                .response
        )


class RegistraClienteIntentHandler(AbstractRequestHandler):
    """Handler for RegistraCliente Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RegistraCliente")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Hello World!"
        slots = handler_input.request_envelope.request.intent.slots
        user_name = slots['nombre'].value
        cintura = slots['cintura'].value
        pecho = slots['pecho'].value
        cadera = slots['cadera'].value
        tiro = slots['tiro'].value
        talle = slots['talle'].value
        espalda = slots['espalda'].value
        
        table.put_item(
            Item={
                'user_id': user_name,
                'Cintura': cintura,
                'Pecho': pecho,
                'Cadera': cadera,
                'Tiro': tiro,
                'Talle': talle,
                'Espalda': espalda
            }
        )
        
        speak_output = "Se ha registrado a " + str(user_name)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Continua la sesión")
                .response
        )
class ConsultaMedidasIntentHandler(AbstractRequestHandler):
    """Handler for ConsultaMedidas Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ConsultaMedidas")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Hello World!"
        slots = handler_input.request_envelope.request.intent.slots
        user_names = slots['nombre'].value
        
        try:
            response = table.get_item(
                Key={
                    'user_id': user_names
                }
            )
            item = response['Item']
            user_name = item['user_id']
            user_cintura = item['Cintura']
            pecho = item['Pecho']
            cadera = item['Cadera']
            tiro = item['Tiro']
            talle = item['Talle']
            espalda = item['Espalda']
            
            speech_output = "se encontró a "+ user_names + " con la medida de cintura: "+ str(user_cintura)  + ", pecho: " + str(pecho) + " , cadera: " + str(cadera) + " ,tiro: " + str(tiro)  + " ,talle: " + str(talle)+ " , y espalda: " + str(espalda)
            
        except:
            speech_output = "No pude encontrar al cliente requerido."

        
        #speak_output = "Se ha registrado a " + str(user_name)

        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask("Continua la sesión")
                .response
        )
class ModificaMedidaIntentHandler(AbstractRequestHandler):
    """Handler for ModificaMedida Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ModificaMedida")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Hello World!"
        slots = handler_input.request_envelope.request.intent.slots
        user_name = slots['nombre'].value
        parte_corporal = str(slots['parte_corporal'].value)
        valor_nuevo = slots['valor_nuevo'].value

        if parte_corporal == 'cintura':
            table.update_item(
                Key={
                    'user_id': user_name
                },
                UpdateExpression='SET Cintura = :val1',
                ExpressionAttributeValues={
                    ':val1': valor_nuevo
                }
            )
            
            speak_output = "He modificado el valor de cintura de " + user_name + " a " + str(valor_nuevo)
        elif parte_corporal == 'pecho':
            table.update_item(
                Key={
                    'user_id': user_name
                },
                UpdateExpression='SET Pecho = :val1',
                ExpressionAttributeValues={
                    ':val1': valor_nuevo
                }
            )
            
            speak_output = "He modificado el valor de pecho de " + user_name + " a " + str(valor_nuevo)
        elif parte_corporal == 'cadera':
            table.update_item(
                Key={
                    'user_id': user_name
                },
                UpdateExpression='SET Cadera = :val1',
                ExpressionAttributeValues={
                    ':val1': valor_nuevo
                }
            ) 
            
            
            speak_output = "He modificado el valor de cadera de " + user_name + " a " + str(valor_nuevo)
        elif parte_corporal == 'tiro':
            table.update_item(
                Key={
                    'user_id': user_name
                },
                UpdateExpression='SET Tiro = :val1',
                ExpressionAttributeValues={
                    ':val1': valor_nuevo
                }
            ) 
            
            
            speak_output = "He modificado el valor de la altura del tiro de " + user_name + " a " + str(valor_nuevo)
        elif parte_corporal == 'talle':
            table.update_item(
                Key={
                    'user_id': user_name
                },
                UpdateExpression='SET Talle = :val1',
                ExpressionAttributeValues={
                    ':val1': valor_nuevo
                }
            ) 
            
            
            speak_output = "He modificado el valor del talle  de " + user_name + " a " + str(valor_nuevo)
        elif parte_corporal == 'espalda':
            table.update_item(
                Key={
                    'user_id': user_name
                },
                UpdateExpression='SET Espalda = :val1',
                ExpressionAttributeValues={
                    ':val1': valor_nuevo
                }
            ) 
            
            
            speak_output = "He modificado el valor de la espalda  de " + user_name + " a " + str(valor_nuevo)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Continua la sesión")
                .response
        )
class EliminaClienteIntentHandler(AbstractRequestHandler):
    """Handler for EliminaCliente Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("EliminaCliente")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Hello World!"
        slots = handler_input.request_envelope.request.intent.slots
        user_name = slots['nombre'].value

        
        table.delete_item(
            Key={
                'user_id': user_name
            }
        )
        
        speak_output = "He eliminado las medidas de " + str(user_name)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Continua la sesión")
                .response
        )
class ConsultaUnaMedidaIntentHandler(AbstractRequestHandler):
    """Handler for ConsultaUnaMedida Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ConsultaUnaMedida")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Hello World!"
        slots = handler_input.request_envelope.request.intent.slots
        user_names = slots['nombre'].value
        parte_corporal = str(slots['parte_del_cuerpo'].value)
        
        try:
            response = table.get_item(
                Key={
                    'user_id': user_names
                }
            )
            item = response['Item']
            user_name = str(item['user_id'])
            user_cintura = str(item['Cintura'])
            pecho = str(item['Pecho'])
            cadera = str(item['Cadera'])
            tiro = str(item['Tiro'])
            talle = str(item['Talle'])
            espalda = str(item['Espalda'])
            
            parteCorporal = ['cintura', 'pecho', 'cadera','tiro','talle','espalda']
            
            #speech_output = "se encontró a "+ user_names + " con la medida de cintura: "+ str(user_cintura)  + ", pecho: " + str(pecho) + " ,y cadera: " + str(cadera)
            
            if parte_corporal == 'cintura' and user_cintura != '0':
                speech_output = "La medida de cintura de " + str(user_name) + " es " + str(user_cintura)
            elif parte_corporal == "pecho" and pecho != '0':
                speech_output = "La medida de pecho de " + str(user_name) + " es " + str(pecho)
            elif parte_corporal == 'cadera' and cadera != '0':
                speech_output = "La medida de cadera de " + str(user_name) + " es " + str(cadera)
            elif parte_corporal == 'tiro' and tiro != '0':
                speech_output = "La medida de tiro de " + str(user_name) + " es " + str(tiro)
            elif parte_corporal == 'talle' and talle != '0':
                speech_output = "La medida del talle de " + str(user_name) + " es " + str(talle)
            elif parte_corporal == 'espalda' and espalda != '0':
                speech_output = "La medida de la espalda de " + str(user_name) + " es " + str(espalda)
            elif (pecho == '0' or user_cintura == '0' or cadera=='0' or tiro=='0' or talle=='0' or espalda=='0') and parte_corporal in parteCorporal:
                speech_output = "No hay medida registrada para esa parte del cuerpo de " + str(user_name)
                
            
        except:
            speech_output = "No pude encontrar al cliente requerido."


        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask("Continua la sesión")
                .response
        )

class ParaConsultarMedidasIntentHandler(AbstractRequestHandler):
    """Handler for ParaConsultarMedidas Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ParaConsultarMedidas")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Hello World!"
        slots = handler_input.request_envelope.request.intent.slots
        accion = str(slots['accion'].value)
        
        valores_acciones = ['modificar', 'cambiar', 'actualizar']
            
        #speech_output = "se encontró a "+ user_names + " con la medida de cintura: "+ str(user_cintura)  + ", pecho: " + str(pecho) + " ,y cadera: " + str(cadera)
            
        if accion in valores_acciones :
            speech_output = "Para actualizar una medida de un cliente, solo di: 'Modifica medida'"
        elif accion == "eliminar":
            speech_output = "Para eliminar las medidas de un cliente, solo di: 'Elimina a, seguido del nombre del cliente'"
        elif accion == 'registrar':
            speech_output = "Solo di: registrar a un nuevo cliente"
        elif accion == 'consultar':
            speech_output = 'Di: dame las medidas de, seguido del nombre de la persona cuyas medidas quieres consultar'
                


        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask("Continua la sesión")
                .response
        ) 


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Consulta medidas solo diciendo: medidas de. más nombre del cliente cuyas medidas requieres"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Espero haber sido de ayuda, vuelve pronto!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "No entendí lo que deseas hacer, pueder repetirlo? por favor"
        reprompt = "Con qué te puedo ayudar?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Acabas de activar el intent " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Lo siento, ocurrió un problema, intentalo de nuevo."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RegistraClienteIntentHandler())
sb.add_request_handler(ConsultaMedidasIntentHandler())
sb.add_request_handler(ModificaMedidaIntentHandler())
sb.add_request_handler(EliminaClienteIntentHandler())
sb.add_request_handler(ConsultaUnaMedidaIntentHandler())
sb.add_request_handler(ParaConsultarMedidasIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()