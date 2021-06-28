import dash_bootstrap_components as dbc
import dash_html_components as html


dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("Model", href="/model"),
        dbc.DropdownMenuItem("Team", href="/team"),
    ],
    nav = True,
    in_navbar = True,
    label = "Menu",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        # dbc.Col(html.Img(src="/assets/virus.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("Tweety Hunter.ai", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="slategray",
    dark=True,
    className="mb-4",
)


