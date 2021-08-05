import dash_html_components as html
import dash_bootstrap_components as dbc
import os
import base64


### IMAGES ### 
j_strasburger = "static/img/j_strasburger.jpg" # replace with your own image
jack_image = base64.b64encode(open(j_strasburger, 'rb').read())

luis_v = "static/img/luis_v.jpeg" # replace with your own image
luis_image = base64.b64encode(open(luis_v, 'rb').read())

sarah_z = "static/img/sarah_z.jpg" # replace with your own image
sarah_image = base64.b64encode(open(sarah_z, 'rb').read())

chris_k = "static/img/chris_k.jpg" # replace with your own image
chris_image = base64.b64encode(open(chris_k, 'rb').read())

murat_o = "static/img/murat_o.jpg" # replace with your own image
murat_image = base64.b64encode(open(murat_o, 'rb').read())


### BIOS ###
jack_bio = 'An avid outdoor adventurer, pilot and data analyst, Jack has spent many years refining his skills in data science. Jack works at General Motors in Austin, Texas.'
luis_bio = 'A fantastic musician, data scientist, and friend to all - Luis can be found spending his time pondering complex algorithms, writing new songs, and supporting the team. '
sarah_bio = 'Sarah leads with kindness and technological expertise, she specializes in Marketing Analytics and Statistics. Sarah works at Bolt in San Francisco, California.'
chris_bio = 'Our Social media analytics specialist, Chris got his start in esports and analytics as a self made entrepreneur. Chris works at General Motors in Austin, Texas.'
murat_bio = 'Murat is critical to our framework and web design. Murat is an active alumni at Tulane University where he graduated Cum Laude. Murat works at American First Finance.'

company_description = """Tweety Hunter is an application developed as a part of an Applied Machine Learning course at Tulane University. The Tweety Hunter application techonology can be applied to inform marketing teams in a wide range of industries. The application is a dash applicaiton, utilizes a flask framework, and is exclusivley written in Python. Much of the back-end processes are run on Amazon Web Services (AWS). We encourage future Tulane students and others to contact us with any questions."""

### LETS CODE SOME STYLED CARDS HERE ###
jack_card = dbc.Card(
    [
        dbc.CardImg(src=j_strasburger, top=True, style={'height':'100%', 'width':'100%'}),
        dbc.CardBody(
            [
                html.H4("Jack Strasburger", className="card-title"),
                html.P(jack_bio,className="card-text",
                ),
                # dbc.Button("Jack' Linkedin", color="primary"),
            ]
        )
    ]
)

luis_card = dbc.Card(
    [
        dbc.CardImg(src=luis_v, top=True, style={'height':'100%', 'width':'100%'}),
        dbc.CardBody(
            [
                html.H4("Luis Villaseñor", className="card-title"),
                html.P(luis_bio,className="card-text",
                ),
                # dbc.Button("Luis' Linkedin", color="primary"),
            ]
        )
    ]
)

sarah_card = dbc.Card(
    [
        dbc.CardImg(src=sarah_z, top=True, style={'height':'100%', 'width':'100%'}),
        dbc.CardBody(
            [
                html.H4("Sarah Zimmerman", className="card-title"),
                html.P(sarah_bio,className="card-text",
                ),
                # dbc.Button("Sarah's Linkedin", color="primary"),
            ]
        )
    ]
)

chris_card = dbc.Card(
    [
        dbc.CardImg(src=chris_k, top=True, style={'height':'100%', 'width':'100%'}),
        dbc.CardBody(
            [
                html.H4("Chris Kornaros", className="card-title"),
                html.P(chris_bio,className="card-text",
                ),
                # dbc.Button("Chris' Linkedin", color="primary"),
            ]
        )
    ]
)

murat_card = dbc.Card(
    [
        dbc.CardImg(src=murat_o, top=True, style={'height':'100%', 'width':'100%'}),
        dbc.CardBody(
            [
                html.H4("Murat Ogeturk", className="card-title"),
                html.P(murat_bio,className="card-text",
                ),
                # dbc.Button("Murat's Linkedin", color="primary"),
            ]
        )
    ]
)

### HTML PAGE LAYOUT ### 
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("About Us"), 
                html.P(company_description),],className="mx-2 my-2")
        ]),
        dbc.Row([
            dbc.Col(html.H2("Team"), className="mx-2 my-2")
        ]),
        dbc.Row([
                dbc.Col(dbc.Card(jack_card), md=4),
                dbc.Col(dbc.Card(sarah_card), md=4),
                dbc.Col(dbc.Card(murat_card), md=4)
        ]),
        dbc.Row([
                dbc.Col(dbc.Card(chris_card), md=4),
                dbc.Col(dbc.Card(luis_card), md=4)
        ], justify="center", className="mx-2 my-2")
    ])
])