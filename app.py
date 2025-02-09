from flask import Flask, render_template, redirect, url_for
from forms import ContactForm
from flask_mail import Mail, Message

s_app = Flask(__name__)
s_app.config['SECRET_KEY'] = 'Kenny,this is your secret key!'

@s_app.route('/')
def home():
    return render_template('home.html')


@s_app.route('/about')
def about():
    return render_template('about.html')


@s_app.route('/projects')
def projects():
    return render_template('projects.html')


@s_app.route('/plot_country_data_2019')
def plot_country_data_2019():
    from bokeh.plotting import figure, output_file, ColumnDataSource
    from bokeh.models.tools import HoverTool
    from bokeh.transform import factor_cmap
    from bokeh.palettes import Viridis256
    from bokeh.embed import components
    from bokeh.resources import CDN

    import pandas as pd

    dataF = pd.read_csv('CountriesPopulation_2019.csv')

    output_file('population_2019.html')

    data_source = ColumnDataSource(dataF)

    countries_list = list(data_source.data['Country'])

    fig = figure(y_range=countries_list,
                 plot_height=700,
                 plot_width=800,
                 title='The Population Of 2019',
                 x_axis_label='Population',
                 sizing_mode='scale_width'
                 )

    fig.hbar(y='Country',
             right='Population',
             left=0,
             height=0.7,
             fill_color=factor_cmap(
                 'Country',
                 factors=countries_list,
                 palette=Viridis256[:229]

             ),
             fill_alpha=0.8,
             source=data_source,
             )

    hover = HoverTool()
    hover.tooltips = """
    <div>
        <h2>@Country</h2>
        <div><b>Population: </b>@Population</div>
    </div>"""

    fig.add_tools(hover)

    script, div = components(fig)

    cdn_js = CDN.js_files[0]
    cdn_css = 'https://cdn.pydata.org/bokeh/release/bokeh-1.2.0.min.css'

    return render_template('country_data2019_plot.html',
                           script=script,
                           div=div,
                           cdn_css=cdn_css,
                           cdn_js=cdn_js)


@s_app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    s_app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    s_app.config['MAIL_PORT'] = 465
    s_app.config['MAIL_USE_SSL'] = True
    s_app.config['MAIL_DEBUG'] = True
    s_app.config['MAIL_USERNAME'] = '******************'
    s_app.config['MAIL_PASSWORD'] = '*********'
    s_app.config['MAIL_MAX_EMAILS'] = 3

    mail = Mail(s_app)
    if form.validate_on_submit():
        msg = Message(f"{form.title.data} from {form.name.data} from Kenny's web app",
                      sender=(form.name.data, '*****************'),
                      recipients=['****************'])
        msg.body = form.message.data
        mail.send(msg)
        return redirect(url_for('home'))
    return render_template('contact.html', form=form)


if __name__ == "__main__":
    s_app.run(debug=True)
