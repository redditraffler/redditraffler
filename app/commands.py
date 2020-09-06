from flask.cli import with_appcontext
from html import unescape
import click

from app.db.models.raffle import Raffle
from app.extensions import db, cache


@click.command(name="delete")
@click.option("--raffle_id", required=True, help="ID of the raffle to remove")
@with_appcontext
def delete(raffle_id):
    try:
        raffle = Raffle.query.filter_by(submission_id=raffle_id).one()
    except:
        click.echo("Raffle '{}' does not exist.".format(raffle_id))
        return

    if click.confirm("Continue deleting Raffle {}?".format(raffle_id)):
        click.echo("[COMMAND] Removing {}".format(raffle_id))
        try:
            db.session.delete(raffle)
            db.session.commit()
            cache.delete("raffle_{}".format(raffle_id))
            click.echo("[COMMAND] Successfully removed {}".format(raffle_id))
        except Exception as e:
            db.session.rollback()
            click.echo("[COMMAND] Something went wrong while deleting the " "raffle.")
            click.echo(e)


@click.command(name="clear_cache")
@with_appcontext
def clear_cache():
    cache.clear()
    click.echo("[COMMAND] Cache cleared")


@click.command(name="unescape_submission_titles")
@with_appcontext
def unescape_submission_titles():
    try:
        updated_raffles = []
        for raffle in Raffle.query.all():
            original_title = raffle.submission_title
            updated_title = unescape(original_title)

            if updated_title == original_title:
                continue

            raffle.submission_title = updated_title
            updated_raffles.append(
                {"original": original_title, "updated": updated_title}
            )

        db.session.commit()
        click.echo("[COMMAND] Successfully unescaped raffle titles")
        click.echo(updated_raffles)
    except Exception as e:
        db.session.rollback()
        click.echo("[COMMAND] Error while trying to unescape submission titles")
        click.echo(e)

