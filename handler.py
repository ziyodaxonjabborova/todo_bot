from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

# Importing updated keyboard names
from buttons import (
    MAIN_MENU_KEYBOARD, 
    TASK_FILTER_KEYBOARD, 
    NAVIGATION_BACK_KEYBOARD, 
    TASK_UPDATE_KEYBOARD
)
from states import DataTask
from database import (
    add_task as db_add_task, 
    get_tasks_by_status, 
    update_task_name, 
    delete_task, 
    update_task_status
)

router = Router()

# --- Utility Function ---
async def return_to_main_menu(message: Message, state: FSMContext, text: str = "Returning to main menu:"):
    """Resets the state and sends the user back to the main dashboard."""
    await state.clear()
    await message.answer(text, reply_markup=MAIN_MENU_KEYBOARD)

# --- Start Handler ---
@router.message(CommandStart())
async def cmd_start(message: Message):
    """Initial greeting and menu display."""
    await message.answer(
        "👋 Welcome to Task Orchestrator! Select an option below:", 
        reply_markup=MAIN_MENU_KEYBOARD
    )

# --- Add Task Flow ---
@router.message(F.text == "➕ Add New Task")
async def start_add_task(message: Message, state: FSMContext):
    await message.answer("✍️ Please enter the name of the new task:", reply_markup=NAVIGATION_BACK_KEYBOARD)
    await state.set_state(DataTask.new_task)

@router.message(DataTask.new_task)
async def process_save_task(message: Message, state: FSMContext):
    if message.text == "⬅️ Return to Menu":
        return await return_to_main_menu(message, state)

    task_name = message.text.strip()
    db_add_task(message.from_user.id, task_name)
    await message.answer(f"✅ Task '{task_name}' successfully saved!", reply_markup=MAIN_MENU_KEYBOARD)
    await state.clear()

# --- View Tasks Flow ---
@router.message(F.text == "📋 View My Tasks")
async def show_filter_options(message: Message):
    await message.answer("🔍 Select task category to view:", reply_markup=TASK_FILTER_KEYBOARD)
    await message.answer("👇 Or use the button below to go back:", reply_markup=NAVIGATION_BACK_KEYBOARD)

@router.callback_query(F.data.startswith("filter_"))
async def process_view_tasks(call: CallbackQuery):
    status = call.data.split("_")[1]
    tasks = get_tasks_by_status(call.from_user.id, status)

    if not tasks:
        await call.message.answer(f"❌ No tasks found in category: {status.upper()}.", reply_markup=NAVIGATION_BACK_KEYBOARD)
        return

    report = f"📝 <b>Active Tasks ({status.capitalize()}):</b>\n\n"
    for task in tasks:
        report += f"🔹 {task['name']} — <i>{task['status'].capitalize()}</i>\n"

    await call.message.answer(report, parse_mode="HTML", reply_markup=NAVIGATION_BACK_KEYBOARD)
    await call.answer()

# --- Navigation Handler ---
@router.message(F.text == "⬅️ Return to Menu")
async def cmd_back(message: Message, state: FSMContext):
    await return_to_main_menu(message, state)

# --- Update Task Flow ---
@router.message(F.text == "✏️ Edit Task")
async def show_edit_options(message: Message):
    await message.answer("⚙️ What would you like to modify?", reply_markup=TASK_UPDATE_KEYBOARD)

@router.callback_query(F.data == "update_title")
async def start_rename_task(call: CallbackQuery, state: FSMContext):
    await call.message.answer("📝 Enter the current name of the task you want to rename:", reply_markup=NAVIGATION_BACK_KEYBOARD)
    await state.set_state(DataTask.get_old_name)
    await state.update_data(user_id=call.from_user.id)
    await call.answer()

@router.message(DataTask.get_old_name)
async def process_old_name(message: Message, state: FSMContext):
    if message.text == "⬅️ Return to Menu":
        return await return_to_main_menu(message, state)

    await state.update_data(old_name=message.text)
    await message.answer("🆕 Enter the new name for this task:", reply_markup=NAVIGATION_BACK_KEYBOARD)
    await state.set_state(DataTask.get_new_name)

@router.message(DataTask.get_new_name)
async def process_new_name(message: Message, state: FSMContext):
    if message.text == "⬅️ Return to Menu":
        return await return_to_main_menu(message, state)

    data = await state.get_data()
    success = update_task_name(data["user_id"], data["old_name"], message.text)
    
    if success:
        await message.answer("✅ Task renamed successfully!", reply_markup=MAIN_MENU_KEYBOARD)
    else:
        await message.answer("⚠️ Task not found. Please verify the name and try again.", reply_markup=NAVIGATION_BACK_KEYBOARD)
    await state.clear()

# --- Status Update Flow ---
@router.callback_query(F.data == "update_status")
async def start_toggle_status(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🔄 Enter the name of the task to update status:", reply_markup=NAVIGATION_BACK_KEYBOARD)
    await state.set_state(DataTask.get_status_task)
    await state.update_data(user_id=call.from_user.id)
    await call.answer()

@router.message(DataTask.get_status_task)
async def process_status_target(message: Message, state: FSMContext):
    if message.text == "⬅️ Return to Menu":
        return await return_to_main_menu(message, state)

    await state.update_data(task_name=message.text)
    await message.answer("🟢 Enter new status (pending/done):", reply_markup=NAVIGATION_BACK_KEYBOARD)
    await state.set_state(DataTask.get_new_status)

@router.message(DataTask.get_new_status)
async def process_status_update(message: Message, state: FSMContext):
    if message.text == "⬅️ Return to Menu":
        return await return_to_main_menu(message, state)

    new_status = message.text.lower().strip()
    if new_status not in ["pending", "done"]:
        await message.answer("⚠️ Invalid status. Use 'pending' or 'done':", reply_markup=NAVIGATION_BACK_KEYBOARD)
        return  

    data = await state.get_data()
    success = update_task_status(data["user_id"], data["task_name"], new_status)
    
    if success:
        await message.answer(f"✅ Status updated to '{new_status.upper()}'!", reply_markup=MAIN_MENU_KEYBOARD)
    else:
        await message.answer("⚠️ Task not found!", reply_markup=NAVIGATION_BACK_KEYBOARD)
    await state.clear()

# --- Delete Task Flow ---
@router.message(F.text == "🗑 Remove Task")
async def start_delete_task(message: Message, state: FSMContext):
    await message.answer("🗑 Which task would you like to permanently remove?", reply_markup=NAVIGATION_BACK_KEYBOARD)
    await state.set_state(DataTask.get_delete_task)
    await state.update_data(user_id=message.from_user.id)

@router.message(DataTask.get_delete_task)
async def process_deletion(message: Message, state: FSMContext):
    if message.text == "⬅️ Return to Menu":
        return await return_to_main_menu(message, state)

    data = await state.get_data()
    success = delete_task(data["user_id"], message.text)
    
    if success:
        await message.answer("🗑 Task successfully deleted!", reply_markup=MAIN_MENU_KEYBOARD)
    else:
        await message.answer("⚠️ Task not found. Verify the name and try again.", reply_markup=NAVIGATION_BACK_KEYBOARD)
    await state.clear()