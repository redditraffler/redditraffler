from flask import current_app
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
        current_app.logger.info('[COMMAND] Removing {}'.format(raffle_id))
        try:
            db.session.delete(raffle)
            db.session.commit()
            current_app.logger.info('[COMMAND] Removed {}'.format(raffle_id))
            click.echo('Successfully removed {}'.format(raffle_id))
        except:
            db.session.rollback()
            current_app.logger.exception(
                '[COMMAND] Error while trying to remove {}'.format(raffle_id)
            )
            click.echo('Something went wrong while deleting the raffle.')


@click.command()
@with_appcontext
def clear_cache():
    cache.clear()
    current_app.logger.info('[COMMAND] Cache cleared')
    click.echo('Cache cleared')
