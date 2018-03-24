from flask.cli import with_appcontext
from app.db.models import Raffle
from app.extensions import db, cache
import click


@click.command()
@click.option('--raffle_id', required=True, help='ID of the raffle to remove')
@with_appcontext
def delete(raffle_id):
    try:
        raffle = Raffle.query.filter_by(submission_id=raffle_id).one()
    except:
        click.echo('Raffle \'{}\' does not exist.'.format(raffle_id))
        return

    if click.confirm('Continue deleting Raffle {}?'.format(raffle_id)):
        click.echo('[COMMAND] Removing {}'.format(raffle_id))
        try:
            db.session.delete(raffle)
            db.session.commit()
            cache.delete('raffle_{}'.format(raffle_id))
            click.echo('[COMMAND] Successfully removed {}'.format(raffle_id))
        except Exception as e:
            db.session.rollback()
            click.echo('[COMMAND] Something went wrong while deleting the '
                       'raffle.')
            click.echo(e)


@click.command()
@with_appcontext
def clear_cache():
    cache.clear()
    click.echo('[COMMAND] Cache cleared')
