import dash_html_components as html
import dash_bootstrap_components as dbc
import os
import base64


### IMAGES
j_strasburger = 'static/img/j_strasburger.jpg' # replace with your own image
jack_image = base64.b64encode(open(j_strasburger, 'rb').read())

luis_v = 'static/img/luis_v.jpeg' # replace with your own image
luis_image = base64.b64encode(open(luis_v, 'rb').read())

sarah_z = 'static/img/sarah_z.jpg' # replace with your own image
sarah_image = base64.b64encode(open(sarah_z, 'rb').read())

chris_k = 'static/img/chris_k.jpg' # replace with your own image
chris_image = base64.b64encode(open(chris_k, 'rb').read())

murat_o = 'static/img/murat_o.jpg' # replace with your own image
murat_image = base64.b64encode(open(murat_o, 'rb').read())


### BIOS
jack_bio = 'Born and raised in Houston, Texas, an avid outdoor adventurer, pilot and data analyst, Jack has spent many years refining his skills in data science. Jack works at General Motors in Austin, Texas.'
luis_bio = 'A fantastic musician, data scientist, and friend to all - Luis can be found spending his time pondering complex algorithms, writing new songs, and supporting the team. '
sarah_bio = 'Sarah leads with kindness and technological expertise, her skills and interests are in Marketing Analytics, Database Managemnet, Data Science, and Predictive Modeling. Sarah works at Bolt in San Francisco, California.'
chris_bio = 'Our Social media analytics specialist, Chris got his start in esports and analytics as a self made entrepreneur. Chris works at General Motors in Austin, Texas.'
murat_bio = 'Murat is critical to our framework and web design. Murat is an active alumni at Tulane University where he graduated Cum Laude. '

company_description = """Tweety Hunter is an application developed as a part of an Applied Machine Learning course at Tulane University. The Tweety Hunter application techonology can be applied to inform marketing teams in a wide range of industries. The application is a dash applicaiton, utilizes a flask framework, and is exclusivley written in Python. Much of the back-end processes are run on Amazon Web Services (AWS). We encourage future Tulane students and others to contact us with any questions."""


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("About Us"), 
                html.P(company_description),
                ],
                className='mx-2 my-2'
            )
        ]),
        dbc.Row([
            dbc.Col(html.H2("Team"), className='mx-2 my-2')
        ]),
        dbc.Row([
            dbc.Col(  
                dbc.Card(
                    dbc.Row([
                        dbc.Col([html.Div([html.Img(src='data:image/png;base64,{}'.format(jack_image.decode()),style={'width': '100%'})])], className='col-5'),
                        dbc.Col([
                            html.H5('Jack Strasburger'),
                            html.P(jack_bio)
                            ],
                            className='col-7'
                        )
                    ])
                ),
                className="col-6 mx-2 my-2"
            )
        ]),
        dbc.Row([
            dbc.Col(  
                dbc.Card(
                    dbc.Row([
                        dbc.Col([html.Div([html.Img(src='data:image/png;base64,{}'.format(luis_image.decode()),style={'width': '100%'})])], className='col-5'),
                        dbc.Col([
                            html.H5('Luis Villaseñor'),
                            html.P(luis_bio)
                            ],
                            className='col-7'
                        )
                    ])
                ),
                className="col-6 mx-2 my-2"
            )
        ]),
        dbc.Row([
            dbc.Col(  
                dbc.Card(
                    dbc.Row([
                        dbc.Col([html.Div([html.Img(src='data:image/png;base64,{}'.format(sarah_image.decode()),style={'width': '100%'})])], className='col-5'),
                        dbc.Col([
                            html.H5('Sarah Zimmerman'),
                            html.P(sarah_bio)
                            ],
                            className='col-7'
                        )
                    ])
                ),
                className="col-6 mx-2 my-2"
            )
        ]),
        dbc.Row([
            dbc.Col(  
                dbc.Card(
                    dbc.Row([
                        dbc.Col([html.Div([html.Img(src='data:image/png;base64,{}'.format(chris_image.decode()),style={'width': '100%'})])], className='col-5'),
                        dbc.Col([
                            html.H5('Chris Kornaros'),
                            html.P(chris_bio)
                            ],
                            className='col-7'
                        )
                    ])
                ),
                className="col-6 mx-2 my-2"
            )
        ]),
        dbc.Row([
            dbc.Col(  
                dbc.Card(
                    dbc.Row([
                        dbc.Col([html.Div([html.Img(src='data:image/png;base64,{}'.format(murat_image.decode()),style={'width': '100%'})])], className='col-5'),
                        dbc.Col([
                            html.H5('Murat Ogeturk'),
                            html.P(murat_bio)
                            ],
                            className='col-7'
                        )
                    ])
                ),
                className="col-6 mx-2 my-2"
            )
        ])
    ])
])
