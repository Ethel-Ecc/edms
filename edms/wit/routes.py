from flask import Blueprint, redirect, url_for, flash, render_template, request
from ckan_wit.src import wit_main as m

wit = Blueprint('wit', __name__)


@wit.route('/europe')
def europe():
    wit_europe = m.ckan_wit_main()['wit_resources']['EUROPE']
    main_metas = wit_europe['wit_metadata']

    return render_template('pages/ckan-wit/europe.html', title='Europe', wit_europe=wit_europe, main_metas=main_metas)


@wit.route('/america')
def america():
    wit_america = m.ckan_wit_main()['wit_resources']['AMERICAS']
    main_metas = wit_america['wit_metadata']
    return render_template('pages/ckan-wit/america.html', title='America', wit_america=wit_america, main_metas=main_metas)


@wit.route('/africa')
def africa():
    wit_africa = m.ckan_wit_main()['wit_resources']['AFRICA']
    main_metas = wit_africa['wit_metadata']
    return render_template('pages/ckan-wit/africa.html', title='Africa', wit_africa=wit_africa, main_metas=main_metas)


@wit.route('/asia')
def asia():
    wit_asia = m.ckan_wit_main()['wit_resources']['ASIA']
    main_metas = wit_asia['wit_metadata']
    return render_template('pages/ckan-wit/asia.html', title='Asia', wit_asia=wit_asia, main_metas=main_metas)
