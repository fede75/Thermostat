import web
import model

# Url mappings
urls = (
    '/', 'index',
    '/add', 'add',
    '/list_programs', 'list_programs',
    '/new_program', 'new_program',
    '/delete/(\d+)', 'delete',
    '/edit/(\d+)', 'edit'
)


# Templates
t_globals = {
    'datestr': web.datestr
}

render = web.template.render('templates', base='base', globals={ 'str': str })

db = web.database(dbn='sqlite', db='/home/pi/Thermostat/backThermostat/thermostat.db')


class index:
    formManual = web.form.Form(
        web.form.Dropdown('active', [(0, 'Automatic'), (1, 'Manual')],description="Mode:"),
        web.form.Textbox('temp', web.form.notnull, size=4, description="Manual Temp:"),
        web.form.Button('Save Program')
    )

    def GET(self):
        formManual=self.formManual()
        last_temp = model.get_last_temp()
        list_temp = model.get_list_temp()
        active_program=model.get_active_program()
        manual_program = model.get_manual_program()
        formManual.fill(manual_program)
        return render.index(last_temp,list_temp,formManual,active_program)

    def POST(self):
        formManual=self.formManual()
        last_temp = model.get_last_temp()
        list_temp = model.get_list_temp()
        manual_program = model.get_manual_program()
        if not formManual.validates():
            formManual.fill(manual_program)
            return render.index(last_temp,list_temp,formManual)
        model.update_manual_program(formManual.d.active,formManual.d.temp)
        raise web.seeother('/')


class list_programs:
    def GET(self):
        programs = model.get_programs()
        return render.list_programs(programs)


class new_program:
    form = web.form.Form(
        web.form.Textbox('day', web.form.notnull, size=1, description="Day:"),
        web.form.Textbox('hour_ini', web.form.notnull, size=5, description="Hour ini:"),
        web.form.Textbox('hour_end', web.form.notnull, size=5, description="Hour end:"),
        web.form.Textbox('temp', web.form.notnull, size=2, description="Temp:"),
        web.form.Button('Save Program'),
    )

    def GET(self):
        form = self.form()
        return render.new_program(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_program(form.d.day, form.d.hour_ini, form.d.hour_end, form.d.temp)
        raise web.seeother('/list_programs')


class delete:
    def GET(self, id):
        model.del_program(int(id))
        raise web.seeother('/list_programs')

class edit:
    def GET(self, id):
        program = model.get_program(int(id))
        form = new_program.form()
        form.fill(program)
        return render.edit(program, form)


    def POST(self, id):
        form = new_program.form()
        program = model.get_program(int(id))
        if not form.validates():
            return render.edit(program, form)
        model.update_program(int(id), form.d.day,form.d.hour_ini, form.d.hour_end, form.d.temp)
        raise web.seeother('/list_programs')


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
