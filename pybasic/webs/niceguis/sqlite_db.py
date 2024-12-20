#!/usr/bin/env python3
from typing import List

import models
from tortoise.contrib.fastapi import register_tortoise

from nicegui import app, ui


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},  # tortoise will look for models in this main module
    generate_schemas=True,  # in production you should use version control migrations instead
)


@ui.refreshable
async def list_of_users() -> None:
    async def delete(user: models.User) -> None:
        await user.delete()
        list_of_users.refresh()

    users: List[models.User] = await models.User.all()
    for user in reversed(users):
        with ui.card():
            with ui.row().classes('items-center'):
                ui.input('Name', on_change=user.save) \
                    .bind_value(user, 'name').on('blur', list_of_users.refresh)
                ui.number('Age', on_change=user.save, format='%.0f') \
                    .bind_value(user, 'age').on('blur', list_of_users.refresh).classes('w-20')
                ui.button(icon='delete', on_click=lambda u=user: delete(u)).props('flat')


@ui.page('/')
async def index():
    async def create() -> None:
        await models.User.create(name=name.value, age=age.value or 0)
        name.value = ''
        age.value = None
        list_of_users.refresh()

    with ui.column().classes('mx-auto'):
        with ui.row().classes('w-full items-center px-4'):
            name = ui.input(label='Name')
            age = ui.number(label='Age', format='%.0f').classes('w-20')
            ui.button(on_click=create, icon='add').props('flat').classes('ml-auto')
        await list_of_users()

ui.run(port=8083)
