#ME ESCUTE

URL = "http://152.67.51.53:8123/api/webhook/BYqtMGhmIvQx9y4E2EcP2uVQb86khe2m"

import requests
import logging
import random
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.slu.entityresolution.resolution import Resolution
from ask_sdk_model.slu.entityresolution import StatusCode
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)
        
    def handle(self, handler_input):
        speak_output = random.choice([
            "Posso ajudar?", 
            "Do que precisa?", 
            "Como posso ajudar?", 
            "Em que posso ajudar?",
            "Estou as ordens.",
            "O que deseja?",
            "O que posso fazer?",
            "Em que posso ser útil?",
            "As ordens."
        ])
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class SelecionadoHanlder(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name('Selecionado')(handler_input)
        
    def handle(self, handler_input):
        slot = ask_utils.get_slot(handler_input=handler_input, slot_name="Selecionados")
        
        if slot and slot.resolutions and slot.resolutions.resolutions_per_authority:
            for resolution in slot.resolutions.resolutions_per_authority:
                if resolution.status.code == StatusCode.ER_SUCCESS_MATCH:
                    objeto = resolution.values[0].value.name
                    requests.post(URL, data=objeto)
                    item = handler_input.request_envelope.request.intent.slots['Selecionados'].value
                    requests.post(URL, data=item)
                    speak_output = random.choice([
                        "Algo mais?", 
                        "Mais alguma coisa?",
                        "Executado. Posso fazer mais alguma coisa?",
                        "Prontinho. precisa de algo mais?",
                        "Okey. Feito. Algo mais?",
                        "Okey. Algo mais?",
                        "Ainda posso ajudar?"
                    ])
                    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class IgnoradoHanlder(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("Ignorado")(handler_input)
        
    def handle(self, handler_input):
        slot = ask_utils.get_slot(handler_input=handler_input, slot_name="Ignorados")
        
        if slot and slot.resolutions and slot.resolutions.resolutions_per_authority:
            for resolution in slot.resolutions.resolutions_per_authority:
                if resolution.status.code == StatusCode.ER_SUCCESS_MATCH:
                    objeto = resolution.values[0].value.name
                    requests.post(URL, data=objeto)
                    speak_output = random.choice([
                        "Um segundo.", 
                        "Um instante.",
                        "Um momento."
                    ])
                    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FinalHanlder(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("Final")(handler_input)

    def handle(self, handler_input):
        slot = ask_utils.get_slot(handler_input=handler_input, slot_name="Finais")
        
        if slot and slot.resolutions and slot.resolutions.resolutions_per_authority:
            for resolution in slot.resolutions.resolutions_per_authority:
                if resolution.status.code == StatusCode.ER_SUCCESS_MATCH:
                    requests.post(URL, data="Interação finalizada.")
                    speak_output = random.choice([
                        "Interação finalizada.", 
                        "Finalizando.",
                        "Terminando.",
                        "Terminado.",
                        "Okey.",
                        "Okey. Finalizando.",
                        "Finalizado."
                    ])
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class EndedRequestHanlder(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)
        
    def handle(self, handler_input):
        requests.post(URL, data="Interação sem resposta.")
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
    
class CancelHanlder(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input)
        
    def handle(self, handler_input):
        requests.post(URL, data="Interação cancelada.")
        speak_output = random.choice([
            "Interação cancelada.",
            "Cancelei a interação."
        ])
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
    
class StopHanlder(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)
        
    def handle(self, handler_input):
        requests.post(URL, data="Interação parada.")
        speak_output = random.choice([
            "Interação foi parada.",
            "Parei a interação."
        ])
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class HelpHanlder(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)
        
    def handle(self, handler_input):
        requests.post(URL, data="Solicitação de ajuda.")
        speak_output = random.choice([
            "Infelizmente não tenho instrução para ajudar. Por favor, repita o comando.",
            "Não tenho habilidade desenvolvida para ajuda. Tente outravez."
        ])
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True
            
    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        requests.post(URL, data="Resposta errada.")
        speak_output = random.choice([
            "Resposta não cadastrada.", 
            "Essa resposta não está no cadastro",
            "Não existe cadastro dessa resposta.",
            "Não posso executar. Não existe cadastro dessa resposta.",
            "Por favor. Preciso que antes cadastre a resposta.",
            "Resposta não existente."
        ])
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SelecionadoHanlder())
sb.add_request_handler(IgnoradoHanlder())
sb.add_request_handler(FinalHanlder())
sb.add_request_handler(EndedRequestHanlder())
sb.add_request_handler(CancelHanlder())
sb.add_request_handler(StopHanlder())
sb.add_request_handler(HelpHanlder())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()