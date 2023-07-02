from random import randint
from flask import render_template, request, flash, redirect, url_for, Response
from flask_login import login_required, current_user
from . import subscribe_routes
from ..models import User, Subscribe, Access, db
from ..events import backend_my_private_event


@subscribe_routes.route('/payment', methods=['GET', 'POST'])
@login_required
def payment() -> str:
    dict_user = {
        'name': current_user.name,
        'login': current_user.login,
        'balance': User.get_balance(current_user)
    }

    if request.method == 'POST':
        summa = float(request.form.get('summa'))
        status = randint(0, 1)

        if status:
            subscribe = current_user.subscribe if current_user.subscribe else None

            if subscribe:
                subscribe.balance += summa
            else:
                new_subscribe = Subscribe(
                    user_id=current_user.id,
                    balance=summa
                )
                db.session.add(new_subscribe)

            db.session.commit()

            dict_user.update({
                'balance': User.get_balance(current_user)
            })

            backend_my_private_event('payment success', f"private_room_{current_user.login}")
            flash('Your transaction is success')
            return render_template('payment.html', user=dict_user)
        else:
            backend_my_private_event('payment reject', f"private_room_{current_user.login}")
            flash('Your transaction is reject')
            return render_template('payment.html', user=dict_user)

    return render_template('payment.html', user=dict_user)


@subscribe_routes.route('/paid', methods=['POST'])
@login_required
def paid() -> Response:
    article_id = request.form.get('article_id')
    subscribe = current_user.subscribe if current_user.subscribe else None
    cost = randint(0, 10)

    if subscribe and subscribe.balance > cost:
        subscribe.balance -= cost

        access = Access(
            user_id=current_user.id,
            article_id=article_id
        )

        db.session.add(access)
        db.session.commit()

        backend_my_private_event(f"access granted to article {article_id}", f"private_room_{current_user.login}")
        flash('Access granted')
    else:
        backend_my_private_event(f"access not granted to article {article_id}", f"private_room_{current_user.login}")
        flash('Access not granted')

    return redirect(url_for('articles.article', article_id=article_id))
