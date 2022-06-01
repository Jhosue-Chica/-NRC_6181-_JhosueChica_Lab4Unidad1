import datetime 
import requests
import os
import argparse
import re
import json

from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase


class FeriadoEcuador(HolidayBase):
    """
    Una clase que representa las vacaciones en Ecuador por provincia (FeriadoEcuador)
    Su objetivo es determinar si una fecha específica sea un feriado lo más rápido
    y flexible posible.
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...
    Atributos (Hereda la clase FeriadoEcuador)
    ----------
    prov: str
        código de provincia según ISO3166-2
        
    Metodos
    -------
    __init__(self, placa, date, time, online=False):
        Construye todos los atributos necesarios para el objeto FeriadoEcuador.
    _populate(self, year):
        Devuelve si una fecha es festiva o no
    """     
    # ISO 3166-2 códigos de las principales subdivisiones, 
    # llamadas provincias
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCES = ["EC-P"]  # TODO añadir más provincias

    def __init__(self, **kwargs):
        """
        Construye todos los atributos necesarios para el objeto FeriadoEcuador.
        """         
        self.pais = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        """
        Comprueba si una fecha es festiva o no
        
        Parametros
        ----------
        year : str
            year of a date
        Retorna
        -------
        Devuelve True si una fecha es festiva, en caso contrario False 
        """                    
        # Año Nuevo
        self[datetime.date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        
        # Navidad
        self[datetime.date(year, DEC, 25)] = "Navidad [Christmas]"
        
        # Semana Santa
        self[easter(year) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo) [Good Friday)]"
        self[easter(year)] = "Día de Pascuas [Easter Day]"
        
        # Carnaval
        total_lent_days = 46
        self[easter(year) - datetime.timedelta(days=total_lent_days+2)] = "Lunes de carnaval [Carnival of Monday)]"
        self[easter(year) - datetime.timedelta(days=total_lent_days+1)] = "Martes de carnaval [Tuesday of Carnival)]"
        
        # Dia de trabajo
        name = "Día Nacional del Trabajo [Labour Day]"
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en 
        # sábado o martes el descanso obligatorio pasará al viernes o lunes inmediato anterior respectivamente
        if year > 2015 and datetime.date(year, MAY, 1).weekday() in (5,1):
            self[datetime.date(year, MAY, 1) - datetime.timedelta(days=1)] = name
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) 
        # si el feriado cae en domingo el descanso obligatorio pasará al lunes siguiente
        elif year > 2015 and datetime.date(year, MAY, 1).weekday() == 6:
            self[datetime.date(year, MAY, 1) + datetime.timedelta(days=1)] = name
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Los feriados que sean
        # en miércoles o jueves se trasladarán al viernes de esa semana
        elif year > 2015 and  datetime.date(year, MAY, 1).weekday() in (2,3):
            self[datetime.date(year, MAY, 1) + rd(weekday=FR)] = name
        else:
            self[datetime.date(year, MAY, 1)] = name
        
        # Batalla del Pichincha, las reglas son las mismas que las del día del trabajo
        name = "Batalla del Pichincha [Pichincha Battle]"
        if year > 2015 and datetime.date(year, MAY, 24).weekday() in (5,1):
            self[datetime.date(year, MAY, 24).weekday() - datetime.timedelta(days=1)] = name
        elif year > 2015 and datetime.date(year, MAY, 24).weekday() == 6:
            self[datetime.date(year, MAY, 24) + datetime.timedelta(days=1)] = name
        elif year > 2015 and  datetime.date(year, MAY, 24).weekday() in (2,3):
            self[datetime.date(year, MAY, 24) + rd(weekday=FR)] = name
        else:
            self[datetime.date(year, MAY, 24)] = name        
        
        # Primer Grito de la Independencia, las reglas son las mismas que las del día del trabajo
        name = "Primer Grito de la Independencia [First Cry of Independence]"
        if year > 2015 and datetime.date(year, AUG, 10).weekday() in (5,1):
            self[datetime.date(year, AUG, 10)- datetime.timedelta(days=1)] = name
        elif year > 2015 and datetime.date(year, AUG, 10).weekday() == 6:
            self[datetime.date(year, AUG, 10) + datetime.timedelta(days=1)] = name
        elif year > 2015 and  datetime.date(year, AUG, 10).weekday() in (2,3):
            self[datetime.date(year, AUG, 10) + rd(weekday=FR)] = name
        else:
            self[datetime.date(year, AUG, 10)] = name       
        
        # Independencia de Guayaquil, las reglas son las mismas que las del día del trabajo
        name = "Independencia de Guayaquil [Guayaquil's Independence]"
        if year > 2015 and datetime.date(year, OCT, 9).weekday() in (5,1):
            self[datetime.date(year, OCT, 9) - datetime.timedelta(days=1)] = name
        elif year > 2015 and datetime.date(year, OCT, 9).weekday() == 6:
            self[datetime.date(year, OCT, 9) + datetime.timedelta(days=1)] = name
        elif year > 2015 and  datetime.date(year, MAY, 1).weekday() in (2,3):
            self[datetime.date(year, OCT, 9) + rd(weekday=FR)] = name
        else:
            self[datetime.date(year, OCT, 9)] = name        
        
        # Día de los difuntos
        namedd = "Día de los difuntos [Day of the Dead]" 
        # Independence of Cuenca
        nameic = "Independencia de Cuenca [Independence of Cuenca]"
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906))
        # Para los feriados nacionales y/o locales que coincidan en días continuos,
        # se aplicarán las siguientes reglas:
        if (datetime.date(year, NOV, 2).weekday() == 5 and  datetime.date(year, NOV, 3).weekday() == 6):
            self[datetime.date(year, NOV, 2) - datetime.timedelta(days=1)] = namedd
            self[datetime.date(year, NOV, 3) + datetime.timedelta(days=1)] = nameic     
        elif (datetime.date(year, NOV, 3).weekday() == 2):
            self[datetime.date(year, NOV, 2)] = namedd
            self[datetime.date(year, NOV, 3) - datetime.timedelta(days=2)] = nameic
        elif (datetime.date(year, NOV, 3).weekday() == 3):
            self[datetime.date(year, NOV, 3)] = nameic
            self[datetime.date(year, NOV, 2) + datetime.timedelta(days=2)] = namedd
        elif (datetime.date(year, NOV, 3).weekday() == 5):
            self[datetime.date(year, NOV, 2)] =  namedd
            self[datetime.date(year, NOV, 3) - datetime.timedelta(days=2)] = nameic
        elif (datetime.date(year, NOV, 3).weekday() == 0):
            self[datetime.date(year, NOV, 3)] = nameic
            self[datetime.date(year, NOV, 2) + datetime.timedelta(days=2)] = namedd
        else:
            self[datetime.date(year, NOV, 2)] = namedd
            self[datetime.date(year, NOV, 3)] = nameic  
            
        # Fundación de Quito, se aplica sólo a la provincia de Pichincha, 
        # las reglas son las mismas que las del día del trabajo
        name = "Fundación de Quito [Foundation of Quito]"        
        if self.prov in ("EC-P"):
            if year > 2015 and datetime.date(year, DEC, 6).weekday() in (5,1):
                self[datetime.date(year, DEC, 6) - datetime.timedelta(days=1)] = name
            elif year > 2015 and datetime.date(year, DEC, 6).weekday() == 6:
                self[(datetime.date(year, DEC, 6).weekday()) + datetime.timedelta(days=1)] =name
            elif year > 2015 and  datetime.date(year, DEC, 6).weekday() in (2,3):
                self[datetime.date(year, DEC, 6) + rd(weekday=FR)] = name
            else:
                self[datetime.date(year, DEC, 6)] = name

class PicoPlaca:
    """
    Una clase para representar un vehículo 
    medida de restricción (Pico y Placa) 
    - ORDENANZA METROPOLITANA No. 0305
    http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
    ...
    Atributos
    ----------
    placa : str 
        La matrícula o patente de un vehículo es una combinación de caracteres alfabéticos
        o numéricos que identifica al vehículo respecto a los demás;
        El formato utilizado es 
        XX-YYYY o XXX-YYYY, 
        donde X es una letra mayuscula e Y es un digito.
        
    date : str
        Fecha en la que el vehículo intenta transitar
        Se trata de seguir la
        ISO 8601 fomato AAAA-MM-DD: por ejemplo., 2020-04-22.
        
    time : str
        time in which the vehicle intends to transit
        Se trata de seguir el formato 
        HH:MM: por ejemplo, 08:35, 19:30
        
    online: boolean,
        si online == True se utilizará la API de holidays
        
    Metodos
    -------
    __init__(self, placa, date, time, online=False):
        Construye todos los atributos necesarios 
        para el objeto PicoPlaca.
    placa(self):
        Obtiene el valor del atributo placa
    placa(self, value):
        Establece el valor del atributo placa
    date(self):
        Obtiene el valor del atributo fecha
    date(self, value):
        Establece el valor del atributo de fecha
    time(self):
        Obtiene el valor del atributo tiempo
    time(self, value):
        Establece el valor del atributo de tiempo
    __encontrar_dia(self, date):
        Devuelve el día de la fecha: por ejemplo, Jueves
    __es_tiempo_prohibido(self, revisar_tiempo):
        Devuelve True si la hora proporcionada está dentro de las horas punta prohibidas,
        en caso contrario False
    __es_feriado:
        Devuelve True si la fecha comprobada (en formato ISO 8601 AAAA-MM-DD) es un día festivo
        en Ecuador, en caso contrario False
    predict(self):
        Devuelve True si el vehículo con la placa especificada puede estar en la carretera
        en la fecha y hora especificadas, en caso contrario False
    """ 
    #Dias de la semana
    __diasSemana=[
            "Lunes",
            "Martes",
            "Miercoles",
            "Jueves",
            "Viernes",
            "Sabado",
            "Domingo"]

    # Diccionario que contiene las restricciones inf la forma {dia: última cifra prohibida}
    __restricciones = {
            "Lunes": [1, 2],
            "Martes": [3, 4],
            "Miercoles": [5, 6],
            "Jueves": [7, 8],
            "Viernes": [9, 0],
            "Sabado": [],
            "Domingo": []}

    def __init__(self, placa, date, time, online=False):
        """
        Construye todos los atributos necesarios para el objeto PicoPlaca.
        
        Parametros
        ----------
            placa : str 
                La matrícula o patente de un vehículo es una combinación de caracteres alfabéticos o numéricos 
                que identifica el vehículo con respecto a los demás; 
                El formato utilizado es XXX-YYYY o XX-YYYY, donde X es una letra mayúscula e Y es un dígito.            
            date : str
                Fecha en la que el vehículo pretende transitar
                Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
            time : str
                tiempo en el que el vehículo pretende transitar
                Sigue el formato HH:MM: por ejemplo, 08:35, 19:30
            online: boolean
                si online == True se utilizará la API de días festivos abstractos (por defecto es False)               
        """                
        self.placa = placa
        self.date = date
        self.time = time
        self.online = online


    @property
    def placa(self):
        """Obtiene el valor del atributo placa"""
        return self._placa


    @placa.setter
    def placa(self, value):
        """
        Establece el valor del atributo placa
        Parametros
        ----------
        value : str
        
        Raises
        ------
        ValueError
            Si la cadena de valores no está formada como 
            XX-YYYY o XXX-YYYY, 
            donde X es una letra mayúscula e Y es un dígito
        """
        if not re.match('^[A-Z]{2,3}-[0-9]{4}$', value):
            raise ValueError(
                'La placa debe tener el siguiente formato XX-YYYY o XXX-YYYY, donde X es una letra mayúscula e Y es un dígito')
        self._placa = value


    @property
    def date(self):
        """Obtiene el valor del atributo fecha"""
        return self._date

    @date.setter
    def date(self, value):
        """
        Establece el valor del atributo de fecha
        Parametros
        ----------
        value : str
        
        Raises
        ------
        ValueError
            Si la cadena de valores no está formada como AAAA-MM-DD (por ejemplo: 2021-04-02)
        """
        try:
            if len(value) != 10:
                raise ValueError
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'La fecha debe tener el siguiente formato: AAAA-MM-DD (por ejemplo: 2021-04-02)') from None
        self._date = value
        

    @property
    def time(self):
        """Obtiene el valor del atributo tiempo"""
        return self._time

    @time.setter
    def time(self, value):
        """
        Establece el valor del atributo de tiempo
        Parametros
        ----------
        value : str
        
        Raises
        ------
        ValueError
            Si la cadena de valores no está formada como HH:MM (por ejemplo, 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', value):
            raise ValueError(
                'La hora debe tener el siguiente formato: HH:MM (por ejemplo, 08:31, 14:22, 00:01)')
        self._time = value


    def __encontrar_dia(self, date):
        """
        Busca el día a partir de la fecha: por ejemplo, miércoles
        Parametros
        ----------
        date : str
            Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        Retorna
        -------
        Devuelve el día de la fecha como una cadena
        """        
        d = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
        return self.__diasSemana[d]


    def __es_tiempo_prohibido(self, revisar_tiempo):
        """
        Comprueba si la hora proporcionada está dentro de las horas punta prohibidas,
        donde las horas punta son: 07:00 - 09:30 y 16:00 - 19:30        
        Parametros
        ----------
        revisar_tiempo : str
            Hora que se comprobará. Está en formato HH:MM: por ejemplo, 08:35, 19:15
        Retorna
        -------
        Devuelve True si la hora proporcionada está dentro de las horas punta prohibidas,
        en caso contrario False
        """           
        t = datetime.datetime.strptime(revisar_tiempo, '%H:%M').time()
        return ((t >= datetime.time(7, 0) and t <= datetime.time(9, 30)) or
                (t >= datetime.time(16, 0) and t <= datetime.time(19, 30)))


    def __es_feriado(self, date, online):
        """
        Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador
        si online == True utilizará una API REST, de lo contrario generará los días festivos del año examinado
        
        Parametros
        ----------
        date : str
            Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        online: boolean, optional
            si online == True se utilizará la API de días festivos abstractos (por defecto es False)        
        Retorna
        -------
        Devuelve True si la fecha comprobada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador,
        en caso contrario False
        """            
        y, m, d = date.split('-')

        if online:
            # abstractapi Holidays API, versión gratuita: 1000 peticiones al mes
            # 1 solicitud por segundo
            # recuperar la clave API de la variable de entorno
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # Esto significa que falta una clave API
                raise requests.HTTPError(
                    'Falta la clave de la API. Guarde su clave en la variable de entorno HOLIDAYS_API_KEY')
            if response.content == b'[]':  # si no hay vacaciones obtenemos un array vacío
                return False
            # Arreglar el Jueves Santo incorrectamente indicado como día festivo
            if json.loads(response.text[1:-1])['name'] == 'Jueves Santo':
                return False
            return True
        else:
            ecu_holidays = FeriadoEcuador(prov='EC-P')
            return date in ecu_holidays


    def predict(self):
        """
        Comprueba si el vehículo con la placa especificada puede estar en la carretera en la fecha y hora indicadas,
        basándose en las normas de Pico y Placa:
        http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf    
        Retorna
        -------
        Retorna True si el vehículo con la placa especificada puede estar en la carretera 
        en la fecha y hora especificadas, en caso contrario, False
        """
        # Compruebe si la fecha es un día festivo
        if self.__es_feriado(self.date, self.online):
            return True

        # Compruebe si hay vehículos excluidos de la restricción según la segunda letra
        # de la placa o si utiliza sólo dos letras
        # https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador
        if self.placa[1] in 'AUZEXM' or len(self.placa.split('-')[0]) == 2:
            return True

        # Compruebe si la hora prevista no está en las horas punta prohibidas
        if not self.__es_tiempo_prohibido(self.time):
            return True

        day = self.__encontrar_dia(self.date)  # Busca el día de la semana a partir de la fecha
        # Compruebe si el último dígito de la placa no está restringido en este día en particular
        if int(self.placa[-1]) not in self.__restricciones[day]:
            return True

        return False


if __name__ == '__main__':

    online=False
    
    placa=input("Ingrese placa (segun el formato XXX-YYYY o XX-YYYY, donde X es una letra mayuscula e Y es un digito): ")
    
    date=input("Ingrese la fecha de circulacion (segun el formato AAAA-MM-DD): ")
    
    time=input("Ingrese la hora de circulacion (segun el formato HH:MM): ")

    pyp = PicoPlaca(placa, date, time, online)

    if pyp.predict():
        print(
            'El vehiculo con placa {} puede circular en la fecha {} a las {}.'.format(
                placa,
                date,
                time))
    else:
        print(
            'El vehiculo con placa {} no puede circular en la fecha {} a las {}.'.format(
                placa,
                date,
                time))