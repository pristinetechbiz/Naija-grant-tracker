from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import ContextTypes, ConversationHandler
import database as db


WAITING_SEARCH = 1


def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["🔍 Search", "📂 Categories"],
            ["🆕 Latest Grants", "💾 Saved Grants"],
            ["👤 My Account", "🔔 My Alerts"],
            ["💎 Premium", "ℹ️ Help"],
        ],
        resize_keyboard=True,
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user

    db.upsert_user(
        u.id,
        u.username,
        u.first_name,
        u.last_name,
    )

    await update.message.reply_text(
    f"👋 Welcome {u.first_name or 'there'}!\n\n"
    "🇳🇬 NaijaGrant Tracker\n\n"
    "Find Nigerian grants, scholarships, loans, "
    "skills programmes and empowerment opportunities.\n\n"
    "Use the buttons below to get started.",
           reply_markup=main_menu(),
    )

async def my_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user

    db.upsert_user(
        u.id,
        u.username,
        u.first_name,
        u.last_name,
    )

    user = db.get_user(u.id)
    saved = db.get_saved_grants(u.id)

    name = " ".join(
        part for part in [u.first_name, u.last_name] if part
    ) or "Not set"

    username = f"@{u.username}" if u.username else "Not set"

    new_alerts = bool(user and user.get("notify_new"))
    deadline_alerts = bool(user and user.get("notify_deadline"))

    text = (
        "👤 MY ACCOUNT\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"👋 Welcome, {u.first_name or 'there'}\n\n"
        "📛 Name\n"
        f"{name}\n\n"
        "🔗 Username\n"
        f"{username}\n\n"
        "🆔 User ID\n"
        f"{u.id}\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📊 ACCOUNT SUMMARY\n\n"
        f"💾 Saved Grants       {len(saved)}\n"
        f"🔔 New Grant Alerts   {'ON' if new_alerts else 'OFF'}\n"
        f"⏰ Deadline Alerts    {'ON' if deadline_alerts else 'OFF'}\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💎 MEMBERSHIP\n\n"
        "Current Plan: FREE"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "💎 Upgrade to Premium",
                callback_data="account:premium",
            )
        ],
        [
            InlineKeyboardButton(
                "🔔 Manage Alerts",
                callback_data="account:alerts",
            ),
            InlineKeyboardButton(
                "💾 My Saved Grants",
                callback_data="account:saved",
            ),
        ],
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def my_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user

    db.upsert_user(
        u.id,
        u.username,
        u.first_name,
        u.last_name,
    )

    user = db.get_user(u.id)

    new_alerts = bool(user and user.get("notify_new"))
    deadline_alerts = bool(user and user.get("notify_deadline"))

    text = (
        "🔔 MY ALERTS\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "Manage the notifications you receive "
        "from NaijaGrant Tracker.\n\n"
        f"🆕 New Grant Alerts: "
        f"{'🟢 ON' if new_alerts else '🔴 OFF'}\n"
        f"⏰ Deadline Alerts: "
        f"{'🟢 ON' if deadline_alerts else '🔴 OFF'}\n\n"
        "Use ⚙️ Preferences to change your alert settings."
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "⚙️ Manage Preferences",
                callback_data="account:prefs",
            )
        ],
        [
            InlineKeyboardButton(
                "◀️ My Account",
                callback_data="account:back",
            )
        ],
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💎 NAIJAGRANT PREMIUM\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🚀 NEVER MISS AN OPPORTUNITY\n\n"
        "Get more from NaijaGrant Tracker "
        "and stay ahead of important opportunities.\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "✨ PREMIUM FEATURES\n\n"
        "🔔 Instant Grant Alerts\n"
        "Get notified when relevant new grants "
        "are added.\n\n"
        "🎯 Personalised Opportunities\n"
        "Receive opportunities based on your interests.\n\n"
        "⏰ Deadline Reminders\n"
        "Never forget an important application deadline.\n\n"
        "💾 Unlimited Saved Grants\n"
        "Save as many opportunities as you want.\n\n"
        "🔎 Advanced Search\n"
        "Find opportunities using powerful filters.\n\n"
        "⚡ Early Access\n"
        "Get selected opportunities before general promotion.\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💰 PREMIUM PLANS\n\n"
        "Monthly: ₦1,500 / month\n"
        "Yearly: ₦12,000 / year\n"
        "💡 Save ₦6,000 with the yearly plan\n\n"
        "Payment integration will be activated in Phase 2."
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "💳 Subscribe Monthly",
                callback_data="premium:monthly",
            )
        ],
        [
            InlineKeyboardButton(
                "💳 Subscribe Yearly",
                callback_data="premium:yearly",
            )
        ],
        [
            InlineKeyboardButton(
                "◀️ My Account",
                callback_data="account:back",
            )
        ],
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *NaijaGrant Tracker Help*\n\n"
        "/start - Start the bot\n"
        "/search - Search grants\n"
        "/categories - Browse categories\n"
        "/latest - Latest grants\n"
        "/saved - Your saved grants\n"
        "/prefs - Notification preferences\n"
        "/help - Show this help\n\n"
        "You can also use the menu buttons.",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cats = db.get_categories()

    if not cats:
        await update.message.reply_text(
            "No grant categories are currently available."
        )
        return

    keyboard = [
        [InlineKeyboardButton(c.title(), callback_data=f"cat:{c}")]
        for c in cats
    ]

    await update.message.reply_text(
        "📂 *Grant Categories*\n\nChoose a category:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    grants = db.search_grants(status="open", limit=10)

    if not grants:
        await update.message.reply_text("No open grants found.")
        return

    await update.message.reply_text(
        "🆕 *Latest Open Grants*",
        parse_mode="Markdown",
    )

    for grant in grants:
        await send_grant(update, grant)


async def saved(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    grants = db.get_saved_grants(user_id)

    if not grants:
        await update.message.reply_text(
            "💾 You have no saved grants yet.\n\n"
            "Open a grant and tap *Save Grant*.",
            parse_mode="Markdown",
        )
        return

    await update.message.reply_text(
        "💾 *Your Saved Grants*",
        parse_mode="Markdown",
    )

    for grant in grants:
        await send_grant(update, grant, saved=True)


async def prefs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current = db.get_user(user_id)

    state = current.get("preferred_state", "Nationwide") if current else "Nationwide"
    notify = current.get("notify_new", 1) if current else 1

    keyboard = [
        [
            InlineKeyboardButton(
                f"📍 State: {state}",
                callback_data="pref:state",
            )
        ],
        [
            InlineKeyboardButton(
                f"🔔 New Grant Alerts: {'ON' if notify else 'OFF'}",
                callback_data="pref:notify",
            )
        ],
        [
            InlineKeyboardButton(
                "📂 Categories",
                callback_data="pref:categories",
            )
        ],
    ]

    await update.message.reply_text(
        "⚙️ *Your Preferences*\n\n"
        "Choose what you want to change:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def search_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 *Search Grants*\n\n"
        "Type a keyword such as:\n"
        "• agriculture\n"
        "• women\n"
        "• youth\n"
        "• scholarship\n"
        "• business\n\n"
        "Type /cancel to stop.",
        parse_mode="Markdown",
    )

    return WAITING_SEARCH


async def search_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    if not query:
        await update.message.reply_text("Please enter a search term.")
        return WAITING_SEARCH

    grants = db.search_grants(
        query=query,
        status="open",
        limit=20,
    )

    if not grants:
        await update.message.reply_text(
            f"🔍 No open grants found for: *{query}*",
            parse_mode="Markdown",
        )
        return ConversationHandler.END

    await update.message.reply_text(
        f"🔍 Found {len(grants)} result(s) for *{query}*:",
        parse_mode="Markdown",
    )

    for grant in grants:
        await send_grant(update, grant)

    return ConversationHandler.END

async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔍 Search":
        return await search_start(update, context)

    if text == "📂 Categories":
        return await categories(update, context)

    if text == "🆕 Latest Grants":
        return await latest(update, context)

    if text == "💾 Saved Grants":
        return await saved(update, context)

    if text == "⚙️ Preferences":
        return await prefs(update, context)

    if text == "👤 My Account":
        return await my_account(update, context)

    if text == "🔔 My Alerts":
        return await my_alerts(update, context)

    if text == "💎 Premium":
        return await premium(update, context)

    if text == "ℹ️ Help":
        return await help_command(update, context)

    await update.message.reply_text("I didn't understand that command.\n\nUse the menu buttons or /help.")


async def account_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data.split(":", 1)[1]

    if action == "premium":
        await query.message.reply_text(
            "💎 NAIJAGRANT PREMIUM\\n\\n"
            "Premium subscriptions will be available soon."
        )
        return

    if action == "alerts":
        await query.message.reply_text(
            "🔔 My Alerts\\n\\n"
            "Use ⚙️ Preferences from the main menu "
            "to manage your notification settings."
        )
        return

    if action == "saved":
        grants = db.get_saved_grants(query.from_user.id)

        if not grants:
            await query.message.reply_text(
                "💾 You don't have any saved grants yet."
            )
            return

        await query.message.reply_text(
            f"💾 You have {len(grants)} saved grant(s)."
        )

        for grant in grants:
            await send_grant(query.message, grant, saved=True)

        return

    if action == "prefs":
        user = db.get_user(query.from_user.id)

        state = (
            user.get("preferred_state", "Nationwide")
            if user else "Nationwide"
        )

        notify = (
            user.get("notify_new", 1)
            if user else 1
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    f"📍 State: {state}",
                    callback_data="pref:state",
                )
            ],
            [
                InlineKeyboardButton(
                    f"🔔 New Grant Alerts: {'ON' if notify else 'OFF'}",
                    callback_data="pref:notify",
                )
            ],
            [
                InlineKeyboardButton(
                    "📂 Categories",
                    callback_data="pref:categories",
                )
            ],
        ]

        await query.message.reply_text(
            "⚙️ *Your Preferences*\\n\\n"
            "Choose what you want to change:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    if action == "back":
        await query.message.reply_text(
            "👤 *My Account*\\n\\n"
            "Use the account options from the main menu.",
            parse_mode="Markdown",
        )


async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.split(":", 1)[1]

    grants = db.search_grants(
        category=category,
        status="open",
        limit=20,
    )

    if not grants:
        await query.edit_message_text(
            f"No open grants found in *{category.title()}*.",
            parse_mode="Markdown",
        )
        return

    await query.edit_message_text(
        f"📂 *{category.title()} Grants*\n\n"
        f"Found {len(grants)} grant(s).",
        parse_mode="Markdown",
    )

    for grant in grants:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=format_grant(grant),
            parse_mode="Markdown",
            reply_markup=grant_keyboard(grant),
        )


async def grant_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    grant_id = int(query.data.split(":", 1)[1])
    grant = db.get_grant(grant_id)

    if not grant:
        await query.edit_message_text("This grant is no longer available.")
        return

    await query.edit_message_text(
        format_grant(grant),
        parse_mode="Markdown",
        reply_markup=grant_keyboard(grant),
    )


async def url_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    grant_id = int(query.data.split(":", 1)[1])
    grant = db.get_grant(grant_id)

    if not grant:
        await query.message.reply_text("Grant not found.")
        return

    url = grant.get("application_url")

    if not url:
        await query.message.reply_text(
            "No application URL is currently available."
        )
        return

    await query.message.reply_text(
        f"🔗 Application link:\n{url}"
    )


async def save_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, grant_id = query.data.split(":", 1)
    grant_id = int(grant_id)
    user_id = query.from_user.id

    if action == "save":
        db.save_grant_for_user(user_id, grant_id)
        await query.answer("✅ Grant saved!")
    else:
        db.unsave_grant(user_id, grant_id)
        await query.answer("🗑 Grant removed.")

    grant = db.get_grant(grant_id)

    if grant:
        await query.edit_message_reply_markup(
            reply_markup=grant_keyboard(
                grant,
                saved=(action == "save"),
            )
        )


async def show_cats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    cats = db.get_categories()

    keyboard = [
        [InlineKeyboardButton(c.title(), callback_data=f"cat:{c}")]
        for c in cats
    ]

    await query.edit_message_text(
        "📂 Choose a category:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def pref_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data.split(":", 1)[1]
    user_id = query.from_user.id

    if action == "notify":
        user = db.get_user(user_id)
        current = user.get("notify_new", 1) if user else 1
        db.set_user_preference(user_id, "notify_new", 0 if current else 1)

        await query.answer(
            "🔔 Notifications updated."
        )

    elif action == "state":
        await query.edit_message_text(
            "📍 State selection is coming next.\n\n"
            "For now, your default state is Nationwide."
        )

    elif action == "categories":
        cats = db.get_categories()

        keyboard = [
            [InlineKeyboardButton(c.title(), callback_data=f"setcat:{c}")]
            for c in cats
        ]

        await query.edit_message_text(
            "📂 Select your preferred category:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


async def setstate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    state = query.data.split(":", 1)[1]
    db.set_user_preference(
        query.from_user.id,
        "preferred_state",
        state,
    )

    await query.edit_message_text(
        f"📍 Preferred state updated to: *{state}*",
        parse_mode="Markdown",
    )


async def setcat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.split(":", 1)[1]
    user = db.get_user(query.from_user.id)

    existing = user.get("preferred_categories", "") if user else ""

    cats = [x.strip() for x in existing.split(",") if x.strip()]

    if category not in cats:
        cats.append(category)

    db.set_user_preference(
        query.from_user.id,
        "preferred_categories",
        ",".join(cats),
    )

    await query.edit_message_text(
        f"✅ *{category.title()}* added to your preferred categories.",
        parse_mode="Markdown",
    )


def format_grant(grant):
    title = grant.get("title", "Untitled Grant")
    organization = grant.get("organization", "Unknown")
    category = grant.get("category", "other")
    description = grant.get("description", "")
    eligibility = grant.get("eligibility", "")
    benefits = grant.get("benefits", "")
    deadline = grant.get("deadline", "Not specified")
    amount = grant.get("amount", "Not specified")
    states = grant.get("states", "Nationwide")
    target = grant.get("target_group", "")

    return (
        f"🎯 *{title}*\n\n"
        f"🏢 *Organization:* {organization}\n"
        f"📂 *Category:* {category.title()}\n"
        f"💰 *Amount:* {amount}\n"
        f"📅 *Deadline:* {deadline}\n"
        f"📍 *States:* {states}\n"
        f"👥 *Target:* {target}\n\n"
        f"📝 *Description*\n{description}\n\n"
        f"✅ *Eligibility*\n{eligibility}\n\n"
        f"🎁 *Benefits*\n{benefits}"
    )


def grant_keyboard(grant, saved=False):
    grant_id = grant["id"]

    save_text = "🗑 Remove Saved" if saved else "💾 Save Grant"
    save_action = "unsave" if saved else "save"

    buttons = [
        [
            InlineKeyboardButton(
                save_text,
                callback_data=f"{save_action}:{grant_id}",
            )
        ],
        [
            InlineKeyboardButton(
                "🔗 Application",
                callback_data=f"url:{grant_id}",
            )
        ],
    ]

    return InlineKeyboardMarkup(buttons)


async def send_grant(update, grant, saved=False):
    await update.message.reply_text(
        format_grant(grant),
        parse_mode="Markdown",
        reply_markup=grant_keyboard(grant, saved),
    )
