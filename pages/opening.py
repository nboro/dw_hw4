import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app

title = "We are here for a ride, darling."

content = html.Img(
    src=app.get_asset_url('imgs/freddie.png'),
    className="img-fluid mx-auto d-block",
    alt="https://fineartamerica.com/featured/2-freddie-mercury-melanie-d.html?product=kids-tshirt",
    title="Freddie Mercury"
)

description = html.Div([
    #html.H5("Lorem Ipsum", className="text-info"),
    html.P("""
    Why is a 40+ years old song still topping the billboard charts today? Yes. We are referring to Bohemian Rhapsody by 
    the famous British Rock band Queen. According to the Billboard ranking’s in the Netherlands Bohemian along with a 
    few other tracks such Hotel California and Imagine stands in the top three rankings of the billboard from 1999 to 2019. 
    Interestingly those are all Rock songs released before 1990. Does this mean that old music is better, or is new music 
    not as great? Looks like we will have to dig deep to find answers to this phenomenon.
    """),
    html.P("""
    We developed a tool that visualizes a collection of charts that could help analyze the billboard data of the top 2000 
    songs in the Netherlands along with additional data sources which could support to elaborate further the factors that 
    makes music rank higher or lower in the billboard.
    """),
    html.P("""
    So, sit back and cruise through the rocking journey down the billboard isle!
    """),

])
