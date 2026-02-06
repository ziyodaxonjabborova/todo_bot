from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

# 🔹 Main Dashboard (Reply Keyboard)
# Using 'Dashboard' or 'Menu' is more professional than 'CRUD'
MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Add New Task")],
        [KeyboardButton(text="📋 View My Tasks")],
        [KeyboardButton(text="✏️ Edit Task"), KeyboardButton(text="🗑 Remove Task")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Select an action from the menu..."
)

# 🔹 Task Filtering (Inline Keyboard)
# 'Filter' implies a more advanced system architecture
TASK_FILTER_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 All Tasks", callback_data="filter_all"),
            InlineKeyboardButton(text="⏳ Pending", callback_data="filter_pending"),
            InlineKeyboardButton(text="🏁 Completed", callback_data="filter_done")
        ]
    ]
)

# 🔹 Task Update Options (Inline Keyboard)
# Using 'Property' or 'Attribute' terminology for professional depth
TASK_UPDATE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Rename Task", callback_data="update_title"),
            InlineKeyboardButton(text="🔄 Toggle Status", callback_data="update_status")
        ]
    ]
)

# 🔹 Navigation (Reply Keyboard)
# Consistent naming convention for secondary navigation
NAVIGATION_BACK_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅️ Return to Menu")]
    ],
    resize_keyboard=True
)