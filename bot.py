#!/usr/bin/env python3
"""
NaijaGrant Tracker – Telegram bot for Nigerian grants & empowerment opportunities.

Setup:
  1. Copy .env.example to .env and fill BOT_TOKEN + ADMIN_IDS
  2. pip install -r requirements.txt
  3. python bot.py
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
)

import database as db
from handlers import user, admin

# Load .env from project root
load_dotenv(Path(__file__).parent / ".env")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token or token == "your_bot_token_here":
        raise SystemExit(
            "❌ BOT_TOKEN not set. Copy .env.example to .env and add your token from @BotFather."
        )

    # Initialise database (creates tables + seeds sample data on first run)
    db.init_db()
    admin.load_admin_ids()

    app = Application.builder().token(token).build()

    # ----- User commands -----
    app.add_handler(CommandHandler("start", user.start))
    app.add_handler(CommandHandler("help", user.help_command))
    app.add_handler(CommandHandler("categories", user.categories))
    app.add_handler(CommandHandler("latest", user.latest))
    app.add_handler(CommandHandler("saved", user.saved))
    app.add_handler(CommandHandler("prefs", user.prefs))

    # Search conversation
    search_conv = ConversationHandler(
        entry_points=[
            CommandHandler("search", user.search_start),
            MessageHandler(filters.Regex("^🔍 Search$"), user.search_start),
        ],
        states={
            user.WAITING_SEARCH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, user.search_receive)
            ],
        },
        fallbacks=[CommandHandler("cancel", admin.cancel)],
        allow_reentry=True,
    )
    app.add_handler(search_conv)

    # Reply-keyboard text router (must be after conversation handlers)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, user.text_router)
    )

    # Callback queries
    app.add_handler(CallbackQueryHandler(user.category_callback, pattern=r"^cat:"))
    app.add_handler(CallbackQueryHandler(user.grant_callback, pattern=r"^grant:"))
    app.add_handler(CallbackQueryHandler(user.url_callback, pattern=r"^url:"))
    app.add_handler(CallbackQueryHandler(user.save_callback, pattern=r"^(save|unsave):"))
    app.add_handler(CallbackQueryHandler(user.show_cats_callback, pattern=r"^show_cats$"))
    app.add_handler(CallbackQueryHandler(user.pref_callback, pattern=r"^pref:"))
    app.add_handler(CallbackQueryHandler(user.setstate_callback, pattern=r"^setstate:"))
    app.add_handler(CallbackQueryHandler(user.setcat_callback, pattern=r"^setcat:"))

    # ----- Admin -----
    app.add_handler(CommandHandler("admin", admin.admin_help))
    app.add_handler(CommandHandler("stats", admin.stats))
    app.add_handler(CommandHandler("listgrants", admin.list_grants))
    app.add_handler(CommandHandler("deletegrant", admin.delete_grant_cmd))
    app.add_handler(CommandHandler("closgrant", admin.close_grant_cmd))
    app.add_handler(CommandHandler("broadcast", admin.broadcast))

    add_conv = ConversationHandler(
        entry_points=[CommandHandler("addgrant", admin.addgrant_start)],
        states={
            admin.TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_title)],
            admin.ORGANIZATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_org)],
            admin.CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_category)],
            admin.DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_description)],
            admin.ELIGIBILITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_eligibility)],
            admin.BENEFITS: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_benefits)],
            admin.DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_deadline)],
            admin.URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_url)],
            admin.AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_amount)],
            admin.TARGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_target)],
            admin.CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_confirm)],
        },
        fallbacks=[CommandHandler("cancel", admin.cancel)],
        allow_reentry=True,
    )
    app.add_handler(add_conv)

    logger.info("NaijaGrant Tracker starting…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
