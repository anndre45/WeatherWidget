"""" Controle do Tempo Exemplo Flet """

# Bibliotecas 

import flet 
from flet import *
import requests
import datetime
from secret import secret

api_key = secret.api_key

_current = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?lat=-19.912998&lon=-43.940933&exclude=minutely,hourly,alert&units=metric&appid={api_key}&lang=pt_br"
)

def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def _expand(e):
        if e.data == "true":
            _c.content.controls[0].height = 540
            _c.content.controls[0].update()
        else:
            _c.content.controls[0].height = 640 * 0.40
            _c.content.controls[0].update()

    def _current_temp():

        _current_temp = int(_current.json()["main"]["temp"])
        _current_weather = _current.json()["weather"][0]["main"]
        _current_description = _current.json()["weather"][0]["description"]
        _current_wind = int(_current.json()["wind"]["speed"])
        _current_humidity = int(_current.json()["main"]["humidity"])
        _current_feels = int(_current.json()["main"]["feels_like"])
        
        return[_current_temp, _current_weather, _current_description, _current_wind, _current_humidity, _current_feels]

    def _current_extra():
        _extra_info = []

        _extra = [
            [
               int(_current.json()["visibility"] / 1000 ),
               "Km",
               "Visibility",
               "./src/visibility.png"
            ],
            [
               round(_current.json()["main"]["pressure"] * 0.03 , 2 ),
               "inHg",
               "Pressure",
               "./src/barometer.png"
            ],
            [
               datetime.datetime.fromtimestamp(
                   _current.json()["sys"]["sunrise"]
               ).strftime("%I:%M %p"),
               "",
               "Sunrise",
               "./src/sunrise.png"
            ],
            [
               datetime.datetime.fromtimestamp(
                   _current.json()["sys"]["sunset"]
               ).strftime("%I:%M %p"),
               "",
               "Sunset",
               "./src/sunset.png"
            ]
        ]

        for data in _extra:
            _extra_info.append(
                Container(
                    bgcolor="white10",
                    border_radius=12,
                    alignment=alignment.center,
                    content=Column(
                        alignment='center',
                        horizontal_alignment='center',
                        spacing=25,
                        controls=[
                            Container(
                                alignment=alignment.center,
                                content=Image(
                                    src=data[3],
                                    color="white"
                                ),
                                width=32,
                                height=32
                            ),
                            Container(
                                content=Column(
                                    alignment="center",
                                    horizontal_alignment="center",
                                    spacing=0,
                                    controls=[  
                                        Text(
                                            str(
                                                data[0]
                                            )   + " " + data[1],
                                            size=14, 
                                        ),
                                        Text(
                                            data[2],
                                            size=11,
                                            color="white54" 
                                        )

                                    ]
                                )
                            )
                        ]
                    )
                )
            )
        return _extra_info

    def _top():
        
        _today = _current_temp()

        _today_extra = GridView(
            max_extent=150,
            expand=1,
            run_spacing=8,
            spacing=8,
        )

        for info in _current_extra():
            _today_extra.controls.append(info)

        top = Container(
            width= 460,
            height= 660 * 0.40,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=["lightblue600", "lightblue900"]
            ),
            border_radius=35,
            animate=animation.Animation(duration=500,
                                        curve="decelerate"),
            on_hover=lambda e: _expand(e),
            content= Column(
                alignment='start',
                spacing=10,
                controls=[
                    Row(
                        alignment='center',
                        controls=[
                            Text(
                                "\nBelo Horizonte, MG",
                                size= 16,
                                weight="w500",
                            )
                        ]
                    ),
                    Container(padding=padding.only
                              (bottom=5)),
                    Row(
                        alignment= 'center',
                        spacing=20,
                        controls=[
                            Column(
                                controls=[
                                    Container(
                                        width=90,
                                        height=90,
                                        image_src="./src/cloudy.png"
                                    )
                                ]
                            ),
                            Column(
                                spacing=5,
                                horizontal_alignment='center',
                                controls=[
                                    Text(
                                        "Today",
                                        size=12,
                                        text_align="center",
                                    ),
                                    Row(
                                        vertical_alignment= 'start',
                                        spacing=0,
                                        controls=[
                                            Container(
                                                content=Text(
                                                    _today[0],
                                                    size=42,
                                                )
                                            ),
                                            Container(
                                                content=Text(
                                                    "°",
                                                    size=28,
                                                    text_align="center"
                                                )
                                            )
                                        ]
                                    ),
                                    Text(
                                        _today[1] + " - Overcast",
                                        size=10,
                                        color="white54",
                                        text_align="center",
                                    )
                                ]
                            )
                        ]
                    ),
                    Divider(
                        height=8,
                        thickness=1,
                        color="white10"
                    ),
                    Row(
                        alignment='spaceAround',
                        controls=[
                            Container(
                                content=Column(
                                    horizontal_alignment="center",
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image(src="./src/wind.png",
                                                          color="white"),
                                            width=20,
                                            height=20
                                        ),
                                        Text(
                                            str(str( _today[3]) + " km/h"),
                                            size=11,
                                        ),
                                        Text(
                                            "Wind",
                                            size=9,
                                            color="white54"
                                        )
                                    ]
                                )
                            ),
                            Container(
                                content=Column(
                                    horizontal_alignment="center",
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image(src="./src/humidity.png",
                                                          color="white"),
                                            width=20,
                                            height=20
                                        ),
                                        Text(
                                            str(str( _today[4]) + "%"),
                                            size=11,
                                        ),
                                        Text(
                                            "Humidity",
                                            size=9,
                                            color="white54"
                                        )
                                    ]
                                )
                            ),
                            Container(
                                content=Column(
                                    horizontal_alignment="center",
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image(src="./src/termometer.png",
                                                          color="white"),
                                            width=20,
                                            height=20
                                        ),
                                        Text(
                                            str(str( _today[5]) + "°"),
                                            size=11,
                                        ),
                                        Text(
                                            "Feels Like",
                                            size=9,
                                            color="white54"
                                        )
                                    ]
                                )
                            )
                        ]
                    ),
                    _today_extra,
                ]
            )
        )

        return top
   
    _c = Container(
        width=310,
        height=660,
        border_radius=35,
        bgcolor="black",
        padding=10,
        content=Stack(
            width=300, 
            height=550,
            controls=[
                _top()
            ])

    )
    page.add(_c)

if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")