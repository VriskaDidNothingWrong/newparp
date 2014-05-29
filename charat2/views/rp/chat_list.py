from flask import abort, g, render_template, url_for
from sqlalchemy import and_, func
from sqlalchemy.orm import aliased, joinedload
from webhelpers import paginate

from charat2.helpers.auth import login_required
from charat2.model import (
    case_options,
    AnyChat,
    GroupChat,
    OneOnOneChat,
    PMChat,
    UserChat,
)
from charat2.model.connections import use_db

chat_classes = {
    None: AnyChat,
    "group": GroupChat,
    "1-on-1": OneOnOneChat,
    "pm": PMChat,
}

@use_db
@login_required
def chat_list(type=None, page=1):

    try:
        ChatClass = chat_classes[type]
    except KeyError:
        abort(404)

    if type in (None, "pm"):

        # Join opposing UserChat on PM chats so we know who the other person is.
        PMUserChat = aliased(UserChat)
        chats = g.db.query(UserChat, ChatClass, PMUserChat).join(ChatClass).outerjoin(
            PMUserChat,
            and_(
                ChatClass.type == "pm",
                PMUserChat.chat_id == ChatClass.id,
                PMUserChat.user_id != g.user.id,
            ),
        ).options(joinedload(PMUserChat.user))

        if type == "pm":
            chats = chats.filter(ChatClass.type == "pm")

    else:

        chats = g.db.query(UserChat, ChatClass).join(ChatClass).filter(
            ChatClass.type == type,
        )

    chats = chats.filter(
        UserChat.user_id == g.user.id,
    ).order_by(
        ChatClass.last_message.desc(),
    ).offset((page-1)*50).limit(50).all()

    if len(chats) == 0 and page != 1:
        abort(404)

    chat_count = g.db.query(func.count('*')).select_from(UserChat).filter(
        UserChat.user_id==g.user.id,
    )
    if type is not None:
        chat_count = chat_count.join(ChatClass).filter(ChatClass.type == type)
    chat_count = chat_count.scalar()

    paginator = paginate.Page(
        [],
        page=page,
        items_per_page=50,
        item_count=chat_count,
        url=lambda page: url_for("chat_list", page=page, type=type),
    )

    return render_template(
        "rp/chat_list.html",
        type=type,
        chats=chats,
        paginator=paginator,
    )

